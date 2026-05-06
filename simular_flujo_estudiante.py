
import os
import django
import random
from datetime import datetime

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesis_STI.settings')
django.setup()

from django.contrib.auth.models import User
from AppEvaluar.models import (
    ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, 
    ResultadoDiagnostico, RecomendacionEstudiante, Ejercicio, 
    ResultadoEjercicio, ResultadoExamen, Examen
)
from AppGestionUsuario.models import Profile, MetricasEstudiante
from AppTutoria.models import Tema, ProgresoEstudiante

def simular_flujo():
    username = 'estudiante_test'
    try:
        user = User.objects.get(username=username)
        profile = user.profile
    except User.DoesNotExist:
        print(f"Error: El usuario {username} no existe.")
        return

    print(f"--- Iniciando simulación para: {username} ---")

    # 1. Identificar Examen Diagnóstico
    examen = ExamenDiagnostico.objects.first()
    if not examen:
        print("Error: No hay exámenes diagnósticos en el sistema.")
        return
    
    print(f"1. Resolviendo Examen Diagnóstico: {examen.nombre}")
    preguntas = Pregunta.objects.filter(examen=examen)
    
    if not preguntas.exists():
        print("Error: El examen no tiene preguntas.")
        return

    # Limpiar respuestas previas para la simulación
    RespuestaUsuario.objects.filter(usuario=user, pregunta__examen=examen).delete()
    ResultadoDiagnostico.objects.filter(estudiante=user, examen=examen).delete()

    respuestas_correctas = 0
    for pregunta in preguntas:
        opciones = list(pregunta.opciones.all())
        if not opciones:
            continue
        
        # Simular respuesta (50% de probabilidad de acierto)
        opcion_seleccionada = random.choice(opciones)
        if opcion_seleccionada.es_correcta:
            respuestas_correctas += 1
            
        RespuestaUsuario.objects.create(
            usuario=user,
            pregunta=pregunta,
            opcion_seleccionada=opcion_seleccionada,
            tiempo_respuesta=random.uniform(10.0, 30.0)
        )

    puntaje = (respuestas_correctas / preguntas.count()) * 100
    ResultadoDiagnostico.objects.create(
        estudiante=user,
        examen=examen,
        puntaje=puntaje
    )
    print(f"   Examen finalizado. Puntaje: {puntaje:.2f}%")

    # 2. Generar Recomendación (Simulada si el servicio no se dispara automáticamente)
    # Buscamos un tema disponible para recomendar
    tema_recomendado = Tema.objects.first()
    if tema_recomendado:
        RecomendacionEstudiante.objects.create(
            usuario=user,
            tema=tema_recomendado.nombre,
            metrica_desempeno=puntaje
        )
        print(f"2. Recomendación generada: Estudiar el tema '{tema_recomendado.nombre}'")

        # 3. Simular Progreso en el Tema
        print(f"3. Simulando estudio y práctica del tema: {tema_recomendado.nombre}")
        
        # Registrar progreso de teoría
        ProgresoEstudiante.objects.create(
            usuario=user,
            tema=tema_recomendado,
            tipo_actividad='Teoría',
            grado=profile.grado or '5to',
            seccion=profile.seccion or 'A',
            porcentaje_completado=100.0
        )
        
        # Resolver ejercicios del tema
        ejercicios = Ejercicio.objects.filter(tema=tema_recomendado)[:3]
        for ej in ejercicios:
            es_correcto = random.choice([True, False])
            ResultadoEjercicio.objects.create(
                usuario=user,
                ejercicio=ej,
                es_correcto=es_correcto,
                tiempo_empleado=random.randint(20, 60),
                feedback_mostrado="Feedback de simulación"
            )
            # Registrar progreso del ejercicio
            ProgresoEstudiante.objects.create(
                usuario=user,
                tema=tema_recomendado,
                tipo_actividad='Ejercicio',
                grado=profile.grado or '5to',
                seccion=profile.seccion or 'A',
                referencia_id=ej.id,
                porcentaje_completado=100.0 if es_correcto else 0.0
            )
        
        print(f"   Se completó el estudio de teoría y se resolvieron {ejercicios.count()} ejercicios.")

    # 4. Actualizar Métricas (Simulado)
    metricas, _ = MetricasEstudiante.objects.get_or_create(usuario=user)
    metricas.precision_general = puntaje # Simplificado para la simulación
    metricas.save()
    
    print("--- Simulación finalizada con éxito ---")
    print(f"Verifica el progreso de {username} en el panel del docente.")

if __name__ == "__main__":
    simular_flujo()
