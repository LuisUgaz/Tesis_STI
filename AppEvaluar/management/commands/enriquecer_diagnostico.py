from django.core.management.base import BaseCommand
from AppEvaluar.models import RespuestaUsuario
from AppEvaluar.services import obtener_feedback_ia
import time

class Command(BaseCommand):
    help = 'Genera explicaciones pedagógicas de la IA para las respuestas del examen diagnóstico que no las tengan.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Sobreescribir feedback de IA existente')
        parser.add_argument('--limit', type=int, help='Número máximo de respuestas a procesar')

    def handle(self, *args, **options):
        # Filtrar respuestas que pertenecen a preguntas de un ExamenDiagnostico
        respuestas = RespuestaUsuario.objects.filter(pregunta__examen__isnull=False)

        if not options['force']:
            # Filtrar las respuestas que aún no tengan feedback generado
            respuestas = respuestas.filter(feedback_ia__isnull=True) | respuestas.filter(feedback_ia="")

        # Evitar duplicados por la unión y ordenar
        respuestas = respuestas.distinct().order_by('id')

        if options['limit']:
            respuestas = respuestas[:options['limit']]

        total_respuestas = respuestas.count()
        self.stdout.write(f"Procesando {total_respuestas} respuestas de examen diagnóstico...")

        if total_respuestas == 0:
            self.stdout.write(self.style.SUCCESS("No hay respuestas por enriquecer."))
            return

        exitos = 0
        errores = 0

        for resp in respuestas:
            self.stdout.write(f"Enriqueciendo respuesta ID {resp.id} (Pregunta: {resp.pregunta.id})...")
            
            intentos = 0
            max_intentos = 3
            exito_respuesta = False
            espera = 5
            
            while intentos < max_intentos and not exito_respuesta:
                try:
                    # En obtener_feedback_ia se llamará a Gemini y se persistirá si es exitoso
                    if options['force']:
                        # Si es forzado, limpiamos el feedback previo para obligar a regenerar
                        resp.feedback_ia = None
                        resp.save(update_fields=['feedback_ia'])
                    
                    res = obtener_feedback_ia(resp)
                    # Si no falló con el mensaje por defecto de error
                    if res and "No se pudo generar la explicacion IA" not in res and "Configuración de IA incompleta" not in res:
                        exitos += 1
                        self.stdout.write(self.style.SUCCESS(f"Éxito: ID {resp.id}"))
                        exito_respuesta = True
                    else:
                        raise ValueError(f"La API de IA no pudo generar un feedback válido: {res}")
                except Exception as e:
                    intentos += 1
                    error_msg = str(e)
                    self.stdout.write(self.style.WARNING(f"Fallo para ID {resp.id}: {error_msg}"))
                    
                    if intentos < max_intentos:
                        self.stdout.write(f"Reintentando en {espera}s (Intento {intentos}/{max_intentos})...")
                        time.sleep(espera)
                        espera *= 2  # Retroceso exponencial
                    else:
                        errores += 1
                        self.stdout.write(self.style.ERROR(f"Fallo definitivo: ID {resp.id} tras {max_intentos} intentos."))
            
            # Pausa base para respetar los límites de cuota de la API
            time.sleep(1.5)

        self.stdout.write(self.style.SUCCESS(f"Finalizado. Éxitos: {exitos}, Errores: {errores}"))
