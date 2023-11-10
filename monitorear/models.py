from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Permission, Group

# Create your models here.
class Cuenta(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='cuentas')
    is_admin = models.BooleanField(default=False)
    user_permissions = models.ManyToManyField(Permission, related_name='cuentas_permissions')
    class Meta:
        permissions = [
            ('permiso_admin', 'Permisos de administrador')
        ]
    def __str__(self):
        return self.username
class Usuario(models.Model):
    name = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name} {self.apellido}"
class Calificacion(models.Model):
    numeroEstrellas = models.IntegerField()
    comentario = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"Calificación de {self.usuario.name}"
class Visitas(models.Model):
    fecha = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"Visita de {self.usuario} el {self.fecha}"
class Planta(models.Model):
    nombrePlanta = models.CharField(max_length=50)
    nombreEspecie = models.CharField(max_length=50)
    origen = models.CharField(max_length=70)
    tiempoVida = models.CharField(max_length=70)
    propiedades = models.TextField()
    detalle = models.TextField()
    curiosidad = models.TextField()
    condicionAmbiental = models.TextField()
    def __str__(self):
        return f"Nombre de la planta: {self.nombrePlanta}, Especie: {self.nombreEspecie}, Tiempo de vida: {self.tiempoVida}"

class Reserva(models.Model):
    cantidad = models.IntegerField()
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    visita = models.ForeignKey(Visitas, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.cantidad} de {self.planta.nombrePlanta} en reserva de {self.visita.usuario.name}"

class Venta(models.Model):
    cantidad = models.IntegerField()
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    visita = models.ForeignKey(Visitas, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.cantidad} de {self.planta.nombrePlanta} en reserva de {self.visita.usuario.name}"
