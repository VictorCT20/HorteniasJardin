from django.views.generic import View
from django.shortcuts import render, redirect
from monitorear.models import Usuario

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={

        }
        return render(request, 'index.html', context)

class ArView(View):
    def get(self, request, *args, **kwargs):
        usuario_id = request.GET.get('usuario_id')  # Obtiene el ID del usuario desde la URL
        context = {
            'usuario_id': usuario_id
        }
        return render(request, 'ar.html', context)

class UserRegisterView(View):
    def get(self, request, *args, **kwargs):
        context={

        }
        return render(request, 'ar.html', context)