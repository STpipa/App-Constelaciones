# app_constelaciones/constelacion/urls.py
from django.urls import path
from . import views

# El nombre de la aplicación ayuda a referenciar las URLs en las plantillas
app_name = 'constelacion' 

urlpatterns = [
    # Mapea la ruta '/' (relativa a lo que definimos en core/urls.py)
    # y la asocia con una función llamada 'inicio' dentro de 'views.py'
    # path('', views.inicio, name='inicio'),
    
    # 🌟 NUEVA RUTA DE REGISTRO
    path('registro/', views.registro, name='registro'),

    
    path('dashboard/', views.dashboard_cliente, name='dashboard_cliente'),
    path('admin-panel/', views.dashboard_admin, name='dashboard_admin'),
    path('crear/', views.crear_sistema, name='crear_sistema'),
    path('detalle/<int:pk>/', views.detalle_sistema, name='detalle_sistema'),
]