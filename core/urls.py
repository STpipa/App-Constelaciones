"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from constelacion.views import inicio
from django.conf import settings 
from django.conf.urls.static import static
<<<<<<< HEAD

=======
>>>>>>> ea6a50eb3166c76fcd699725d7c1a6ad4c36dbda

urlpatterns = [
    # 1. Panel de Administración de Django
    path('admin/', admin.site.urls),
    
<<<<<<< HEAD
    # 🌟 1. Rutas de Autenticación: Debe ir solo una vez
    path('accounts/', include('django.contrib.auth.urls')), 

    # 🌟 2. Ruta de Inicio (/): Usa tu vista de inicio
    path('', inicio, name='inicio'), 

    # 🌟 3. Rutas de tu App: Incluye el resto de las URLs de 'constelacion'
    path('', include('constelacion.urls')),
]

# Esto es SOLO para desarrollo (DEBUG=True) y permite que se carguen las imágenes
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
    # 2. Rutas de Autenticación de Django (login, logout, password_reset, etc.)
    # Estas URLs serán: /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')), 

    # 3. Rutas de la Aplicación 'constelacion'

    # a) Ruta de Inicio (la raíz del sitio '/')
    path('', inicio, name='inicio'), 
    
    # b) El resto de las URLs de la aplicación (dashboard, crear, detalle, etc.)
    # Estas URLs serán: /dashboard/, /registro/, /crear/, etc.
    path('', include('constelacion.urls')),
]

# Configuración de archivos estáticos SÓLO para modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> ea6a50eb3166c76fcd699725d7c1a6ad4c36dbda
