# Generated by Django 4.2.16 on 2024-10-10 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_carrito_carritoitem_orden_ordencontrol_ordenitem_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]