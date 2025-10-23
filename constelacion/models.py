from django.db import models
from django.contrib.auth.models import User

#----------------------------------------------------------
#--------------------- DEFINIMOS MODELOS-------------------
#----------------------------------------------------------

# --- 1. MODELO PRINCIPAL DE LA CONSTELACIÓN ---

class SistemaConstelar(models.Model):
    """Representa la constelación o sistema que el cliente ha creado."""
    
    # Asocia la constelación con un usuario (el cliente)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, 
                                help_text="Usuario (cliente) que creó esta constelación.")
    
    titulo = models.CharField(max_length=150, 
                            help_text="Un título o enfoque para la constelación (ej: 'Mi relación con el dinero').")
    
    descripcion = models.TextField(blank=True, null=True, 
                                help_text="Notas o intenciones del cliente sobre este sistema.")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Campo para guardar la configuración visual del genograma (posición, líneas, etc.)
    # Esto guardará datos en formato JSON/Texto que usará el frontend JS
    configuracion_visual_json = models.JSONField(default=list, blank=True, null=True, 
                                                help_text="Datos JSON con las posiciones, colores y enlaces del diagrama.")
    
    def __str__(self):
        return f"Sistema: {self.titulo} de {self.cliente.username}"


# --- 2. MODELO PARA CADA ELEMENTO DENTRO DEL SISTEMA ---
# Este modelo es muy flexible para permitir personas, objetos o conceptos
class Elemento(models.Model):
    TIPO_CHOICES = [
        ('PER', 'Persona/Familiar'),
        ('OBJ', 'Objeto/Lugar'),
        ('CON', "Concepto/Sentimiento (ej: 'Culpa', 'Éxito')"),
    ]

    sistema = models.ForeignKey(SistemaConstelar, related_name='elementos', on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=100, help_text="Nombre del elemento (ej: 'Mamá', 'La Casa', 'Mi Miedo').")
    
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES, default='PER', 
                            help_text="Define si es una persona, objeto o concepto.")
    
    rol = models.CharField(max_length=150, blank=True, 
                        help_text="Rol o cualidad asignada por el cliente (ej: 'El Excluido', 'Lo Inaccesible').")
    
    # Datos específicos que el cliente podría adjuntar a este elemento
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()}) en {self.sistema.titulo}"