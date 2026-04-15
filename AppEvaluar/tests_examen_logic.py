from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppEvaluar.models import Examen, Pregunta, ExamenDiagnostico
from AppEvaluar.services import asignar_preguntas_aleatorias

class ExamenLogicTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Geometría Plana")
        # Crear 10 preguntas para el tema
        for i in range(10):
            Pregunta.objects.create(
                texto=f"Pregunta {i}",
                tema=self.tema,
                dificultad="Básico"
            )
        
        self.otro_tema = Tema.objects.create(nombre="Trigonometría")
        Pregunta.objects.create(
            texto="Pregunta de otro tema",
            tema=self.otro_tema,
            dificultad="Básico"
        )

    def test_asignacion_exitosa(self):
        """Verificar que se asignan la cantidad correcta de preguntas del tema."""
        examen = Examen.objects.create(
            nombre="Examen Test",
            tema=self.tema,
            cantidad_preguntas=5,
            tiempo_limite=30
        )
        asignar_preguntas_aleatorias(examen)
        
        self.assertEqual(examen.preguntas.count(), 5)
        for pregunta in examen.preguntas.all():
            self.assertEqual(pregunta.tema, self.tema)

    def test_preguntas_ya_asignadas_no_se_reutilizan(self):
        """Verificar que preguntas en otro examen no se asignan al nuevo."""
        examen1 = Examen.objects.create(
            nombre="Examen 1",
            tema=self.tema,
            cantidad_preguntas=8,
            tiempo_limite=30
        )
        asignar_preguntas_aleatorias(examen1)
        
        # Intentar crear otro examen con 5 preguntas (solo quedan 2 disponibles)
        examen2 = Examen.objects.create(
            nombre="Examen 2",
            tema=self.tema,
            cantidad_preguntas=5,
            tiempo_limite=30
        )
        with self.assertRaises(ValueError):
            asignar_preguntas_aleatorias(examen2)

    def test_preguntas_diagnostico_no_se_reutilizan(self):
        """Verificar que preguntas de ExamenDiagnostico no se asignan."""
        diagnostico = ExamenDiagnostico.objects.create(nombre="Diagnostico")
        pregunta_diag = Pregunta.objects.get(texto="Pregunta 0")
        pregunta_diag.examen = diagnostico
        pregunta_diag.save()
        
        # Hay 10 preguntas en total, 1 es de diagnóstico, quedan 9.
        # Intentar pedir 10 preguntas debería fallar.
        examen = Examen.objects.create(
            nombre="Examen Fallido",
            tema=self.tema,
            cantidad_preguntas=10,
            tiempo_limite=30
        )
        with self.assertRaises(ValueError):
            asignar_preguntas_aleatorias(examen)

    def test_liberacion_preguntas_al_eliminar(self):
        """Verificar que las preguntas quedan disponibles al eliminar el examen."""
        examen = Examen.objects.create(
            nombre="Examen a eliminar",
            tema=self.tema,
            cantidad_preguntas=5,
            tiempo_limite=30
        )
        asignar_preguntas_aleatorias(examen)
        preguntas_ids = list(examen.preguntas.values_list('id', flat=True))
        
        examen.delete()
        
        # Verificar que las preguntas ahora tienen examen_tema = None
        for p_id in preguntas_ids:
            pregunta = Pregunta.objects.get(id=p_id)
            self.assertIsNone(pregunta.examen_tema)
