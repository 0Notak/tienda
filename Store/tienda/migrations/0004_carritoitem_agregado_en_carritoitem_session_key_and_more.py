# Generated by Django 4.2.16 on 2024-10-10 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tienda', '0003_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='carritoitem',
            name='agregado_en',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='carritoitem',
            unique_together={('usuario', 'producto', 'session_key')},
        ),
        migrations.RemoveField(
            model_name='carritoitem',
            name='carrito',
        ),
    ]
