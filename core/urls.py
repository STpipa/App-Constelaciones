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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # 🌟 Usar la vista de inicio directamente en la raíz (/)
    path('', inicio, name='inicio'), # <-- Llama a views.inicio, no a include

    # 🌟 Redirige todo lo que vaya a 'constelaciones/' a las URLs de la app
    # path('constelaciones/', include('constelacion.urls')),

    # 🌟 Añade las URLs de autenticación por defecto de Django
    # Las URLs serán /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Redirige la raíz
    path('', include('constelacion.urls')),
]
