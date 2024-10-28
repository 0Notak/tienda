from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from .models import Producto, Carrito, CarritoItem, Orden, OrdenItem, OrdenControl

# Create your views here.


def inicio(request):
    
    
    return render(request, 'index.html', {
        
    })



def registro(request):

    print(request.POST)

    if request.method == 'GET':
            return render(request, 'registro.html', {
        'login': UserCreationForm
        })

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Validación de que los campos no estén vacíos
            if not username or not email or not password1 or not password2:
                messages.error(request, "Todos los campos son obligatorios.")
                return redirect('registrarse')

            # Validación de formato de correo electrónico
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "El correo electrónico no es válido.")
                return redirect('registrarse')

            # Verificar que las contraseñas coincidan
            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden.")
                return redirect('registrarse')

            # Validar que el email sea único
            if User.objects.filter(email=email).exists():
                messages.error(request, "Este correo electrónico ya está registrado.")
                return redirect('registrarse')

            # Validación de la fuerza de la contraseña
            try:
                validate_password(password1)
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('registrarse')

            # Validación de que el nombre de usuario sea único
            if User.objects.filter(username=username).exists():
                messages.error(request, "Este nombre de usuario ya está en uso.")
                return redirect('registrarse')

            # Creación segura del usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )

            # Guardamos el usuario
            user.save()

            # Iniciar sesión automáticamente después del registro
            login(request, user)

            # Mensaje de éxito
            messages.success(request, "Te has registrado correctamente.")
            return redirect('inicio')

    return render(request, 'registro.html')
        
def salida (request):
    logout(request)
    return redirect('inicio')


def entrar (request):
    if request.method == 'GET':
        return render (request, 'login.html',{
        'form': AuthenticationForm
    })
    else: 
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            
            return render(request, 'login.html',{
                'form': AuthenticationForm,
                'error': 'Usuario y contrasena es incorrecto'
            })


def tienda (request,):
    datos1= Producto.objects.all().values()
   
    return render (request, 'agregar_productos.html',{
        'productos': datos1
    })




# Vista para agregar un producto al carrito
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Verificar si el producto ya está en el carrito
    item, item_created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not item_created:
        # Si ya está en el carrito, incrementar la cantidad
        item.cantidad += 1
        item.save()

    return redirect('ver_carrito')

# Vista para ver los productos en el carrito
@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)
   
    
    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
        
    })

# Vista para eliminar un producto del carrito
@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if item.carrito.usuario == request.user:
        item.delete()
    return redirect('ver_carrito')

# Vista para finalizar la compra
@login_required
def finalizar_compra(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = carrito.items.all()

    if not items:
        return redirect('ver_carrito')  # No puedes finalizar compra con un carrito vacío

    total = sum(item.producto.precio * item.cantidad for item in items)

    # Crear la Orden
    nueva_orden = Orden.objects.create(usuario=request.user, total=total)

    # Mover los elementos del carrito a la orden
    for item in items:
        OrdenItem.objects.create(
            orden=nueva_orden,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
    
    # Crear un registro de control para la auditoría
    OrdenControl.objects.create(orden=nueva_orden, comentarios="Compra finalizada")

    # Vaciar el carrito después de la compra
    carrito.items.all().delete()

    return redirect('detalle_orden', orden_id=nueva_orden.id)

# Vista para ver el detalle de una orden específica
@login_required
def detalle_orden(request, orden_id):
    orden = get_object_or_404(Orden, id=orden_id, usuario=request.user)
    items = orden.items.all()
    
    return render(request, 'detalle_orden.html', {
        'orden': orden,
        'items': items
    })

def contacto (request):
    
    return render (request, 'contacto.html',{
        
    })