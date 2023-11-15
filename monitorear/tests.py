from django.test import TestCase
from django.test import RequestFactory
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from monitorear.models import *
from django.test import TestCase, Client
import unittest
from django.contrib.auth.models import User
from django.urls import reverse

def es_admin(user):
    return user.is_admin
class LoginTest(TestCase):
    def setUp(self):
        # Configurar un cliente para realizar solicitudes HTTP
        self.client = Client()
        # Crear una instancia de Cuenta u otro modelo según sea necesario
        self.cuenta = Cuenta.objects.create_user(username='admin', password='Hortensias2023')
        self.client.login(username='admin', password='Hortensias2023')

    def test_login(self):
        # Simular una solicitud GET a la página de inicio de sesión
        response = self.client.get(reverse('login'))

        # Verificar que la página de inicio de sesión se carga correctamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log In')  # Ajusta esto según el contenido de tu página

        # Simular una solicitud POST con credenciales de inicio de sesión
        response = self.client.post(reverse('login'), {'username': 'admin', 'password': 'Hortensias2023'})

        # Verificar que el inicio de sesión fue exitoso
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        # Verificar que se redirige correctamente después de iniciar sesión
        self.assertRedirects(response, '/monitorear/visitas', status_code=302)  # Ajusta esto según la URL a la que debería redirigir

        # Verificar que la vista es accesible después del inicio de sesión
        response_after_login = self.client.get(reverse('monitorear:movisita'))
        self.assertEqual(response_after_login.status_code, 301) 

        # Limpia las sesiones después de la prueba
        self.client.session.flush()

class UserRegisterViewTest(TestCase):
    def setUpUser(self):
        self.client = Client()
        self.cuenta = Cuenta.objects.create_user(username='user', password='usuario2023')
        self.client.login(username='user', password='usuario2023')
    
    def test_get_success_user(self):
        response = self.client.get(reverse('userEntry'))
        self.assertEquals(response.status_code, 302)

    def test_valid_post_user(self):
        # Iniciar sesión antes de realizar la solicitud
        login_result = self.client.login(username='user', password='usuario2023')
        print(f"Login result: {login_result}")
        url = reverse('userEntry')
        data = {
            'name': 'Juan',
            'apellido': 'Perez' 
        }
        
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('ar'))
        
        # Verificar usuario creado
        self.assertTrue(Usuario.objects.filter(name='Juan').exists()) 
    def test_invalid_post_user(self):
        # Iniciar sesión antes de realizar la solicitud
        login_result = self.client.login(username='admin', password='Hortensias2023')
        print(f"Login result: {login_result}")
        url = reverse('userEntry')

        # Nombre inválido
        data = {
            'name': '12',
            'apellido': 'Perez'
        }

        response = self.client.post(reverse('userEntry'), data, follow=True)
        # Redirigir de nuevo al formulario de entrada de usuario
        self.assertRedirects(response, reverse('userEntry'))

        # Apellido inválido
        data = {
            'name': 'Juan',
            'apellido': '123'
        }

        response = self.client.post(reverse('userEntry'), data, follow=True)

        self.assertRedirects(response, reverse('userEntry'))

class CalificacionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cuenta = Cuenta.objects.create_user(username='user', password='usuario2023')
        self.client.login(username='user', password='usuario2023')
        self.usuario = Usuario.objects.create(name='John', apellido='Doe')

    def test_valid_calificacion_submission(self):
        url = reverse('valorar')
        data = {
            'usuario_id': self.usuario.id,
            'numero_estrellas': '5',
            'comentario': 'Buen servicio'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Debería redirigir a 'ar'

        # Verificar que la Calificacion se ha creado correctamente
        self.assertTrue(Calificacion.objects.filter(usuario=self.usuario, numeroEstrellas='5', comentario='Buen servicio').exists())

    def test_invalid_calificacion_submission(self):
        # Comentario con caracteres especiales
        data = {
            'usuario_id': self.usuario.id,
            'numero_estrellas': '3',
            'comentario': 'Mal servicio!@#$%^&*()'
        }

        response = self.client.post(reverse('valorar'), data, follow=True)
        # Redirigir de nuevo al formulario de calificación
        self.assertRedirects(response, reverse('valorar'))

        # Verificar que no se haya creado una calificación con información no válida
        self.assertFalse(Calificacion.objects.filter(usuario=self.usuario, numeroEstrellas='3', comentario='Mal servicio!@#$%^&*()').exists())
