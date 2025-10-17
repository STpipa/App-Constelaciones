# app_constelaciones/constelacion/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm # Importamos el formulario estándar de Django
from django.contrib.auth.decorators import login_required
from .models import SistemaConstelar, Elemento
from django.contrib.auth.decorators import user_passes_test
import json


# Create your views here.
def inicio(request):
    """
    Ahora usamos la función render() de Django para cargar la plantilla HTML.
    """
    
    # render(solicitud, nombre_plantilla, contexto)
    return render(request, 'constelacion/inicio.html', {})

def registro(request):
    """
    Vista para manejar el registro de nuevos clientes.
    """
    if request.method == 'POST':
        # Si se envió el formulario, inicializamos el formulario con los datos POST
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Si los datos son válidos, guarda el nuevo usuario y redirige al login
            form.save()
            return redirect('login') # Redirige a la URL de login
    else:
        # Si es una solicitud GET (primera vez que se abre la página), muestra un formulario vacío
        form = UserCreationForm()
        
    # Renderiza la plantilla de registro, pasando el formulario
    return render(request, 'constelacion/registro.html', {'form': form})

@login_required # <-- Solo usuarios logueados pueden acceder
def crear_sistema(request):
    """
    Vista para iniciar la creación de un nuevo Sistema Constelar interactivo.
    """
    if request.method == 'POST':
        # Esta parte se usará para guardar el JSON del frontend
        
        # 1. Obtener los datos del formulario (título y descripción)
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        
        # 2. Inicializar el Sistema Constelar (sin el JSON de constelación aún)
        sistema = SistemaConstelar.objects.create(
            cliente=request.user,
            titulo=titulo,
            descripcion=descripcion,
        )
        
        # 3. Guardaremos la estructura de los elementos más tarde.
        # Por ahora, solo redirigimos a donde se hará la edición del genograma (detalle)
        return redirect('constelacion:detalle_sistema', pk=sistema.pk) 
    
    # Si es GET, muestra el formulario inicial
    return render(request, 'constelacion/crear_sistema.html', {})

@login_required
def detalle_sistema(request, pk):
    sistema = SistemaConstelar.objects.get(pk=pk) 
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'guardar':
            # 1. Obtiene la cadena JSON de la constelación
            constelacion_data_json = request.POST.get('constelacion_data', '[]')
            
            # 2. Actualiza el campo JSON en el modelo
            sistema.configuracion_visual_json = json.loads(constelacion_data_json)
            sistema.save()
            
            # 3. Guardar elementos individuales (OPCIONAL, pero recomendado para el Terapeuta)
            # Primero eliminamos los antiguos elementos para simplificar
            sistema.elementos.all().delete() 
            
            # Iteramos sobre los datos JSON para recrear los objetos Elemento en la DB
            for item in sistema.configuracion_visual_json:
                Elemento.objects.create(
                    sistema=sistema,
                    nombre=item.get('name', 'Sin Nombre'),
                    tipo=item.get('type', 'CON'), # Usar 'CON' como tipo por defecto si no lo encuentra
                    # Rol y notas se pueden añadir más tarde con un formulario de edición
                )

            # Mantenemos al usuario en la misma página después de guardar
            return redirect('constelacion:detalle_sistema', pk=sistema.pk)
    
    # Lógica para GET (mostrar la página)
    context = {
        'sistema': sistema,
        # Asegúrate de pasar el JSON como una cadena segura para que JS lo pueda parsear
        'datos_json_iniciales': json.dumps(sistema.configuracion_visual_json or []),
    }
    
    return render(request, 'constelacion/detalle_sistema.html', context)

@login_required
def dashboard_cliente(request):
    """
    Muestra la lista de todos los Sistemas Constelares creados por el usuario logueado.
    """
    sistemas = SistemaConstelar.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    
    context = {
        'sistemas': sistemas,
    }
    
    return render(request, 'constelacion/dashboard_cliente.html', context)

# Decorador para asegurar que solo los superusuarios (administradores) accedan
@user_passes_test(lambda u: u.is_superuser) 
@login_required 
def dashboard_admin(request):
    """
    Muestra TODOS los Sistemas Constelares creados por todos los clientes.
    Solo accesible para el Superusuario.
    """
    # Obtiene todos los sistemas, ordenados por la última actualización
    sistemas = SistemaConstelar.objects.all().order_by('-fecha_actualizacion')
    
    context = {
        'sistemas': sistemas,
    }
    
    return render(request, 'constelacion/dashboard_admin.html', context)