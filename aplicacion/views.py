from django.shortcuts import render
from .models import Producto, Usuario,Carrito,ItemCarrito, Pedido
from .forms import ProductoForm, UpdateProductoForm, UpdateUsuarioForm
from django.shortcuts import get_object_or_404, redirect

from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .decoradores import staff_required
from django.conf import settings
from os import remove,path
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UsuarioCreationForm
from django.contrib.auth.forms import AuthenticationForm
import json


def iniciarsesion(request):
    if request.method=='POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            usuario=form.get_user()
            if usuario is not None:
                login(request,usuario)
                return redirect(to='index')
        else:
            return redirect(to='login')
    form=AuthenticationForm()
    data={
        "form":form
    }
    return render(request,'registration/login.html',data)

def cerrar_sesion(request):
    logout(request)
    return redirect(to='index')

# Create your views here.

def index(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }

    return render(request,'aplicacion/index.html',datos)

def cambiadireccion(request):
    return render(request,'aplicacion/cambiadireccion.html')

def cambiatarjeta(request):
    return render(request,'aplicacion/cambiatarjeta.html')

from django.shortcuts import get_object_or_404

def carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total_carrito = carrito.total_carrito()
    
    # Obtener los datos del usuario
    usuario = request.user
    nombre_completo = f"{usuario.nombre} {usuario.apellido}"
    email = usuario.email
    telefono = usuario.telefono

    if request.method == 'POST':
        if 'proceder_pago' in request.POST:
            # Serializar los productos del carrito
            productos_pedido = []
            for item in items:
                producto = {
                    'nombre': item.producto.nombre,
                    'cantidad': item.cantidad,
                    'precio_unitario': item.producto.precio,
                    'subtotal': item.subtotal(),
                }
                productos_pedido.append(producto)
            
            # Convertir la lista de productos a JSON
            productos_json = json.dumps(productos_pedido)

            # Guardar el pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                productos=productos_json,
                subtotal=total_carrito,
                nombre_completo=nombre_completo,
                email=email,
                direccion=request.POST.get('direccion'),
                departamento_oficina_piso=request.POST.get('dept'),
            )

            # Limpiar el carrito después de guardar el pedido
            for item in carrito.items.all():
                item.delete()
            messages.success(request, '¡Pedido realizado con éxito!')

            # Redireccionar a una página de confirmación o a donde desees
            return redirect('historial_user')  # Ajusta esto a tu URL de confirmación

        item_id = request.POST.get('item_id')
        if 'accion' in request.POST:
            accion = request.POST.get('accion')

            if accion.startswith('restar'):
                item_id = int(accion.split('_')[1])
                item = get_object_or_404(ItemCarrito, id=item_id)
                if item.cantidad > 1:
                    item.cantidad -= 1
                    item.save()

            elif accion.startswith('sumar'):
                item_id = int(accion.split('_')[1])
                item = get_object_or_404(ItemCarrito, id=item_id)
                item.cantidad += 1
                item.save()

        elif 'eliminar_item' in request.POST:
            item_id = request.POST.get('eliminar_item')
            item = get_object_or_404(ItemCarrito, id=item_id)
            item.delete()
            # Redireccionar a la vista del carrito después de eliminar el item
            return redirect('carrito')

        total_carrito = carrito.total_carrito()

    datos = {
        "carrito": carrito,
        "items": items,
        "total_carrito": total_carrito,
        "nombre_completo": nombre_completo,
        "email": email,
        "telefono": telefono,
    }

    return render(request, 'aplicacion/carrito.html', datos)


def cervezas(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }  
    return render(request,'aplicacion/cervezas.html',datos)

def contra(request):
    return render(request,'aplicacion/contra.html')

def crearu(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Aquí puedes hacer cualquier acción adicional después de guardar el usuario
            return redirect('login')  # Reemplaza con la ruta a donde redirigir
    else:
        form = UsuarioCreationForm()
    return render(request, 'aplicacion/crearu.html', {'form': form})

def destilados(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }
    return render(request,'aplicacion/destilados.html',datos)

def espumantes(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }
    return render(request,'aplicacion/espumantes.html',datos)


@staff_required
def gestionusuario(request):

    # Obtener todos los productos existentes para mostrarlos
    usuario = Usuario.objects.all()

    if request.method == "POST":
        form = UsuarioCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestionusuario')  # Redirigir a la misma página después de guardar el producto
    else:
        form = UsuarioCreationForm()

    datos = {
        "form": form,
        "usuario": usuario 
    }
    return render(request,'aplicacion/gestionusuario.html',datos)

def historial_user(request):
    
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')

    pedidos=list(pedidos)



    for i in pedidos:
        i.productos=i.productos.replace("\'", "\"")
        
        i.productos=json.loads(i.productos)
        

    

 

    datos = {
        'pedidos': pedidos
    }

    return render(request, 'aplicacion/historial_user.html', datos)

@staff_required
def historialEnvio(request):
    return render(request,'aplicacion/historialEnvio.html')

def index_copy(request):
    return render(request,'aplicacion/index_copy.html')


def licores(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }
    return render(request,'aplicacion/licores.html',datos)

def opciones(request):


    return render(request,'aplicacion/opciones.html')

def pago(request):
    return render(request,'aplicacion/pago.html')

def user(request):
    return render(request,'aplicacion/user.html')

def verificacion(request):
    return render(request,'aplicacion/verificacion.html')

def verproducto(request,id):

    producto=get_object_or_404(Producto,id=id)


    if request.method == 'POST':
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        item_carrito, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not item_created:
            item_carrito.cantidad += 1
            item_carrito.save()

        return redirect('carrito')
    


    datos={
        "producto":producto
    }

    return render(request,'aplicacion/verproducto.html',datos)

def vinos(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }
    return render(request,'aplicacion/vinos.html',datos)

def whiskies(request):
    producto = Producto.objects.all()


    datos = {
        "producto": producto  # Pasar todos los productos al contexto
    }
    return render(request,'aplicacion/whiskies.html',datos)

@staff_required
def gestion_prod(request,):
    # Obtener todos los productos existentes para mostrarlos
    producto = Producto.objects.all()

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion_prod')  # Redirigir a la misma página después de guardar el producto
    else:
        form = ProductoForm()

    datos = {
        "form": form,
        "producto": producto  # Pasar todos los productos al contexto
    }

    return render(request, 'aplicacion/gestion_prod.html', datos)

@staff_required
def editarproducto(request,id):
    producto=get_object_or_404(Producto,id=id)
    form = UpdateProductoForm(instance=producto)

    if request.method == "POST":
        form = UpdateProductoForm(data=request.POST,files=request.FILES,instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestion_prod')

    datos={
        "form":form,
        "producto":producto
    }

    return render(request,'aplicacion/editarproducto.html',datos)

@staff_required
def eliminarproducto(request,id):
    producto=get_object_or_404(Producto,id=id)
    if request.method=="POST":
        
        remove(path.join(str(settings.MEDIA_ROOT).replace('/media',''))+producto.imagen.url)
        producto.delete()

        return redirect(to='gestion_prod')
        

    datos={
        "producto":producto
    }
    return render(request,'aplicacion/eliminarproducto.html',datos)

@staff_required
def editarusuario(request,id):
    usuario=get_object_or_404(Usuario,rut=id)
    form = UpdateUsuarioForm(instance=usuario)

    if request.method == "POST":
        form = UpdateUsuarioForm(data=request.POST,files=request.FILES,instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gestionusuario')

    datos={
        "form":form,
        "usuario":usuario
    }


    return render(request,'aplicacion/editarusuario.html',datos)

@staff_required
def eliminarusuario(request,id):
    usuario=get_object_or_404(Usuario,rut=id)
    if request.method=="POST":
        
        usuario.delete()

        return redirect(to='gestionusuario')
        

    datos={
        "usuario":usuario
    }


    return render(request,'aplicacion/eliminarusuario.html',datos)


