from django import forms
from .models import Modulo, LeccionVideo, PreguntaExamen, PreguntaTest

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Módulo 1: Introducción'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LeccionForm(forms.ModelForm):
    class Meta:
        model = LeccionVideo
        fields = ['titulo', 'video_archivo', 'descripcion', 'puntos_recompensa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'video_archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'puntos_recompensa': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PreguntaExamenForm(forms.ModelForm):
    class Meta:
        model = PreguntaExamen
        fields = ['texto', 'opcion_a', 'opcion_b', 'opcion_c', 'correcta']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿Cuál es la capital de...?'}),
            'opcion_a': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'opcion_b': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'opcion_c': forms.TextInput(attrs={'class': 'form-control bg-light'}),
            'correcta': forms.Select(attrs={'class': 'form-select fw-bold'}),
        }

class PreguntaTestForm(forms.ModelForm):
    class Meta:
        model = PreguntaTest
        fields = ['texto', 'opcion_a', 'opcion_b', 'opcion_c', 'correcta']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pregunta del video...'}),
            'opcion_a': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Opción A'}),
            'opcion_b': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Opción B'}),
            'opcion_c': forms.TextInput(attrs={'class': 'form-control bg-light', 'placeholder': 'Opción C'}),
            'correcta': forms.Select(attrs={'class': 'form-select fw-bold'}),
        }