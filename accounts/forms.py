# forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm




class CustomLoginForm(AuthenticationForm):
    # Ajoutez d'autres champs personnalisés ici

    class Meta:
        model = User  # Remplacez par votre modèle User
        fields = ('username', 'password')  # Incluez les champs existants
