from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
# Modelos
from .models import LeccionVideo, ProgresoUsuario, Modulo, PreguntaExamen, PreguntaTest
from apps.usuarios.models import Perfil
# Formularios
from .forms import ModuloForm, LeccionForm, PreguntaExamenForm, PreguntaTestForm

# ==========================================
# SECCIÓN 1: VISTAS PARA ESTUDIANTES
# ==========================================

@login_required
def ver_leccion(request, leccion_id):
    """
    Vista donde el estudiante ve el video y responde el Quiz rápido (Test).
    """
    leccion = get_object_or_404(LeccionVideo, id=leccion_id)
    # Obtenemos las preguntas asociadas a este video específico
    preguntas = leccion.preguntas.all() 
    
    # Verificar o crear registro de progreso
    progreso, created = ProgresoUsuario.objects.get_or_create(usuario=request.user, leccion=leccion)

    if request.method == 'POST':
        # Lógica para calificar el Quiz del video
        aciertos = 0
        total = preguntas.count()
        
        for pregunta in preguntas:
            respuesta_usuario = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_usuario == pregunta.correcta:
                aciertos += 1
        
        # Calcular nota (0 a 100)
        nota = (aciertos / total) * 100 if total > 0 else 0
        
        if nota >= 60: # Se aprueba con 60%
            if not progreso.completado:
                progreso.completado = True
                progreso.puntaje_obtenido = nota
                progreso.save()
                
                # Sumar puntos al perfil del usuario
                perfil = request.user.perfil
                perfil.puntos += leccion.puntos_recompensa
                
                # Sistema de Niveles
                if perfil.puntos >= 100: perfil.nivel = 'Intermedio'
                if perfil.puntos >= 300: perfil.nivel = 'Avanzado'
                if perfil.puntos >= 500: perfil.nivel = 'Maestro'
                perfil.save()
                
                messages.success(request, f'¡Excelente! Aprobaste y ganaste {leccion.puntos_recompensa} puntos.')
            else:
                messages.info(request, 'Ya habías completado esta lección, pero buen repaso.')
            
            return redirect('dashboard')
        else:
            messages.error(request, 'No alcanzaste el puntaje mínimo. Inténtalo de nuevo.')

    return render(request, 'formacion/ver_leccion.html', {
        'leccion': leccion,
        'preguntas': preguntas,
        'progreso': progreso
    })

@login_required
def realizar_examen(request, modulo_id):
    """
    Vista para tomar el Examen Final de un Módulo completo.
    """
    modulo = get_object_or_404(Modulo, id=modulo_id)
    preguntas = modulo.preguntas_examen.all()
    
    if not preguntas:
        messages.warning(request, 'Este módulo aún no tiene un examen asignado.')
        return redirect('dashboard')

    if request.method == 'POST':
        aciertos = 0
        total = preguntas.count()
        
        for pregunta in preguntas:
            respuesta = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta == pregunta.correcta:
                aciertos += 1
        
        nota = (aciertos / total) * 100 if total > 0 else 0
        
        if nota >= 70: # Examen final exige 70%
            # Dar puntos extra por aprobar módulo (ej: 50 pts)
            perfil = request.user.perfil
            perfil.puntos += 50 
            perfil.save()
            
            messages.success(request, f'¡FELICIDADES! Aprobaste el Módulo "{modulo.titulo}" con {int(nota)}%. +50 Puntos extra.')
            return redirect('dashboard')
        else:
            messages.error(request, f'Reprobaste con {int(nota)}%. Necesitas 70% para aprobar. Repasa los videos e inténtalo de nuevo.')

    return render(request, 'formacion/realizar_examen.html', {'modulo': modulo, 'preguntas': preguntas})


# ==========================================
# SECCIÓN 2: GESTIÓN (ADMINISTRADOR / STAFF)
# ==========================================

@staff_member_required
def crear_modulo(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_admin')
    else:
        form = ModuloForm()
    
    return render(request, 'formacion/form_gestion.html', {
        'form': form, 
        'titulo': 'Crear Nuevo Módulo'
    })

@staff_member_required
def crear_leccion(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)
    
    if request.method == 'POST':
        form = LeccionForm(request.POST, request.FILES)
        if form.is_valid():
            leccion = form.save(commit=False)
            leccion.modulo = modulo
            leccion.save()
            return redirect('panel_admin')
    else:
        form = LeccionForm()
    
    return render(request, 'formacion/form_gestion.html', {
        'form': form, 
        'titulo': f'Nueva Lección para: {modulo.titulo}'
    })

@staff_member_required
def agregar_pregunta_examen(request, modulo_id):
    """
    Agrega una pregunta al EXAMEN FINAL del módulo.
    """
    modulo = get_object_or_404(Modulo, id=modulo_id)
    if request.method == 'POST':
        form = PreguntaExamenForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.modulo = modulo
            pregunta.save()
            messages.success(request, 'Pregunta agregada al examen final correctamente.')
            return redirect('panel_admin')
    else:
        form = PreguntaExamenForm()
    
    return render(request, 'formacion/form_gestion.html', {
        'form': form, 
        'titulo': f'Agregar Pregunta al Examen Final: {modulo.titulo}'
    })

@staff_member_required
def agregar_pregunta_test(request, leccion_id):
    """
    Agrega una pregunta al QUIZ RÁPIDO de un video específico.
    """
    leccion = get_object_or_404(LeccionVideo, id=leccion_id)
    
    if request.method == 'POST':
        form = PreguntaTestForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.leccion = leccion
            pregunta.save()
            messages.success(request, 'Pregunta de evaluación agregada al video correctamente.')
            return redirect('panel_admin')
    else:
        form = PreguntaTestForm()
    
    return render(request, 'formacion/form_gestion.html', {
        'form': form, 
        'titulo': f'Agregar Quiz para el video: {leccion.titulo}'
    })