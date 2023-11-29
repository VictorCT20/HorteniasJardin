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

