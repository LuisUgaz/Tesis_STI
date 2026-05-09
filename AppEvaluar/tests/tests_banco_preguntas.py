from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, OpcionEjercicio, RecomendacionEstudiante

class BancoPreguntasTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.docente_user = User.objects.create_user(username='docente1', password='password123')
        self.docente_profile = Profile.objects.create(user=self.docente_user, rol='Docente')
        
        self.estudiante_user = User.objects.create_user(username='estudiante1', password='password123')
        self.estudiante_profile = Profile.objects.create(user=self.estudiante_user, rol='Estudiante', grado='2do', seccion='A')
        
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        try:
            self.url_create = reverse('evaluar:banco_preguntas_create')
            self.url_list = reverse('evaluar:banco_preguntas_list')
        except:
            self.url_create = '/evaluar/banco-preguntas/nuevo/'
            self.url_list = '/evaluar/banco-preguntas/'

    def test_eliminacion_logica_ejercicio(self):
        """Debe marcar un ejercicio como inactivo en lugar de borrarlo físicamente."""
        ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Para eliminar", dificultad="Básico")
        try:
            url_delete = reverse('evaluar:banco_preguntas_delete', kwargs={'pk': ejercicio.pk})
        except:
            url_delete = f'/evaluar/banco-preguntas/eliminar/{ejercicio.pk}/'

        self.client.login(username='docente1', password='password123')
        
        # Al ser un POST (o DELETE simulado con POST para CBV DeleteView con confirmación)
        response = self.client.post(url_delete)
        self.assertEqual(response.status_code, 302) # Redirección tras éxito

        ejercicio.refresh_from_db()
        self.assertFalse(ejercicio.es_activo)
        # Verificar que el registro sigue existiendo en DB
        self.assertTrue(Ejercicio.objects.filter(id=ejercicio.id).exists())

    def test_preguntas_inactivas_no_aparecen_en_listado_docente(self):
        """El listado de gestión debe mostrar solo ejercicios activos por defecto."""
        Ejercicio.objects.create(tema=self.tema, texto="Activo", es_activo=True)
        Ejercicio.objects.create(tema=self.tema, texto="Inactivo", es_activo=False)

        self.client.login(username='docente1', password='password123')
        response = self.client.get(self.url_list)
        
        self.assertContains(response, "Activo")
        self.assertNotContains(response, "Inactivo")

    def test_preguntas_inactivas_no_aparecen_en_practica_estudiante(self):
        """Los estudiantes no deben recibir preguntas inactivas en sus sesiones de práctica."""
        # 1. Preparar recomendación para el estudiante
        RecomendacionEstudiante.objects.create(
            usuario=self.estudiante_user, 
            tema=self.tema.nombre, 
            metrica_desempeno=50
        )
        
        # 2. Crear una activa y una inactiva
        Ejercicio.objects.create(tema=self.tema, texto="Pregunta Activa", es_activo=True, dificultad="Básico")
        Ejercicio.objects.create(tema=self.tema, texto="Pregunta Inactiva", es_activo=False, dificultad="Básico")

        self.client.login(username='estudiante1', password='password123')
        url_practica = reverse('evaluar:iniciar_practica')
        
        response = self.client.get(url_practica)
        self.assertContains(response, "Pregunta Activa")
        self.assertNotContains(response, "Pregunta Inactiva")

    def test_acceso_eliminacion_restringido_a_docentes(self):
        """Un estudiante no debe poder eliminar (desactivar) preguntas."""
        ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Prohibido borrar", dificultad="Básico")
        try:
            url_delete = reverse('evaluar:banco_preguntas_delete', kwargs={'pk': ejercicio.pk})
        except:
            url_delete = f'/evaluar/banco-preguntas/eliminar/{ejercicio.pk}/'

        self.client.login(username='estudiante1', password='password123')
        response = self.client.post(url_delete)
        self.assertEqual(response.status_code, 403)
        
        ejercicio.refresh_from_db()
        self.assertTrue(ejercicio.es_activo)

    def test_acceso_restringido_a_docentes(self):
        """Solo los docentes deben poder acceder al formulario de creación de preguntas."""
        # Estudiante no debe tener acceso (403 Prohibido)
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 403)
        
        # Docente debe tener acceso (200 OK)
        self.client.login(username='docente1', password='password123')
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)

    def test_acceso_listado_restringido_a_docentes(self):
        """Solo los docentes deben poder acceder al listado de gestión del banco."""
        # Estudiante no debe tener acceso (403 Prohibido)
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 403)
        
        # Docente debe tener acceso (200 OK)
        self.client.login(username='docente1', password='password123')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)

    def test_validacion_campos_obligatorios(self):
        """El formulario debe validar que todos los campos requeridos estén presentes."""
        self.client.login(username='docente1', password='password123')
        response = self.client.post(self.url_create, {}) # Envío vacío
        # En la fase roja, esperamos que falle porque la URL o vista no existen
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFormError(form, 'texto', 'Este campo es obligatorio.')
        self.assertFormError(form, 'tema', 'Este campo es obligatorio.')

    def test_registro_exitoso_pregunta_con_opciones(self):
        """Debe guardar correctamente un ejercicio con sus 5 opciones vinculadas."""
        self.client.login(username='docente1', password='password123')
        
        data = {
            'texto': '¿Cuál es la suma de los ángulos internos de un triángulo?',
            'tema': self.tema.id,
            'dificultad': 'Básico',
            'explicacion_tecnica': 'La suma siempre es 180 grados.',
            # Opciones (InlineFormSet) - Prefijo 'opciones'
            'opciones-TOTAL_FORMS': '5',
            'opciones-INITIAL_FORMS': '0',
            'opciones-MIN_NUM_FORMS': '5',
            'opciones-MAX_NUM_FORMS': '5',
            
            'opciones-0-texto': '180',
            'opciones-0-es_correcta': True,
            'opciones-1-texto': '90',
            'opciones-1-es_correcta': False,
            'opciones-2-texto': '360',
            'opciones-2-es_correcta': False,
            'opciones-3-texto': '270',
            'opciones-3-es_correcta': False,
            'opciones-4-texto': '100',
            'opciones-4-es_correcta': False,
        }
        
        response = self.client.post(self.url_create, data)
        self.assertEqual(response.status_code, 302)
        
        ejercicio = Ejercicio.objects.get(texto=data['texto'])
        self.assertEqual(ejercicio.tema, self.tema)
        
        opciones = OpcionEjercicio.objects.filter(ejercicio=ejercicio)
        self.assertEqual(opciones.count(), 5)
        self.assertTrue(opciones.get(texto='180').es_correcta)

    def test_edicion_existosa_pregunta_y_opciones(self):
        """Debe actualizar correctamente un ejercicio y sus opciones existentes."""
        # 1. Crear un ejercicio previo
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="Texto original",
            dificultad="Básico"
        )
        opciones_objs = []
        for i in range(5):
            opciones_objs.append(OpcionEjercicio.objects.create(
                ejercicio=ejercicio,
                texto=f"Opción original {i}",
                es_correcta=(i == 0)
            ))

        try:
            url_edit = reverse('evaluar:banco_preguntas_edit', kwargs={'pk': ejercicio.pk})
        except:
            url_edit = f'/evaluar/banco-preguntas/editar/{ejercicio.pk}/'

        self.client.login(username='docente1', password='password123')
        
        # 2. Carga inicial del formulario de edición
        response = self.client.get(url_edit)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].instance, ejercicio)
        
        # 3. Envío de cambios
        data = {
            'texto': 'Texto editado',
            'tema': self.tema.id,
            'dificultad': 'Intermedio',
            'explicacion_tecnica': 'Explicación editada',
            # Opciones (InlineFormSet)
            'opciones-TOTAL_FORMS': '5',
            'opciones-INITIAL_FORMS': '5',
            'opciones-MIN_NUM_FORMS': '5',
            'opciones-MAX_NUM_FORMS': '5',
        }
        # Añadir datos de cada opción (editando la primera y la segunda)
        for i in range(5):
            data[f'opciones-{i}-id'] = opciones_objs[i].id
            data[f'opciones-{i}-ejercicio'] = ejercicio.id
            if i == 0:
                data[f'opciones-{i}-texto'] = 'Opción 1 editada'
                data[f'opciones-{i}-es_correcta'] = False
            elif i == 1:
                data[f'opciones-{i}-texto'] = 'Opción 2 editada (Ahora correcta)'
                data[f'opciones-{i}-es_correcta'] = True
            else:
                data[f'opciones-{i}-texto'] = opciones_objs[i].texto
                data[f'opciones-{i}-es_correcta'] = opciones_objs[i].es_correcta

        response = self.client.post(url_edit, data)
        self.assertEqual(response.status_code, 302) # Redirección tras éxito

        # 4. Verificar persistencia
        ejercicio.refresh_from_db()
        self.assertEqual(ejercicio.texto, 'Texto editado')
        self.assertEqual(ejercicio.dificultad, 'Intermedio')
        
        self.assertEqual(ejercicio.opciones.count(), 5)
        opc1 = ejercicio.opciones.get(id=opciones_objs[0].id)
        self.assertEqual(opc1.texto, 'Opción 1 editada')
        self.assertFalse(opc1.es_correcta)
        
        opc2 = ejercicio.opciones.get(id=opciones_objs[1].id)
        self.assertEqual(opc2.texto, 'Opción 2 editada (Ahora correcta)')
        self.assertTrue(opc2.es_correcta)

