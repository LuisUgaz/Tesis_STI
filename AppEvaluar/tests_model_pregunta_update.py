from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from AppTutoria.models import Tema
from AppEvaluar.models import Pregunta, ExamenDiagnostico

class PreguntaModelUpdateTests(TestCase):
    def setUp(self):
        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Test", tiempo_limite=30)
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")

    def test_pregunta_tiene_campos_nuevos(self):
        """Verifica que los nuevos campos tema y dificultad existan en el modelo."""
        pregunta = Pregunta.objects.create(
            examen=self.examen,
            texto="Test campos",
            tipo='OPCION_MULTIPLE',
            tema=self.tema,
            dificultad="Intermedio"
        )
        
        self.assertEqual(pregunta.tema, self.tema)
        self.assertEqual(pregunta.dificultad, "Intermedio")

    def test_pregunta_usa_foreign_key_tema(self):
        """Verifica que tema sea una relación con el modelo Tema."""
        pregunta = Pregunta.objects.create(
            examen=self.examen,
            texto="Test tema",
            tema=self.tema,
            dificultad="Básico"
        )
        self.assertEqual(pregunta.tema.nombre, "Triángulos")
