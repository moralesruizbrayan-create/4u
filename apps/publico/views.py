from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Producto
# Importamos AMBOS formularios
from .forms import ProductoForm, CategoriaForm 

def index(request):
    productos = Producto.objects.all()
    return render(request, 'publico/index.html', {'productos': productos})

# --- GESTIÓN DE TIENDA (ADMIN) ---

@staff_member_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = ProductoForm()
    return render(request, 'formacion/form_gestion.html', {'form': form, 'titulo': 'Nuevo Producto'})

@staff_member_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('panel_admin')

@staff_member_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = CategoriaForm()
    
    return render(request, 'formacion/form_gestion.html', {'form': form, 'titulo': 'Nueva Categoría'})