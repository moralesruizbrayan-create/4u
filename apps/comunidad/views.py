from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tema, Comentario
from .forms import TemaForm, ComentarioForm

def foro(request):
    # Obtenemos todos los temas, los más nuevos primero
    temas = Tema.objects.all().order_by('-id')
    # Pasamos el formulario vacío para la barra lateral
    form = TemaForm()
    
    return render(request, 'comunidad/foro.html', {
        'temas': temas,
        'form': form
    })

@login_required
def crear_tema(request):
    if request.method == 'POST':
        form = TemaForm(request.POST)
        if form.is_valid():
            tema = form.save(commit=False)
            tema.autor = request.user
            tema.save()
            return redirect('foro')
    return redirect('foro')

@login_required
def ver_tema(request, tema_id):
    tema = get_object_or_404(Tema, id=tema_id)
    comentarios = tema.comentario_set.all().order_by('id') # Asumiendo relación por defecto
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tema = tema
            comentario.autor = request.user
            comentario.save()
            return redirect('ver_tema', tema_id=tema.id)
    else:
        form = ComentarioForm()

    return render(request, 'comunidad/detalle.html', {
        'tema': tema,
        'comentarios': comentarios,
        'form': form
    })