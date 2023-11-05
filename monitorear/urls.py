from django.contrib import admin
from django.urls import path, include   
from .views import EncuestasMoniView, VisitasMoniView, VentasMoniView

app_name="monitorear"

urlpatterns = [
    path('encuestas/', EncuestasMoniView.as_view(), name="moencuesta"),
    path('ventas/', VentasMoniView.as_view(), name="moventa"),
    path('visitas/', VisitasMoniView.as_view(), name="movisita"),
]