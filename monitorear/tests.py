from django.test import TestCase
from django.test import RequestFactory
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from monitorear.models import *
from django.test import TestCase, Client
import unittest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from django.test import LiveServerTestCase
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
        self.assertRedirects(response, '/')  # Ajusta esto según la URL a la que debería redirigir

        # Verificar que la vista es accesible después del inicio de sesión
        response_after_login = self.client.get(reverse('Home'))
        self.assertEqual(response_after_login.status_code, 200) 

class UserRegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cuenta = Cuenta.objects.create_user(username='user', password='usuario2023')
        self.client.login(username='user', password='usuario2023')
    
    def test_get_success(self):
      
        response = self.client.get(reverse('userEntry'))
        
        self.assertEquals(response.status_code, 200)

    def test_valid_post(self):
        url = reverse('userEntry')
        data = {
            'name': 'Juan',
            'apellido': 'Perez' 
        }
        
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('ar'))
        
        # Verificar usuario creado
        self.assertTrue(Usuario.objects.filter(name='Juan').exists()) 

class TestMyWebPage(unittest.TestCase):
    def setUp(self):
        # Configurar el driver de Selenium (asegúrate de tener el controlador en tu PATH)
        self.driver = webdriver.Chrome()

    def tearDown(self):
        # Cerrar el navegador al finalizar la prueba
        self.driver.close()

    def test_validar_formulario(self):
        # Abrir la página web
        self.driver.get("http://jardinhorten.onrender.com/registro")

        # Encontrar el campo de comentario y enviar datos inválidos
        comentario_input = self.driver.find_element_by_id("comentar")
        comentario_input.send_keys("Comentario con caracteres no permitidos #$%^")

        # Encontrar el botón de enviar y hacer clic
        submit_button = self.driver.find_element_by_xpath("//button[@class='submit']")
        submit_button.click()

        # Validar que se muestra la alerta de caracteres no permitidos
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, "El comentario no cumple con los requisitos.")
        alert.accept()

if __name__ == "__main__":
    unittest.main()
class CalificacionViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.cuenta = Cuenta.objects.create_user(username='user', password='usuario2023')
        self.client.login(username='user', password='usuario2023')
        # Crear un usuario de ejemplo
        self.usuario = Usuario.objects.create(id=1,name='Ejemplo', apellido='Usuario')
        
    def test_get_successCali(self):
      
        response = self.client.get(reverse('valorar'))
        
        self.assertEquals(response.status_code, 200)

    def test_creacion_calificacion(self):
        # Prueba de creación de calificación con un usuario existente
        response = self.client.post(reverse('valorar'), {'usuario_id': self.usuario.id, 'numero_estrellas': 4, 'comentar': '¡Gran experiencia!'})
        self.assertEqual(response.status_code, 302)  # Debería redirigir después de un POST exitoso
        self.assertRedirects(response, reverse('ar'))

        # Verificar que la calificación se ha creado
        calificacion = Calificacion.objects.get(usuario=self.usuario)
        self.assertIsNotNone(calificacion)
        self.assertEqual(calificacion.numeroEstrellas, 4)
        self.assertEqual(calificacion.comentario, '¡Gran experiencia!')

    def test_creacion_calificacion_con_comentario_no_permitido(self):
        # Prueba de creación de calificación con un comentario no permitido
        response = self.client.post(reverse('valorar'), {'usuario_id': self.usuario.id, 'numero_estrellas': 3, 'comentar': 'Comentario invalido!@#$'})
        self.assertEqual(response.status_code, 200)  # Debería permanecer en la misma página
        self.assertContains(response, 'El comentario no cumple con los requisitos.')

        # Verificar que la calificación no se ha creado con un comentario no permitido
        calificacion_invalida = Calificacion.objects.filter(usuario=self.usuario, numeroEstrellas=3, comentario='Comentario invalido!@#$')
        self.assertFalse(calificacion_invalida.exists())