from django.core.management.base import BaseCommand
from AppEvaluar.models import Ejercicio
from AppEvaluar.services_ia_logic import generar_representacion_formal
import time

class Command(BaseCommand):
    help = 'Genera representaciones lógicas JSON para todos los ejercicios existentes que no las tengan.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Sobreescribir metadatos existentes')
        parser.add_argument('--limit', type=int, help='Número máximo de ejercicios a procesar')

    def handle(self, *args, **options):
        ejercicios = Ejercicio.objects.all()
        if not options['force']:
            ejercicios = ejercicios.filter(meta_geometria__isnull=True)

        if options['limit']:
            ejercicios = ejercicios[:options['limit']]

        self.stdout.write(f"Procesando {ejercicios.count()} ejercicios...")

        exitos = 0
        errores = 0

        for ej in ejercicios:
            self.stdout.write(f"Enriqueciendo ejercicio ID {ej.id}...")
            
            intentos = 0
            max_intentos = 3
            exito_ejercicio = False
            espera = 10
            
            while intentos < max_intentos and not exito_ejercicio:
                try:
                    res = generar_representacion_formal(ej)
                    if res:
                        ej.meta_geometria = res
                        ej.save()
                        exitos += 1
                        self.stdout.write(self.style.SUCCESS(f"Éxito: ID {ej.id}"))
                        exito_ejercicio = True
                    else:
                        raise ValueError("La API devolvió una respuesta vacía o no válida.")
                except Exception as e:
                    intentos += 1
                    error_msg = str(e)
                    self.stdout.write(self.style.WARNING(f"Fallo para ID {ej.id}: {error_msg}"))
                    
                    if intentos < max_intentos:
                        self.stdout.write(f"Reintentando en {espera}s (Intento {intentos}/{max_intentos})...")
                        time.sleep(espera)
                        espera *= 2  # Retroceso exponencial inteligente
                    else:
                        errores += 1
                        self.stdout.write(self.style.ERROR(f"Fallo definitivo: ID {ej.id} tras {max_intentos} intentos."))
            
            # Pausa base para respetar los límites de la API
            time.sleep(2)

        self.stdout.write(self.style.SUCCESS(f"Finalizado. Éxitos: {exitos}, Errores: {errores}"))
