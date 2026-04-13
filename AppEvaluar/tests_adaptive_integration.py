from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, OpcionEjercicio, ResultadoEjercicio, ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, RecomendacionEstudiante, ResultadoDiagnostico
from AppEvaluar.services import calcular_recomendacion

class AdaptiveIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alumno_pro', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante', nivel_dificultad_actual='Básico', grado='2do', seccion='A')
        self.tema = Tema.objects.create(nombre="Ángulos", slug="angulos")
        
        # 1. Crear examen diagnóstico
        self.examen = ExamenDiagnostico.objects.create(nombre="D1")
        self.p1 = Pregunta.objects.create(examen=self.examen, texto="P1", categoria="Ángulos", tipo='OPCION_MULTIPLE')
        self.oc1 = Opcion.objects.create(pregunta=self.p1, texto="Correcta", es_correcta=True)
        
        # 2. Crear ejercicios de niveles diferentes
        self.e_basico = Ejercicio.objects.create(tema=self.tema, texto="E Básico", dificultad='Básico')
        OpcionEjercicio.objects.create(ejercicio=self.e_basico, texto="O1", es_correcta=True)
        
        self.e_intermedio = Ejercicio.objects.create(tema=self.tema, texto="E Intermedio", dificultad='Intermedio')
        self.oi1 = OpcionEjercicio.objects.create(ejercicio=self.e_intermedio, texto="O1", es_correcta=True)

    def test_full_adaptive_flow(self):
        """Flujo: Diagnóstico -> Nivel Inicial -> Práctica exitosa -> Cambio de Nivel."""
        self.client.login(username='alumno_pro', password='password123')
        
        # --- PASO 1: Rendir diagnóstico con 100% ---
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1, opcion_seleccionada=self.oc1)
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=100)
        
        # El servicio se llama normalmente tras el POST del examen
        calcular_recomendacion(self.user)
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.nivel_dificultad_actual, 'Avanzado') # 100% -> Avanzado
        
        # Forzar nivel a Básico para probar la subida tras práctica
        self.profile.nivel_dificultad_actual = 'Básico'
        self.profile.save()
        
        # --- PASO 2: Iniciar práctica (debe cargar el ejercicio básico) ---
        response = self.client.get(reverse('iniciar_practica'))
        self.assertContains(response, "E Básico")
        
        # --- PASO 3: Resolver 5 ejercicios con éxito (simulamos 5 resultados) ---
        for i in range(5):
            e = Ejercicio.objects.create(tema=self.tema, texto=f"Ex {i}", dificultad='Básico')
            op = OpcionEjercicio.objects.create(ejercicio=e, texto="C", es_correcta=True)
            
            self.client.post(reverse('validar_respuesta'), {
                'ejercicio_id': e.id,
                'opcion_id': op.id,
                'tiempo': 5
            })
            
        # --- PASO 4: Verificar cambio a Intermedio ---
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.nivel_dificultad_actual, 'Intermedio')
        
        # --- PASO 5: La siguiente práctica debe cargar el intermedio ---
        response2 = self.client.get(reverse('iniciar_practica'))
        self.assertContains(response2, "E Intermedio")
