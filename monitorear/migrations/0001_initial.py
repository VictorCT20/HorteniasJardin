# Generated by Django 4.2.6 on 2023-11-02 02:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('contraseña', models.CharField(max_length=50)),
                ('admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrePlanta', models.CharField(max_length=50)),
                ('nombreEspecie', models.CharField(max_length=50)),
                ('tiempoVida', models.CharField(max_length=70)),
                ('Imagen', models.CharField(max_length=100)),
                ('detalle', models.TextField()),
                ('curiosidad', models.TextField()),
                ('propiedades', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(limit_value=0.01), django.core.validators.MaxValueValidator(limit_value=1000.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Visitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitorear.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visita', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitorear.visitas')),
            ],
        ),
        migrations.CreateModel(
            name='PlantaReserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitorear.planta')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitorear.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroEstrellas', models.IntegerField()),
                ('comentario', models.TextField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitorear.usuario')),
            ],
        ),
    ]
