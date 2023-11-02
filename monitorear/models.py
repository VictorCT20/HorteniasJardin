from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Cuenta(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        # Hasheamos la contraseña antes de guardarla
        self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
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
class Reserva(models.Model):
    visita = models.ForeignKey(Visitas, on_delete=models.CASCADE)
    def __str__(self):
        return f"Reserva de {self.visita.usuario.name}"
class Planta(models.Model):
    nombrePlanta = models.CharField(max_length=50)
    nombreEspecie = models.CharField(max_length=50)
    tiempoVida = models.CharField(max_length=70)
    Imagen = models.CharField(max_length=100)
    propiedades = models.TextField()
    detalle = models.TextField()
    curiosidad = models.TextField()
    propiedades = models.TextField()
    precio = models.DecimalField(
        max_digits=10,  # Número máximo de dígitos en el precio
        decimal_places=2,  # Número de decimales
        validators=[
            MinValueValidator(limit_value=0.01),  # Precio mínimo
            MaxValueValidator(limit_value=1000.00)  # Precio máximo
        ]
    )
    def __str__(self):
        return f"Nombre de la planta: {self.nombrePlanta}, Especie: {self.nombreEspecie}, Tiempo de vida: {self.tiempoVida}"

class PlantaReserva(models.Model):
    cantidad = models.IntegerField()
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.cantidad} de {self.planta.nombrePlanta} en reserva de {self.reserva.visita.usuario.name}"
