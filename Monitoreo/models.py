from django.db import models

# Create your models here.
class Post(models.Model):
    user=models.CharField(max_length=250)
    contra=models.CharField(max_length=250)

    def __str__(self):
        return f"Usuario: {self.user}, Contraseña: [Oculto por seguridad]"