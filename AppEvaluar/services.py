from typing import Dict, Optional
from django.contrib.auth.models import User
from .models import ResultadoDiagnostico, RespuestaUsuario, RecomendacionEstudiante, ResultadoEjercicio, Examen, Pregunta, Opcion
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Configurar Gemini si la API KEY existe
if hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class SinResultadosError(Exception):
    """Excepción lanzada cuando un estudiante no tiene resultados de diagnóstico."""
    pass

def obtener_feedback_ia(respuesta: RespuestaUsuario) -> str:
    """
    Genera una explicación pedagógica usando Gemini 1.5 Flash para una respuesta específica.
    """
    try:
        pregunta = respuesta.pregunta
        opcion_correcta = Opcion.objects.filter(pregunta=pregunta, es_correcta=True).first()
        
        # Determinar si el alumno acertó
        es_correcta = False
        respuesta_alumno = ""
        if pregunta.tipo == 'OPCION_MULTIPLE':
            es_correcta = respuesta.opcion_seleccionada and respuesta.opcion_seleccionada.es_correcta
            respuesta_alumno = respuesta.opcion_seleccionada.texto if respuesta.opcion_seleccionada else "Sin respuesta"
        else:
            respuesta_alumno = respuesta.respuesta_texto
            # Nota: Para texto corto, la lógica de "correcto" podría ser más compleja, 
            # por ahora confiamos en el juicio de la IA o comparativa simple.

        # Construir el prompt pedagógico refinado (HU40 Refactor)
        status_msg = "¡Respuesta Correcta!" if es_correcta else "Respuesta Incorrecta"
        prompt = (
            f"Eres un tutor de geometría experto para secundaria. Tu meta es la claridad pedagógica.\n\n"
            f"CONTEXTO:\n"
            f"- Pregunta: {pregunta.texto}\n"
            f"- El estudiante eligió: {respuesta_alumno} ({status_msg})\n"
            f"- Respuesta correcta real: {opcion_correcta.texto if opcion_correcta else 'N/A'}\n"
            f"- Tema: {pregunta.tema.nombre if pregunta.tema else 'Geometría'}\n"
            f"- Dificultad: {pregunta.dificultad}\n\n"
            f"TAREA:\n"
            f"Genera una explicación de EXACTAMENTE 3 líneas.\n"
            f"1. Si acertó: Felicita brevemente y explica por qué esa es la respuesta usando la propiedad geométrica.\n"
            f"2. Si falló: Identifica el error lógico más probable basado en su opción y guíalo paso a paso hacia la verdad.\n"
            f"Usa un lenguaje motivador, sencillo y directo."
        )

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Manejo de imagen (Multimodal)
        if pregunta.imagen:
            try:
                from PIL import Image
                img = Image.open(pregunta.imagen.path)
                response = model.generate_content([prompt, img])
            except Exception as e:
                logger.error(f"Error procesando imagen para IA: {e}")
                response = model.generate_content(prompt)
        else:
            response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        logger.error(f"Error al obtener feedback de IA: {e}")
        return "No se pudo generar la explicacion IA"

def asignar_preguntas_aleatorias(examen: Examen):
    """Busca preguntas disponibles para el tema del examen y las asigna aleatoriamente.
    
    Args:
        examen: El objeto Examen al cual se le asignarán las preguntas.
        
    Raises:
        ValueError: Si no existen suficientes preguntas disponibles para el tema.
    """
    # Filtrar preguntas: mismo tema, sin examen diagnóstico y sin examen de tema previo.
    preguntas_disponibles = Pregunta.objects.filter(
        tema=examen.tema,
        examen__isnull=True,
        examen_tema__isnull=True
    ).order_by('?') # Orden aleatorio
    
    if preguntas_disponibles.count() < examen.cantidad_preguntas:
        raise ValueError(
            f"No hay suficientes preguntas disponibles para el tema {examen.tema.nombre}. "
            f"Se requieren {examen.cantidad_preguntas} y solo hay {preguntas_disponibles.count()}."
        )
    
    # Tomar la cantidad necesaria y asignarlas
    seleccionadas = preguntas_disponibles[:examen.cantidad_preguntas]
    for pregunta in seleccionadas:
        pregunta.examen_tema = examen
        pregunta.save()

def calcular_recomendacion(estudiante: User) -> Optional[Dict]:
    """Calcula el tema que el estudiante debe reforzar basado en sus respuestas.

    Args:
        estudiante: El objeto User del estudiante para el cual se genera la
            recomendación.

    Returns:
        Un diccionario que contiene el tema recomendado y su métrica de
        desempeño (porcentaje de aciertos), o None si no se puede determinar.
        Ejemplo: {'tema': 'Ángulos', 'metrica': 25.0}

    Raises:
        SinResultadosError: Si el estudiante no tiene un ResultadoDiagnostico
            o no existen respuestas detalladas registradas.
    """
    if not ResultadoDiagnostico.objects.filter(estudiante=estudiante).exists():
        raise SinResultadosError(
            "El estudiante no tiene resultados de diagnóstico registrados.")
    
    respuestas = RespuestaUsuario.objects.filter(
        usuario=estudiante).select_related('pregunta', 'opcion_seleccionada')
    
    if not respuestas.exists():
        raise SinResultadosError(
            "No se encontraron respuestas detalladas para el estudiante.")

    resumen_temas: Dict[str, Dict] = {}

    for respuesta in respuestas:
        tema = respuesta.pregunta.categoria
        if tema not in resumen_temas:
            resumen_temas[tema] = {'correctas': 0, 'total': 0}
        
        resumen_temas[tema]['total'] += 1
        
        es_correcta = False
        if respuesta.pregunta.tipo == 'OPCION_MULTIPLE':
            if (respuesta.opcion_seleccionada and 
                respuesta.opcion_seleccionada.es_correcta):
                es_correcta = True
        
        if es_correcta:
            resumen_temas[tema]['correctas'] += 1

    mejor_recomendacion: Optional[Dict] = None
    min_porcentaje = 101.0

    # Ordenar temas alfabéticamente para asegurar consistencia en empates
    for tema in sorted(resumen_temas.keys()):
        datos = resumen_temas[tema]
        porcentaje = (datos['correctas'] / datos['total']) * 100
        
        if porcentaje < min_porcentaje:
            min_porcentaje = porcentaje
            mejor_recomendacion = {
                'tema': tema,
                'metrica': round(porcentaje, 2),
                'total_preguntas': datos['total'],
                'correctas': datos['correctas']
            }

    if mejor_recomendacion:
        # Persistir la recomendación (HU08)
        # Eliminamos previa para mantener solo una (la más reciente del diagnóstico)
        RecomendacionEstudiante.objects.filter(usuario=estudiante).delete()
        RecomendacionEstudiante.objects.create(
            usuario=estudiante,
            tema=mejor_recomendacion['tema'],
            metrica_desempeno=mejor_recomendacion['metrica']
        )

        # HU15: Ajuste de dificultad inicial basado en el diagnóstico
        # Regla: 0-40 (Básico), 41-75 (Intermedio), 76-100 (Avanzado)
        # Nota: Usamos la métrica del tema con menor desempeño para nivelar desde la base
        metrica = mejor_recomendacion['metrica']
        if metrica <= 40:
            nuevo_nivel = 'Básico'
        elif metrica <= 75:
            nuevo_nivel = 'Intermedio'
        else:
            nuevo_nivel = 'Avanzado'

        if hasattr(estudiante, 'profile'):
            estudiante.profile.nivel_dificultad_actual = nuevo_nivel
            estudiante.profile.save()

    return mejor_recomendacion

def ajustar_dificultad_estudiante(estudiante: User):
    """
    Analiza los últimos 5 resultados de ejercicios para ajustar el nivel del estudiante.
    Regla: >= 80% aciertos sube de nivel.
    """
    if not hasattr(estudiante, 'profile'):
        return

    # Obtener los últimos 5 resultados
    ultimos_resultados = ResultadoEjercicio.objects.filter(
        usuario=estudiante
    ).order_by('-fecha_resolucion')[:5]

    if ultimos_resultados.count() < 5:
        # No hay suficiente historia para ajustar
        return

    # Calcular desempeño en la sesión
    aciertos = sum(1 for r in ultimos_resultados if r.es_correcto)
    porcentaje = (aciertos / 5) * 100

    nivel_actual = estudiante.profile.nivel_dificultad_actual
    nuevo_nivel = nivel_actual

    if porcentaje >= 80:
        # Subir de nivel
        if nivel_actual == 'Básico':
            nuevo_nivel = 'Intermedio'
        elif nivel_actual == 'Intermedio':
            nuevo_nivel = 'Avanzado'
    
    # Por ahora no bajamos nivel para evitar desmotivación, solo mantenemos o subimos.
    
    if nuevo_nivel != nivel_actual:
        estudiante.profile.nivel_dificultad_actual = nuevo_nivel
        estudiante.profile.save()
