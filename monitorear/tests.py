from django.test import TestCase
from django.test import RequestFactory
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from monitorear.models import *
from django.test import TestCase, Client
import unittest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
import pytest
import datetime
from core.views import EncuestaView


def es_admin(user):
    return user.is_admin

@pytest.mark.django_db  
def test_login_form():

    client = Client()  
    url = reverse('login')
    
    response = client.get(url)
    assert response.status_code == 200

    # Verificar campos formulario
    
    data = {'username': 'foo', 'password': 'bar'}
    response = client.post(url, data)
    assert response.status_code == 200

    # Crear cuenta de prueba
    user = Cuenta.objects.create_user('test', 'test@test.com', 'pwd')
    
    data = {'username': 'test', 'password': 'pwd'}
    response = client.post(url, data, follow=True)
  
    assert response.redirect_chain == [('http://testserver/visitas/', 302)]

    

class UsuarioTest(TestCase):
    def test_str_representation(self):
        usuario = Usuario(name="Juan", apellido="Pérez")
        self.assertEqual(str(usuario), "Juan Pérez")

class CalificacionTest(TestCase):
    def test_str_representation(self):
        usuario = Usuario(name="Juan", apellido="Pérez")
        calificacion = Calificacion(numeroEstrellas=5, comentario="Excelente servicio", usuario=usuario)
        self.assertEqual(str(calificacion), "Calificación de Juan")

class VisitasTest(TestCase):
    def test_str_representation(self):
        usuario = Usuario(name="Juan", apellido="Pérez")
        visita = Visitas(fecha=datetime.datetime(2023, 11, 28), usuario=usuario)
        self.assertEqual(str(visita), "Visita de Juan Pérez el 2023-11-28 00:00:00")

class PlantaTest(TestCase):
    def test_str_representation(self):
        planta = Planta(nombrePlanta="Hortensia", nombreEspecie="Hydrangea macrophylla", tiempoVida="Perenne")
        self.assertEqual(str(planta), "Nombre de la planta: Hortensia, Especie: Hydrangea macrophylla, Tiempo de vida: Perenne")

class ReservaTest(TestCase):
    def test_str_representation(self):
        usuario = Usuario(name="Juan", apellido="Pérez")
        planta = Planta(nombrePlanta="Hortensia", nombreEspecie="Hydrangea macrophylla")
        visita = Visitas(fecha=datetime.datetime(2023, 11, 28), usuario=usuario)
        reserva = Reserva(cantidad=2, planta=planta, visita=visita)
        self.assertEqual(str(reserva), "2 de Hortensia en reserva de Juan")

class VentaTest(TestCase):
    def test_str_representation(self):
        usuario = Usuario(name="Juan", apellido="Pérez")
        planta = Planta(nombrePlanta="Hortensia", nombreEspecie="Hydrangea macrophylla")
        visita = Visitas(fecha=datetime.datetime(2023, 11, 28), usuario=usuario)
        venta = Venta(cantidad=2, planta=planta, visita=visita)
        self.assertEqual(str(venta), "2 de Hortensia en reserva de Juan")


class EncuestaViewTest(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        # Create a custom user object
        user = Cuenta.objects.create_user('test_user', 'test@example.com', 'password')
        self.request = self.request_factory.get('/', user=user)
    def test_get_request(self):
        request = self.request_factory.get('/')
        response = EncuestaView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Estrellas.html')

    def test_post_request_valid_data(self):
        request = self.request_factory.post('/', {'usuario_id': 1, 'numero_estrellas': 5, 'comentar': 'Excelente servicio'})
        response = EncuestaView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/monitorear/visitas/', status_code=302)

    def test_post_request_invalid_data(self):
        request = self.request_factory.post('/', {'usuario_id': 1, 'numero_estrellas': 5, 'comentar': '!#$%&'})
        response = EncuestaView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Estrellas.html')

class EncuestaViewTest(TestCase):
    def setUp(self):
        # Configuración inicial de datos para las pruebas
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.usuario = Usuario.objects.create(name='Test', apellido='User')
        self.client = Client()

    def test_get_encuesta_view(self):
        user = Cuenta.objects.create_user('admin', 'Hortensias2023')  
        self.client.force_login(user)
        # Prueba para GET en la vista de encuesta
        response = self.client.get(reverse('valorar'), follow=True)
        self.assertEqual(response.status_code, 200)
        #print(response.content.decode())  # Imprime el contenido real de la respuesta
        self.assertContains(response, 'Calificación Estrella')

    def test_post_encuesta_view_valid(self):
        # Prueba para POST válido en la vista de encuesta
        self.client.force_login(self.user)  # Inicia sesión para simular un usuario autenticado
        data = {'usuario_id': self.usuario.id, 'numero_estrellas': 5, 'comentar': 'Buen trabajo'}
        response = self.client.post(reverse('valorar'), data)
        self.assertEqual(response.status_code, 302)  # Redireccionamiento después de enviar el formulario
        self.assertEqual(Calificacion.objects.count(), 1)  # Se espera que se haya creado una nueva calificación

    def test_post_encuesta_view_invalid(self):
    # Prueba para POST inválido en la vista de encuesta (comentario no válido)
        self.client.force_login(self.user)
        data = {'usuario_id': self.usuario.id, 'numero_estrellas': 3, 'comentar': '!@# Invalid Comment'}
        
        # Intenta enviar el formulario inválido
        response = self.client.post(reverse('valorar'), data)
        
        # Verifica que la página muestra el mensaje de error y no se ha creado ninguna calificación
        self.assertContains(response, 'El comentario no cumple con los requisitos.')
        self.assertEqual(Calificacion.objects.count(), 0)


class UserRegisterViewTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba para simular una sesión iniciada
        self.user = Cuenta.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_get_user_register_view(self):
        # Prueba para GET en la vista de registro de usuario
        user = Cuenta.objects.create_user('prueba', 'prueba2023')  
        self.client.force_login(user)
        response = self.client.get(reverse('userEntry'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'interfaceUser.html')

    def test_post_user_register_valid(self):
        # Prueba para POST válido en la vista de registro de usuario
        user = Cuenta.objects.create_user('prueba', 'prueba2023')  
        self.client.force_login(user)
        data = {'name': 'John', 'apellido': 'Cortez'}
        response = self.client.post(reverse('userEntry'), data)

        # Verifica que la redirección después de enviar el formulario muestra un mensaje de éxito.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Usuario.objects.count(), 1)  # Se espera que se haya creado un nuevo usuario

    def test_post_user_register_invalid(self):
        user = Cuenta.objects.create_user('prueba', 'prueba2023')
        self.client.force_login(user)

        # Prueba para POST inválido en la vista de registro de usuario (nombre/apellido no válidos)
        data = {'name': '123', 'apellido': '!@#'}
        response = self.client.post(reverse('userEntry'), data)  # No seguir la redirección

        # Verifica que la respuesta sea una redirección (código 302)
        self.assertEqual(response.status_code, 200)

        # Verifica que no se ha creado ningún usuario
        self.assertEqual(Usuario.objects.count(), 0)