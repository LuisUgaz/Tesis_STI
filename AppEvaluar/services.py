from typing import Dict, Optional
from django.contrib.auth.models import User
from .models import ResultadoDiagnostico, RespuestaUsuario, RecomendacionEstudiante, ResultadoEjercicio, Examen, Pregunta, Opcion, Ejercicio, LogEntrenamientoSVM
from AppTutoria.models import Tema
import google.generativeai as genai
from django.conf import settings
import logging
from django.db.models import Avg, StdDev
import math
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import numpy as np

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
    """Busca preguntas disponibles para el tema del examen y las asigna aleatoriamente."""
    preguntas_disponibles = Pregunta.objects.filter(
        tema=examen.tema,
        examen__isnull=True,
        examen_tema__isnull=True
    ).order_by('?')
    
    if preguntas_disponibles.count() < examen.cantidad_preguntas:
        raise ValueError(
            f"No hay suficientes preguntas disponibles para el tema {examen.tema.nombre}."
        )
    
    seleccionadas = preguntas_disponibles[:examen.cantidad_preguntas]
    for pregunta in seleccionadas:
        pregunta.examen_tema = examen
        pregunta.save()

def resolver_empate_svm(estudiante: User, temas_empatados: list) -> str:
    """
    Utiliza un clasificador SVM para decidir qué tema priorizar en caso de empate.
    Variables: tiempo promedio global, nivel, puntos.
    Incorpora aprendizaje evolutivo basado en LogEntrenamientoSVM.
    """
    try:
        if not temas_empatados: return None
        if len(temas_empatados) == 1: return temas_empatados[0]

        # 1. Preparar features del estudiante actual
        profile = getattr(estudiante, 'profile', None)
        puntos = float(profile.puntos_acumulados) if profile else 0
        nivel = 1
        if profile:
            niveles = {'Básico': 1, 'Intermedio': 2, 'Avanzado': 3}
            nivel = niveles.get(profile.nivel_dificultad_actual, 1)
        
        # Tiempo promedio global de respuestas correctas
        avg_time = RespuestaUsuario.objects.filter(
            usuario=estudiante, 
            opcion_seleccionada__es_correcta=True
        ).aggregate(Avg('tiempo_respuesta'))['tiempo_respuesta__avg'] or 30.0
        
        X_current = np.array([[float(avg_time), float(nivel), float(puntos)]])

        # 2. Obtener datos de entrenamiento reales (Excluir pendientes de feedback)
        logs_reales = LogEntrenamientoSVM.objects.exclude(fue_exito__isnull=True)
        
        if logs_reales.count() >= 10:
            # Entrenamiento con datos reales de la base de datos
            X_train = np.array([
                [l.tiempo_promedio, float(l.nivel_estudiante), l.puntos_acumulados] 
                for l in logs_reales
            ])
            # y=1 si fue éxito (reforzamos la decisión tomada), y=0 si fue fallo
            y_train = np.array([1 if l.fue_exito else 0 for l in logs_reales])
        else:
            # Fallback a datos sintéticos iniciales ampliados
            X_train = np.array([
                [10, 3, 500], [60, 1, 50], [15, 2, 400], [50, 1, 100],
                [12, 3, 600], [55, 1, 80], [20, 2, 350], [45, 1, 120]
            ])
            y_train = np.array([1, 0, 1, 0, 1, 0, 1, 0])

        # 3. Normalización (Escalado) para manejar diferentes magnitudes (puntos vs nivel)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_current_scaled = scaler.transform(X_current)

        # 4. Clasificación SVM
        clf = SVC(kernel='linear', C=1.0)
        clf.fit(X_train_scaled, y_train)
        
        prediccion = clf.predict(X_current_scaled)[0]
        # Si la predicción es 1 (éxito probable con cambio), prioriza el segundo tema.
        # Esto es una lógica simplificada para el desempate.
        indice_elegido = 1 if prediccion == 1 else 0
        tema_elegido_nombre = temas_empatados[indice_elegido]

        # 5. Registrar en el log para futura retroalimentación (etiqueta 'fue_exito' pendiente)
        tema_obj = Tema.objects.filter(nombre=tema_elegido_nombre).first()
        if tema_obj:
            LogEntrenamientoSVM.objects.create(
                estudiante=estudiante,
                tema_elegido=tema_obj,
                tiempo_promedio=float(avg_time),
                nivel_estudiante=nivel,
                puntos_acumulados=puntos,
                fue_exito=None 
            )
        
        return tema_elegido_nombre

    except Exception as e:
        logger.error(f"Error en SVM desempate dinámico: {e}")
        return temas_empatados[0] if temas_empatados else None

def evaluar_exito_recomendacion(estudiante: User, tema_nombre: str, es_correcto: bool):
    """
    Evalúa si la recomendación actual está siendo efectiva para actualizar el LogEntrenamientoSVM.
    Se llama cada vez que el estudiante resuelve un ejercicio de práctica.
    """
    try:
        tema = Tema.objects.filter(nombre=tema_nombre).first()
        if not tema: return

        # Buscar el último log pendiente para este estudiante y tema
        ultimo_log = LogEntrenamientoSVM.objects.filter(
            estudiante=estudiante,
            tema_elegido=tema,
            fue_exito__isnull=True
        ).order_by('-fecha_recomendacion').first()

        if ultimo_log:
            # Si el estudiante acierta, marcamos como éxito de la recomendación
            if es_correcto:
                ultimo_log.fue_exito = True
                ultimo_log.save()
            # En un sistema más complejo, el fallo esperaría a varios intentos antes de marcar False
    except Exception as e:
        logger.error(f"Error al evaluar éxito de recomendación: {e}")

def calcular_recomendacion(estudiante: User) -> Optional[Dict]:
    """Calcula el tema que el estudiante debe reforzar basado en sus respuestas.
    Incorpora dificultad de pregunta, tiempo de respuesta y SVM para empates (HU42).
    """
    if not ResultadoDiagnostico.objects.filter(estudiante=estudiante).exists():
        raise SinResultadosError("No hay resultados de diagnóstico.")
    
    respuestas = RespuestaUsuario.objects.filter(
        usuario=estudiante).select_related('pregunta', 'opcion_seleccionada', 'pregunta__tema')
    
    if not respuestas.exists():
        raise SinResultadosError("No se encontraron respuestas detalladas.")

    resumen_temas: Dict[str, Dict] = {}
    pesos_dificultad = {'Básico': 3, 'Intermedio': 2, 'Avanzado': 1}

    # Estadísticas globales para normalización de tiempo
    stats_tiempo = RespuestaUsuario.objects.filter(
        opcion_seleccionada__es_correcta=True
    ).values('pregunta_id').annotate(
        promedio=Avg('tiempo_respuesta'),
        desviacion=StdDev('tiempo_respuesta')
    )
    dict_stats = {s['pregunta_id']: s for s in stats_tiempo}

    for respuesta in respuestas:
        pregunta = respuesta.pregunta
        tema = pregunta.tema.nombre if pregunta.tema else "General"
        dificultad = pregunta.dificultad or 'Básico'
        peso = pesos_dificultad.get(dificultad, 1)

        if tema not in resumen_temas:
            resumen_temas[tema] = {'score_obtenido': 0.0, 'score_maximo': 0, 'correctas': 0, 'total': 0}
        
        resumen_temas[tema]['total'] += 1
        resumen_temas[tema]['score_maximo'] += peso
        
        es_correcta = False
        if (respuesta.opcion_seleccionada and respuesta.opcion_seleccionada.es_correcta):
            es_correcta = True
        
        if es_correcta:
            puntos_ganados = float(peso)
            if respuesta.tiempo_respuesta:
                stats = dict_stats.get(pregunta.id)
                if stats and stats['promedio'] and stats['desviacion']:
                    promedio, desviacion = float(stats['promedio']), float(stats['desviacion'])
                    if desviacion > 0:
                        z_score = (respuesta.tiempo_respuesta - promedio) / desviacion
                        if z_score > 1.5:
                            puntos_ganados *= (1 - min(0.3, (z_score - 1.5) * 0.1))
            
            resumen_temas[tema]['correctas'] += 1
            resumen_temas[tema]['score_obtenido'] += puntos_ganados

    # Identificar temas con el PDP más bajo
    temas_finales = []
    min_pdp = 101.0

    for tema in sorted(resumen_temas.keys()):
        datos = resumen_temas[tema]
        pdp = (datos['score_obtenido'] / datos['score_maximo']) * 100 if datos['score_maximo'] > 0 else 0
        datos['pdp_final'] = round(pdp, 2)
        
        if pdp < min_pdp:
            min_pdp = pdp
            temas_finales = [tema]
        elif math.isclose(pdp, min_pdp, rel_tol=1e-5):
            temas_finales.append(tema)

    # Resolver empate con SVM
    tema_elegido = temas_finales[0]
    if len(temas_finales) > 1:
        tema_elegido = resolver_empate_svm(estudiante, temas_finales)

    datos_finales = resumen_temas[tema_elegido]
    mejor_recomendacion = {
        'tema': tema_elegido,
        'metrica': datos_finales['pdp_final'],
        'total_preguntas': datos_finales['total'],
        'correctas': datos_finales['correctas']
    }

    # Persistencia
    RecomendacionEstudiante.objects.filter(usuario=estudiante).delete()
    RecomendacionEstudiante.objects.create(
        usuario=estudiante,
        tema=tema_elegido,
        metrica_desempeno=mejor_recomendacion['metrica']
    )

    # HU15: Ajuste de dificultad inicial (RANGOS ACTUALIZADOS)
    metrica = mejor_recomendacion['metrica']
    nuevo_nivel = 'Básico' if metrica <= 40 else ('Intermedio' if metrica <= 75 else 'Avanzado')
    if hasattr(estudiante, 'profile'):
        estudiante.profile.nivel_dificultad_actual = nuevo_nivel
        estudiante.profile.save()

    return mejor_recomendacion

def ajustar_dificultad_estudiante(estudiante: User):
    """
    Analiza los últimos 5 resultados de ejercicios para ajustar el nivel del estudiante.
    Incorpora PDP y penalización por tiempo (HU42).
    """
    if not hasattr(estudiante, 'profile'): return
    
    ultimos_resultados = ResultadoEjercicio.objects.filter(usuario=estudiante).order_by('-fecha_resolucion')[:5]
    if ultimos_resultados.count() < 5: return
    
    pesos_dificultad = {'Básico': 3, 'Intermedio': 2, 'Avanzado': 1}
    score_obtenido = 0.0
    score_maximo = 0

    # Estadísticas para tiempo (ejercicios)
    stats_tiempo = ResultadoEjercicio.objects.filter(
        es_correcto=True
    ).values('ejercicio_id').annotate(
        promedio=Avg('tiempo_empleado'),
        desviacion=StdDev('tiempo_empleado')
    )
    dict_stats = {s['ejercicio_id']: s for s in stats_tiempo}

    for r in ultimos_resultados:
        peso = pesos_dificultad.get(r.ejercicio.dificultad, 1)
        score_maximo += peso
        
        if r.es_correcto:
            puntos = float(peso)
            # Penalización por tiempo (HU42)
            stats = dict_stats.get(r.ejercicio.id)
            if stats and stats['promedio'] and stats['desviacion'] and stats['desviacion'] > 0:
                z_score = (r.tiempo_empleado - float(stats['promedio'])) / float(stats['desviacion'])
                if z_score > 1.5:
                    puntos *= (1 - min(0.3, (z_score - 1.5) * 0.1))
            score_obtenido += puntos

    pdp = (score_obtenido / score_maximo) * 100 if score_maximo > 0 else 0
    nivel_actual = estudiante.profile.nivel_dificultad_actual
    nuevo_nivel = nivel_actual

    # Rangos adaptativos HU42/HU15
    if pdp >= 80:
        if nivel_actual == 'Básico': nuevo_nivel = 'Intermedio'
        elif nivel_actual == 'Intermedio': nuevo_nivel = 'Avanzado'
    elif pdp <= 40:
        if nivel_actual == 'Avanzado': nuevo_nivel = 'Intermedio'
        elif nivel_actual == 'Intermedio': nuevo_nivel = 'Básico'
    
    if nuevo_nivel != nivel_actual:
        estudiante.profile.nivel_dificultad_actual = nuevo_nivel
        estudiante.profile.save()
