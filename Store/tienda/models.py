from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    inventario = models.PositiveIntegerField(default=0)  # Cantidad en inventario
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Modelo Carrito de Compras
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
# Modelo para los elementos dentro del Carrito
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.username}"


# Modelo Orden para registrar las compras finalizadas
class Orden(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_orden = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Orden #{self.id} de {self.usuario.username} por ${self.total}"

# Modelo para registrar los productos comprados en una Orden
class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en la Orden #{self.orden.id}"

# Modelo para registrar control (estilo DataVault)
class OrdenControl(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # Fecha y hora del registro
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Control de Orden #{self.orden.id} en {self.timestamp}"
