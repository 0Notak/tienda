from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name="registrarse"),
    path('logout/', views.salida, name="signout"),
    path('login/', views.entrar, name="login"),
    
    path('tienda/', views.tienda, name="tienda"),
  
    
 
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    
    path('contacto/', views.contacto, name="contacto"),


    
    
 

]