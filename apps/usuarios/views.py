from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .forms import RegistroUsuarioForm

# --- IMPORTACIONES DE OTRAS APPS ---
# Traemos los modelos necesarios para el Dashboard y el Panel Admin
from apps.formacion.models import Modulo
from apps.publico.models import Producto

# 1. VISTA DE REGISTRO DE USUARIOS
def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Loguear automáticamente al usuario después de registrarse
            login(request, usuario)
            # Redirigir al panel principal
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})

# 2. VISTA DASHBOARD (Para estudiantes/usuarios normales)
@login_required
def dashboard(request):
    # Traemos los cursos disponibles. 
    # Usamos prefetch_related para que cargue rápido las lecciones asociadas.
    modulos = Modulo.objects.all().prefetch_related('lecciones')
    
    return render(request, 'usuarios/dashboard.html', {'modulos': modulos})

# 3. VISTA PANEL DE GESTIÓN (Solo para Administradores)
@staff_member_required
def panel_admin(request):
    # Recopilamos datos para mostrar en tu panel privado
    total_usuarios = User.objects.all().count()
    productos = Producto.objects.all()
    modulos = Modulo.objects.all()
    
    contexto = {
        'total_usuarios': total_usuarios,
        'productos': productos,
        'modulos': modulos
    }
    return render(request, 'usuarios/panel_admin.html', contexto)