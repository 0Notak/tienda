from django.contrib import admin
from .models import Producto, Carrito, CarritoItem, Orden, OrdenItem, OrdenControl

# Register your models here.
admin.site.register(Producto,)
admin.site.register(Orden,)
admin.site.register(OrdenControl,)
