# app_constelaciones/constelacion/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm # Importamos el formulario estándar de Django
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import SistemaConstelar, Elemento
from django import forms
from django.contrib.auth.decorators import user_passes_test
import json


# -------------------------------------------------------------
# Paso 1: Definir el Formulario (Se requiere un formulario simple)
# -------------------------------------------------------------

# Definimos un formulario simple para crear el título del sistema.
# Si ya lo tenías, asegúrate de que esté correcto.
class SistemaConstelarForm(forms.ModelForm):
    class Meta:
        model = SistemaConstelar
        # Solo le pedimos el titulo al usuario
        fields = ['titulo']


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
        form = SistemaConstelarForm(request.POST)
        if form.is_valid():
            # No guardarmos el formulario inmediatamente (commit=False)
            nuevo_sistema = form.save(commit=False)

            # Asignamos el usuario actual (el que está logueado)
            nuevo_sistema.cliente = request.user

            # El campo 'constelacion_data' (el JSON) se deja vacío por ahora
            # ya que se llenará en detalle_sistema.
             
            nuevo_sistema.save()

            # Redirigimos al lienzo interactivo para empezar a constelar
            return redirect('constelacion:detalle_sistema', pk=nuevo_sistema.pk)
    else:
        # Si es una solicitud GET, mostramos el formulario vacío
        form = SistemaConstelarForm()
        
    return render(request, 'constelacion/crear_sistema.html', {'form': form}) 
        
@login_required
def detalle_sistema(request, pk):
    # Usamos get_object_or_404 para evitar un error 500 si el PK no existe
    sistema = get_object_or_404(SistemaConstelar, pk=pk) 
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'guardar':
            # 1. Obtiene la cadena JSON
            constelacion_data_json = request.POST.get('constelacion_data', '[]')
            
            # 2. Carga y Guarda el JSON
            try:
                data = json.loads(constelacion_data_json)
            except json.JSONDecodeError:
                # Si el JSON está mal, lo tratamos como vacío para evitar un error fatal
                data = []

            sistema.configuracion_visual_json = data
            sistema.save()
            
            # 3. Regeneración de elementos (sin cambios aquí)
            sistema.elementos.all().delete() 
            for item in data:
                # Nos aseguramos de que el 'tipo' esté en mayúsculas para coincidir con TIPO_CHOICES
                tipo_normalizado = item.get('type', 'CON').upper() 
                Elemento.objects.create(
                    sistema=sistema,
                    nombre=item.get('name', 'Sin Nombre'),
                    tipo=tipo_normalizado[:3], # Tomamos solo los primeros 3 caracteres (PER, OBJ, CON)
                )

            return redirect('constelacion:detalle_sistema', pk=sistema.pk)
    
    # Lógica para GET (mostrar la página)
    
    # Asegúrate de que si el campo es None, se devuelva un array vacío para JSON
    datos_iniciales = sistema.configuracion_visual_json if sistema.configuracion_visual_json else []
    
    context = {
        'sistema': sistema,
        # Convertimos a JSON para el frontend, ¡asegurándonos de que sea un array vacío si no hay datos!
        'datos_json_iniciales': json.dumps(datos_iniciales), 
    }
    
    return render(request, 'constelacion/detalle_sistema.html', context)
    
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