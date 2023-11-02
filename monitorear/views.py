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
            usuario_id = nuevo_usuario.id
            nuevo_usuario.save()
            return redirect('ar', usuario_id=usuario_id)

        context={
        }
        return render(request, 'interfaceUser.html', context)
