from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from monitorear.models import Usuario, Visitas, Calificacion, Cuenta
from datetime import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
import json

# Define la función de prueba para verificar si el usuario es administrador
def es_admin(user):
    return user.is_admin

class QrView(View): 
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, 'registration/qr.html', context)
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            data = json.loads(request.body)
            content = data['contenido_qr']
            print("content: " + content)
            if(content == 'usuario logeado para usar ar'):
                user = authenticate(username='user', password='Hortensias2023')
                login(request, user)
                print('es el qr correcto')

                return redirect('userEntry')
            else:
                print('no es el qr correcto') 

                return redirect('logqr')
            
        context={}
        return render(request, 'registration/qr.html', context) 

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, 'index.html', context)

class ArView(View):
    def get(self, request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')  # Obtiene el usuario_id de la variable de sesión
        
        # Obtiene la instancia del usuario correspondiente o muestra un error si no existe
        usuario = get_object_or_404(Usuario, id=usuario_id)
        # Verifica si ya existe una visita para este usuario
        existing_visita = Visitas.objects.filter(usuario=usuario).first()
        
        if not existing_visita:
            # No existe una visita, crea una nueva
            visita = Visitas(usuario=usuario, fecha=datetime.now())
            visita.save()
            visita_id = visita.id
        else: 
            visita = get_object_or_404(Visitas, usuario=usuario)
            visita_id = visita.id 
             
        context = {
            'usuario_id': usuario_id,
            'visita_id' : visita_id
        }

        return render(request, 'ar.html', context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        usuario_id = request.POST.get('usuario_id')
        visita_id = request.POST.get('visita_id')
        request.session['usuario_id'] = usuario_id
        request.session['visita_id'] = visita_id
        # Redirige a la vista apropiada según el botón presionado
        if action == 'EncuestaView':
            return redirect('valorar')
        elif action == 'vista_2':
            return redirect('vista_2')

@method_decorator(login_required, name='dispatch')
class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        print('a')
        context={ } 
        return render(request, 'interfaceUser.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST['name']
            apellido = request.POST['apellido']
            
            nuevo_usuario = Usuario(
                name=name,
                apellido=apellido
            )
            nuevo_usuario.save()
            usuario_id = nuevo_usuario.id
            # Pasa el ID como una variable de contexto en lugar de la URL
            request.session['usuario_id'] = usuario_id
            return redirect('ar')

        context={ }
        return render(request, 'interfaceUser.html', context)
        


class EncuestaView(View):
    def get(self, request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id') 
        context={
            'usuario_id':usuario_id
        } 
        return render(request, 'Estrellas.html', context) 
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            usuario_id = request.POST['usuario_id']
            numero_estrellas = request.POST['numero_estrellas']
            comentario = request.POST['comentar']
            usuario = get_object_or_404(Usuario, id=usuario_id) 

            # Crea una instancia de Calificacion y guárdala en la base de datos
            calificacion = Calificacion(
                numeroEstrellas=numero_estrellas, 
                comentario=comentario, 
                usuario=usuario) 
            calificacion.save()

            return redirect('ar')  

        context={ }
        return render(request, 'Estrellas.html', context)