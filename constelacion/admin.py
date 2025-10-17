from django.contrib import admin
from django.contrib.auth.models import User
from .models import SistemaConstelar, Elemento

# Register your models here.

admin.site.register(SistemaConstelar)
admin.site.register(Elemento)

