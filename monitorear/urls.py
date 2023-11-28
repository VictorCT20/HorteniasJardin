from django.contrib import admin
from django.urls import path, include   
from .views import EncuestasMoniView, VisitasMoniView, VentasMoniView, FiltrarVisitasView, FiltrarCalificacionesView, FiltrarVentasView

app_name="monitorear"

urlpatterns = [
    path('encuestas/', EncuestasMoniView.as_view(), name="moencuesta"),
    path('ventas/', VentasMoniView.as_view(), name="moventa"),
    path('visitas/', VisitasMoniView.as_view(), name="movisita"),
    path('filtrar_visitas/', FiltrarVisitasView.as_view(), name='filtrar_visitas'),
    path('filtrar_visitas/<fecha>/', FiltrarVisitasView.as_view(), name='filtrar_visitas'),
    path('filtrar_calificaciones/', FiltrarCalificacionesView.as_view(), name='filtrar_calificaciones'),
    path('filtrar_calificaciones/<fecha>/', FiltrarCalificacionesView.as_view(), name='filtrar_calificaciones'),
    path('filtrar_ventas/', FiltrarVentasView.as_view(), name='filtrar_ventas'),
    path('filtrar_ventas/<fecha>/', FiltrarVentasView.as_view(), name='filtrar_ventas'),
]