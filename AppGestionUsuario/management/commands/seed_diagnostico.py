import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile, MetricasEstudiante
from AppEvaluar.models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, ResultadoDiagnostico
from django.utils import timezone
from decimal import Decimal
from django.db import transaction

class Command(BaseCommand):
    help = 'Genera resultados realistas de exámenes diagnósticos para estudiantes entre 05 y 20'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad', 
            type=int, 
            default=5, 
            help='Número de estudiantes a los que se les generará un resultado'
        )
        parser.add_argument(
            '--examen_id', 
            type=int, 
            help='ID del examen diagnóstico específico a usar'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        examen_id = options.get('examen_id')

        # 1. Buscar el examen diagnóstico
        if examen_id:
            try:
                examen = ExamenDiagnostico.objects.get(id=examen_id)
            except ExamenDiagnostico.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Examen con ID {examen_id} no encontrado.'))
                return
        else:
            # Intentar obtener el primero si no se especifica ID
            examen = ExamenDiagnostico.objects.first()
            if not examen:
                self.stdout.write(self.style.ERROR('No se encontró ningún ExamenDiagnostico en la base de datos.'))
                return

        self.stdout.write(self.style.SUCCESS(f'Iniciando simulación para el examen: "{examen.nombre}"'))

        # 2. Obtener preguntas y validar que tengan opciones
        preguntas = list(examen.preguntas.all())
        if not preguntas:
            self.stdout.write(self.style.ERROR('El examen seleccionado no tiene preguntas vinculadas.'))
            return

        # 3. Filtrar estudiantes (rol='Estudiante') que aún no han realizado este diagnóstico
        estudiantes_evaluados = ResultadoDiagnostico.objects.filter(examen=examen).values_list('estudiante_id', flat=True)
        estudiantes = User.objects.filter(
            profile__rol='Estudiante'
        ).exclude(id__in=estudiantes_evaluados)[:cantidad]

        if not estudiantes.exists():
            self.stdout.write(self.style.WARNING('No se encontraron nuevos estudiantes para procesar.'))
            return

        self.stdout.write(f'Procesando {estudiantes.count()} estudiantes...\n')

        total_exito = 0

        for user in estudiantes:
            try:
                with transaction.atomic():
                    # Definir un perfil de desempeño realista
                    # Probabilidades: 25% Destacado, 50% Promedio, 25% Bajo
                    perfil = random.choices(['destacado', 'promedio', 'bajo'], weights=[25, 50, 25])[0]
                    
                    if perfil == 'destacado':
                        nota_objetivo = random.randint(17, 20)
                    elif perfil == 'promedio':
                        nota_objetivo = random.randint(11, 16)
                    else:
                        nota_objetivo = random.randint(5, 10)

                    # Asegurar un mínimo de aciertos para que la nota sea >= 5
                    # Nota = (aciertos / total) * 20  => aciertos = (Nota * total) / 20
                    min_aciertos = int((5 * len(preguntas)) / 20)
                    
                    aciertos_objetivo = int((nota_objetivo * len(preguntas)) / 20)
                    # Forzar que el objetivo sea al menos el mínimo para sacar 05
                    aciertos_objetivo = max(aciertos_objetivo, min_aciertos)

                    # Barajamos las preguntas para asignar cuáles serán correctas
                    indices_preguntas = list(range(len(preguntas)))
                    random.shuffle(indices_preguntas)
                    indices_correctos = set(indices_preguntas[:aciertos_objetivo])
                    
                    aciertos_reales = 0
                    tiempos = []
                    
                    # Generar las respuestas
                    for i, pregunta in enumerate(preguntas):
                        opciones = list(pregunta.opciones.all())
                        if not opciones:
                            continue
                        
                        correcta = next((o for o in opciones if o.es_correcta), None)
                        incorrectas = [o for o in opciones if not o.es_correcta]

                        # Asignar opción según el índice pre-calculado para cumplir la nota objetivo
                        if i in indices_correctos and correcta:
                            opcion_elegida = correcta
                            aciertos_reales += 1
                        else:
                            opcion_elegida = random.choice(incorrectas) if incorrectas else correcta

                        # Tiempo de respuesta "humano"
                        t_base = random.uniform(15, 60) if perfil == 'destacado' else random.uniform(30, 90)
                        tiempo_pregunta = round(t_base + random.uniform(-5, 15), 2)
                        tiempos.append(tiempo_pregunta)

                        RespuestaUsuario.objects.create(
                            usuario=user,
                            pregunta=pregunta,
                            opcion_seleccionada=opcion_elegida,
                            tiempo_respuesta=tiempo_pregunta
                        )

                    # Calcular puntaje final real basado en aciertos
                    puntaje_final = (aciertos_reales / len(preguntas)) * 20
                    puntaje_final = Decimal(str(round(puntaje_final, 2)))

                    # Guardar Resultado del Diagnóstico
                    ResultadoDiagnostico.objects.create(
                        estudiante=user,
                        examen=examen,
                        puntaje=puntaje_final
                    )

                    # Actualizar métricas del estudiante para alimentar la IA
                    metricas, _ = MetricasEstudiante.objects.get_or_create(usuario=user)
                    metricas.precision_general = Decimal(str(round((aciertos_reales / len(preguntas)) * 100, 2)))
                    metricas.rendimiento_academico = puntaje_final
                    metricas.tiempo_respuesta_promedio = Decimal(str(round(sum(tiempos) / len(tiempos), 2)))
                    metricas.save()

                    # Actualizar perfil si es necesario (ej: dificultad inicial basada en el diagnóstico)
                    profile = user.profile
                    if puntaje_final >= 17:
                        profile.nivel_dificultad_actual = 'Avanzado'
                    elif puntaje_final >= 12:
                        profile.nivel_dificultad_actual = 'Intermedio'
                    else:
                        profile.nivel_dificultad_actual = 'Básico'
                    profile.save()

                    self.stdout.write(f'  [OK] {user.username.ljust(15)} | Nota: {str(puntaje_final).zfill(5)} | Perfil: {perfil}')
                    total_exito += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [ERROR] Error procesando a {user.username}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\nFinalizado: {total_exito} estudiantes procesados con éxito.'))
