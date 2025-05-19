from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Benevole, Permanence
from .forms import BenevoleForm, CustomUserRegistrationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

def index(request):
    return redirect('/')  # Redirect to Angular's root route

def home(request):
    return redirect('/')  # Redirect to Angular's home route

def success(request):
    return redirect('/success')  # Redirect to Angular's success route

@login_required
def espace_perso(request):
    return redirect('/espace-perso')  # Updated to match Angular route

def login(request):
    if request.user.is_authenticated:
        return redirect('/espace-perso')
    return redirect('/login')  # Redirect to Angular's login route

def logout_view(request):
    auth_logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('/')  # Redirect to Angular's home route

def register(request):
    return redirect('/register')  # Redirect to Angular's register route

@login_required
def modif_benev(request):
    return redirect('/modifier-benevole')  # Redirect to Angular's modif-benev route

@login_required
def messagerie(request, message_id=None):
    return redirect('/messagerie')  # Redirect to Angular's messagerie route

@login_required
def saisie_contraintes(request):
    return redirect('/saisie')  # Redirect to Angular's saisie route

@login_required
def saisie(request):
    return redirect('/saisie')  # Redirect to Angular's saisie route