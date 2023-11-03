from django.contrib import admin
from django.urls import path, include
from .views import HomeView, ArView, UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', HomeView.as_view(), name="Home"),
    path('monitorear/',include('monitorear.urls', namespace='monitorear')),
    path('ar/', ArView.as_view(), name="ar"),
    path('registro/', UserRegisterView.as_view(), name="userEntry"),
    path('valorar/', UserRegisterView.as_view(), name="valorar"),
]   
    