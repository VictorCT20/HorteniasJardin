from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models.functions import Cast
from django.db.models import DateTimeField
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from datetime import datetime, timedelta

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

class FiltrarCalificacionesView(View):
    def get(self, request, *args, **kwargs):
        try:
            fecha = request.GET.get('fecha')
            
            # Verifica si la fecha es None o una cadena vacía
            if fecha:
                # Convierte la cadena de fecha a un objeto datetime
                fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d')

                # Filtra las visitas para la fecha específica y obtén los IDs de los usuarios
                usuarios_ids = Visitas.objects.filter(
                    fecha__gte=fecha_datetime,
                    fecha__lt=fecha_datetime + timedelta(days=1)
                ).values_list('usuario', flat=True)
                

                # Filtra las calificaciones para los usuarios obtenidos
                calificaciones_filtradas = Calificacion.objects.filter(usuario__id__in=usuarios_ids)

                # Renderiza solo el fragmento necesario de la página
                data = render_to_string('monitorear/calificaciones_table.html', {'calificaciones': calificaciones_filtradas})

                # Devuelve la respuesta como HTML
                return HttpResponse(data)
            else:
                # Si la fecha es None, devolver una respuesta indicando que no se proporcionó una fecha
                return JsonResponse({'error': 'No se proporcionó una fecha'}, status=400)
        except Exception as e:
            # Registra detalles del error
            print(f"Error en FiltrarCalificacionesView: {e}")
            # Devuelve una respuesta de error al cliente
            return JsonResponse({'error': 'Ocurrió un error al procesar la solicitud'}, status=500)
        

@method_decorator(user_passes_test(es_admin, login_url='/accounts/login/'), name='dispatch')
class VisitasMoniView(View): 
    def get(self, request, *args, **kwargs):
        visitas = Visitas.objects.all()
        context={
            'visitas': visitas
        }
        return render(request, 'monitorear/Visitas.html', context)

@method_decorator(user_passes_test(es_admin, login_url='/accounts/login/'), name='dispatch')
class FiltrarVisitasView(View):
    def get(self, request, *args, **kwargs):
        try:
            fecha = request.GET.get('fecha')
            
            # Verifica si la fecha es None o una cadena vacía
            if fecha:
                # Convierte la cadena de fecha a un objeto datetime
                fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d')
                # Filtra las visitas para el rango de un día
                visitas_filtradas = Visitas.objects.filter(
                    fecha__gte=fecha_datetime,
                    fecha__lt=fecha_datetime + timedelta(days=1)
                )

                # Renderiza solo el fragmento necesario de la página
                data = render_to_string('monitorear/visitas_table.html', {'visitas': visitas_filtradas})

                # Devuelve la respuesta como HTML
                return HttpResponse(data)
            else:
                # Si la fecha es None, devolver una respuesta indicando que no se proporcionó una fecha
                return JsonResponse({'error': 'No se proporcionó una fecha'}, status=400)
        except Exception as e:
            # Registra detalles del error
            print(f"Error en FiltrarVisitasView: {e}")
            # Devuelve una respuesta de error al cliente
            return JsonResponse({'error': 'Ocurrió un error al procesar la solicitud'}, status=500)


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

@method_decorator(user_passes_test(es_admin, login_url='/accounts/login/'), name='dispatch')
class FiltrarVentasView(View):
    def get(self, request, *args, **kwargs):
        try:
            fecha = request.GET.get('fecha')
            
            # Verifica si la fecha es None o una cadena vacía
            if fecha:
                # Convierte la cadena de fecha a un objeto datetime
                fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d')

                # Obtén las visitas para la fecha específica
                visitas = Visitas.objects.filter(
                    fecha__gte=fecha_datetime,
                    fecha__lt=fecha_datetime + timedelta(days=1)
                )

                # Obtén los IDs de las visitas
                visita_ids = visitas.values_list('id', flat=True)

                # Filtra las ventas para los visita_id obtenidos
                ventas_filtradas = Venta.objects.filter(visita__id__in=visita_ids)

                # Renderiza solo el fragmento necesario de la página
                data = render_to_string('monitorear/ventas_table.html', {'ventas': ventas_filtradas})

                # Devuelve la respuesta como HTML
                return HttpResponse(data)
            else:
                # Si la fecha es None, devolver una respuesta indicando que no se proporcionó una fecha
                return JsonResponse({'error': 'No se proporcionó una fecha'}, status=400)
        except Exception as e:
            # Registra detalles del error
            print(f"Error en FiltrarVentasView: {e}")
            # Devuelve una respuesta de error al cliente
            return JsonResponse({'error': 'Ocurrió un error al procesar la solicitud'}, status=500)
