
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

def simular_estudiante(username, probabilidad_acierto):
    try:
        user = User.objects.get(username=username)
        profile = user.profile
    except User.DoesNotExist:
        print(f"Error: El usuario {username} no existe.")
        return

    print(f"\n>>> Simulando para: {username} (Perfil de éxito: {probabilidad_acierto*100}%)")

    # 1. Resolver Examen Diagnóstico
    examen = ExamenDiagnostico.objects.first()
    if not examen:
        return
    
    preguntas = Pregunta.objects.filter(examen=examen)
    if not preguntas.exists():
        return

    # Limpiar previos
    RespuestaUsuario.objects.filter(usuario=user, pregunta__examen=examen).delete()
    ResultadoDiagnostico.objects.filter(estudiante=user, examen=examen).delete()

    respuestas_correctas = 0
    for pregunta in preguntas:
        opciones = list(pregunta.opciones.all())
        if not opciones: continue
        
        # Simular respuesta basada en su probabilidad
        if random.random() < probabilidad_acierto:
            opcion_seleccionada = next((o for o in opciones if o.es_correcta), random.choice(opciones))
        else:
            opciones_incorrectas = [o for o in opciones if not o.es_correcta]
            opcion_seleccionada = random.choice(opciones_incorrectas) if opciones_incorrectas else random.choice(opciones)

        if opcion_seleccionada.es_correcta:
            respuestas_correctas += 1
            
        RespuestaUsuario.objects.create(
            usuario=user, pregunta=pregunta,
            opcion_seleccionada=opcion_seleccionada,
            tiempo_respuesta=random.uniform(5.0, 40.0)
        )

    puntaje = (respuestas_correctas / preguntas.count()) * 100
    ResultadoDiagnostico.objects.create(estudiante=user, examen=examen, puntaje=puntaje)
    print(f"   [Diagnóstico] Puntaje: {puntaje:.2f}%")

    # 2. Recomendación y Progreso
    temas = list(Tema.objects.all())
    if temas:
        # Recomendamos un tema aleatorio para variar los datos del docente
        tema_recomendado = random.choice(temas)
        RecomendacionEstudiante.objects.filter(usuario=user).delete() # Limpiar previa
        RecomendacionEstudiante.objects.create(
            usuario=user, tema=tema_recomendado.nombre, metrica_desempeno=puntaje
        )
        print(f"   [Recomendación] Tema sugerido: {tema_recomendado.nombre}")

        # Simular Progreso
        ProgresoEstudiante.objects.filter(usuario=user, tema=tema_recomendado).delete()
        
        # Teoría (siempre la completan)
        ProgresoEstudiante.objects.create(
            usuario=user, tema=tema_recomendado, tipo_actividad='Teoría',
            grado=profile.grado or '5to', seccion=profile.seccion or 'A',
            porcentaje_completado=100.0
        )
        
        # Ejercicios (3 por tema)
        ejercicios = Ejercicio.objects.filter(tema=tema_recomendado)[:3]
        ejercicios_resueltos = 0
        for ej in ejercicios:
            es_correcto = random.random() < probabilidad_acierto
            if es_correcto: ejercicios_resueltos += 1
            
            ResultadoEjercicio.objects.create(
                usuario=user, ejercicio=ej, es_correcto=es_correcto,
                tiempo_empleado=random.randint(15, 90),
                feedback_mostrado="Simulación de feedback"
            )
            ProgresoEstudiante.objects.create(
                usuario=user, tema=tema_recomendado, tipo_actividad='Ejercicio',
                grado=profile.grado or '5to', seccion=profile.seccion or 'A',
                referencia_id=ej.id, porcentaje_completado=100.0 if es_correcto else 0.0
            )
        print(f"   [Práctica] Resolvió {ejercicios.count()} ejercicios ({ejercicios_resueltos} correctos).")

    # 3. Métricas
    metricas, _ = MetricasEstudiante.objects.get_or_create(usuario=user)
    metricas.precision_general = (puntaje + (probabilidad_acierto * 100)) / 2
    metricas.save()

if __name__ == "__main__":
    estudiantes = [
        ('Gaby07', 0.9),    # Estudiante excelente
        ('Jorge12', 0.6),   # Estudiante promedio
        ('Edwin07', 0.3),   # Estudiante con dificultades
        ('Laura01', 0.75),  # Estudiante buena
    ]
    
    print("=== INICIANDO SIMULACIÓN MULTI-USUARIO ===")
    for user, prob in estudiantes:
        simular_estudiante(user, prob)
    print("\n=== SIMULACIÓN FINALIZADA ===")
    print("Datos listos para ser visualizados en el Panel Docente.")
