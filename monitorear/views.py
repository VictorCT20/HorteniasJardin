from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create your views here.
def es_admin(user):
    return user.is_staff  

@method_decorator(user_passes_test(es_admin, login_url='/accounts/login/'), name='dispatch')
class EncuestasMoniView(View): 
    def get(self, request, *args, **kwargs):
        calificaciones = Calificacion.objects.all()
        context={
            'calificaciones': calificaciones
        }
        return render(request, 'monitorear/Encuestas.html', context)

@method_decorator(user_passes_test(es_admin, login_url='/accounts/login/'), name='dispatch')
class VisitasMoniView(View): 
    def get(self, request, *args, **kwargs):
        visitas = Visitas.objects.all()
        context={
            'visitas': visitas
        }
        return render(request, 'monitorear/Visitas.html', context)

@method_decorator(user_passes_test(es_admin, login_url='/accounts/login/'), name='dispatch')
class VentasMoniView(View): 
    def get(self, request, *args, **kwargs):
        ventas = Venta.objects.all()
        reservas = Reserva.objects.all()
        context={
            'ventas': ventas,
            'reservas': reservas
        }
        return render(request, 'monitorear/Ventas.html', context)

    def post(self, request, *args, **kwargs):  
        print("a ver")
        action = request.POST.get('action')
        reserva_id = request.POST.get('reserva_id')
        reserva = get_object_or_404(Reserva, id=reserva_id)
        if action == 'Realizado':
            nueva_venta = Venta(
                cantidad=reserva.cantidad,
                planta=reserva.planta,
                visita=reserva.visita,
            )
            nueva_venta.save()
            reserva.delete()
            return redirect('monitorear:moventa')
        elif action == 'Cancelado':
            reserva.delete()
            return redirect('monitorear:moventa')

