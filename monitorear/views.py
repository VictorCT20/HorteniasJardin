from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Usuario
# Create your views here.

class UserEntryView(View):
    def get(self, request, *args, **kwargs):
        context={
        } 
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
            context={
                'usuario_id':usuario_id
            }
            return redirect('ar', context)

        context={
        }
        return render(request, 'interfaceUser.html', context)
