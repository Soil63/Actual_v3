from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import  Benevole, Permanence
from .forms import (
    BenevoleForm,
    CustomUserRegistrationForm,
    CustomAuthenticationForm,
   
)
from django.contrib.auth import get_user_model
from .models import Message
from .forms import MessageForm
from datetime import datetime, timedelta
from math import ceil

User = get_user_model()


def index(request):
    return render(request, 'benvoplanify/index.html')

def home(request):
    return render(request,'benvoplanify/home.html')

def success(request):
    return render(request, 'benvoplanify/success.html')




@login_required
def espace_perso(request):
    """Espace personnel avec statistiques et gestion des plannings"""
    user = request.user
    benevole = get_object_or_404(Benevole, user=user)

    # Calculer le planning
    benevoles = Benevole.objects.filter(is_active=True)
    planning = generate_planning(benevoles, mois=datetime.now().month)

    # Détecter les conflits
    conflicts = Permanence.objects.filter(is_filled=False)
    solutions = []

    for conflict in conflicts:
        solutions.append({
            'permanence': conflict,
            'possible_benevoles': Benevole.objects.filter(is_active=True),
        })

    context = {
        'benevole': benevole,
        'nb_permanences': benevole.nb_permanences,
        'planning': planning,
        'conflicts': conflicts,
        'solutions': solutions,
    }

    if not planning:
        messages.warning(request, "Aucun planning disponible pour le moment.")

    return render(request, 'benvoplanify/espace_perso.html', context)


#---------------------------------------------------------------------------------


def login(request):
    """Page de connexion avec gestion des erreurs"""
    if request.user.is_authenticated:
        return redirect('espace_perso')  # Redirige si déjà connecté

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'benvoplanify/login.html', {'form': form})



#---------------------------------------------------------------------------------


def logout_view(request):
    """Déconnexion de l'utilisateur avec message de confirmation"""
    auth_logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')

#---------------------------------------------------------------------------------



def register(request):
    """Inscription utilisateur avec validation et message de bienvenue"""
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Benevole.objects.create(
                user=user,
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                email=form.cleaned_data['email'],
                date_naiss=form.cleaned_data['date_naiss'],
            )
            auth_login(request, user)
            messages.success(request, f"Bienvenue {user.prenom} {user.nom} ! Votre compte a été créé avec succès.")
            return redirect('home')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'benvoplanify/register.html', {'form': form})


#---------------------------------------------------------------------------------


@login_required
def modif_benev(request):
    user = request.user
    benevole = get_object_or_404(Benevole, user=user)
    if request.method == 'POST':
        form = BenevoleForm(request.POST, instance=benevole)
        if form.is_valid():
            form.save()
            return redirect('espace_perso')
    else:
        form = BenevoleForm(instance=benevole)
    return render(request, 'benvoplanify/modif_benev.html', {'form': form})


#---------------------------------------------------------------------------------



@login_required
def messagerie(request, message_id=None):
    """Gère la messagerie : affichage des messages, envoi et consultation des détails"""
    user = request.user

    # Afficher les messages reçus
    messages_reçus = Message.objects.filter(receiver=user).order_by('-timestamp')

    # Consultation des détails d'un message
    message_detail = None
    if message_id:
        message_detail = get_object_or_404(Message, id=message_id, receiver=user)
        message_detail.is_read = True
        message_detail.save()

    # Envoi d'un nouveau message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.save()
            messages.success(request, "Message envoyé avec succès.")
            return redirect('messagerie')
    else:
        form = MessageForm()

    return render(request, 'benvoplanify/messagerie.html', {
        'messages_reçus': messages_reçus,
        'message_detail': message_detail,
        'form': form,
    })
#---------------------------------------------------------------------------------


@login_required
def saisie_contraintes(request):
    """Génère un planning respectant les contraintes et préférences"""
    benevoles = Benevole.objects.filter(is_active=True)
    permanences = Permanence.objects.filter(is_filled=False).order_by('date')

    # Calculer le nombre de permanences à effectuer pour chaque bénévole
    permanences_by_benevole = calculate_permanences()

    planning = []
    conflicts = []

    for permanence in permanences:
        assigned = False
        for benevole in benevoles:
            constraints = benevole.constraints or {}
            preferences = benevole.preferences or {}

            # Vérifiez si le bénévole est disponible pour cette permanence
            if permanence.time_slot in constraints.get(permanence.date.strftime('%A'), []):
                # Vérifiez si le bénévole n'a pas dépassé son quota
                if permanences_by_benevole[benevole] > 0:
                    permanence.benevole = benevole
                    permanence.is_filled = True
                    permanence.save()
                    benevole.nb_permanences += 1
                    benevole.save()
                    permanences_by_benevole[benevole] -= 1
                    planning.append(permanence)
                    assigned = True
                    break

        if not assigned:
            conflicts.append(permanence)

    return render(request, 'benvoplanify/saisie.html', {
        'planning': planning,
        'conflicts': conflicts,
    })
#---------------------------------------------------------------------------------
def generate_planning(benevoles, mois):
    """Génère un planning structuré pour les bénévoles actifs"""
    permanences = Permanence.objects.filter(date__month=mois, is_filled=False).order_by('date')
    planning = {}

    for permanence in permanences:
        jour = permanence.date.strftime('%A')  # Nom du jour (ex : Lundi, Mardi)
        if jour not in planning:
            planning[jour] = {"Matin": None, "Apres_midi": None}  # Initialiser les créneaux

        for benevole in benevoles:
            constraints = benevole.constraints or {}
            if permanence.time_slot not in constraints.get(jour, []):
                if permanence.time_slot == "Matin" and not planning[jour]["Matin"]:
                    planning[jour]["Matin"] = permanence
                    permanence.benevole = benevole
                    permanence.is_filled = True
                    permanence.save()
                    break
                elif permanence.time_slot == {{"Après_midi"}} and not planning[jour]["Apres_midi"]:
                    planning[jour]["Apres_midi"] = permanence
                    permanence.benevole = benevole
                    permanence.is_filled = True
                    permanence.save()
                    break

    return planning




#---------------------------------------------------------------------------------

@login_required
def detect_conflicts_and_solutions(request):
    """Détecte les conflits et propose des solutions"""
    conflicts = Permanence.objects.filter(is_filled=False)
    solutions = []

    for conflict in conflicts:
        # Proposez des solutions en fonction des préférences souples
        solutions.append({
            'permanence': conflict,
            'possible_benevoles': Benevole.objects.filter(is_active=True),
        })

    return render(request, 'benvoplanify/saisie.html', {
        'conflicts': conflicts,
        'solutions': solutions,
    })

# what about calculate permanence?

def calculate_permanences():
    """Calcule le nombre de permanences à effectuer pour chaque bénévole"""
    benevoles = Benevole.objects.filter(is_active=True)
    permanences = Permanence.objects.filter(is_filled=False)

    # Nombre total de permanences non attribuées
    total_permanences = permanences.count()

    # Nombre de bénévoles actifs
    total_benevoles = benevoles.count()

    if total_benevoles == 0:
        return {}  # Aucun bénévole actif

    # Calcul du nombre moyen de permanences par bénévole
    avg_permanences = ceil(total_permanences / total_benevoles)

    # Créez un dictionnaire pour stocker les permanences par bénévole
    permanences_by_benevole = {}

    for benevole in benevoles:
        # Initialisez chaque bénévole avec le nombre moyen de permanences
        permanences_by_benevole[benevole] = avg_permanences

    return permanences_by_benevole


#---------------------------------------------------------------------------------
@login_required
def saisie(request):
    """Permet aux bénévoles de saisir leurs informations, génère un planning et détecte les conflits"""
    benevole = Benevole.objects.get(user=request.user)

    # Étape 1 : Saisie des contraintes et préférences
    if request.method == 'POST':
        form = BenevoleForm(request.POST, instance=benevole)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos contraintes et préférences ont été enregistrées.")
        else:
            messages.error(request, "Une erreur est survenue lors de l'enregistrement de vos informations.")
    else:
        form = BenevoleForm(instance=benevole)

    # Étape 2 : Calcul des permanences
    permanences_by_benevole = calculate_permanences()

    # Étape 3 : Génération du planning
    benevoles = Benevole.objects.filter(is_active=True)
    permanences = Permanence.objects.filter(is_filled=False).order_by('date')
    planning = []
    conflicts = []

    for permanence in permanences:
        assigned = False
        for benevole in benevoles:
            constraints = benevole.constraints or {}
            preferences = benevole.preferences or {}

            # Vérifiez si le bénévole est disponible pour cette permanence
            if permanence.time_slot in constraints.get(permanence.date.strftime('%A'), []):
                # Vérifiez si le bénévole n'a pas dépassé son quota
                if permanences_by_benevole[benevole] > 0:
                    permanence.benevole = benevole
                    permanence.is_filled = True
                    permanence.save()
                    benevole.nb_permanences += 1
                    benevole.save()
                    permanences_by_benevole[benevole] -= 1
                    planning.append(permanence)
                    assigned = True
                    break

        if not assigned:
            conflicts.append(permanence)

    # Étape 4 : Détection des conflits et solutions
    solutions = []
    for conflict in conflicts:
        solutions.append({
            'permanence': conflict,
            'possible_benevoles': Benevole.objects.filter(is_active=True),
        })

    return render(request, 'benvoplanify/saisie.html', {
        'form': form,
        'planning': planning,
        'conflicts': conflicts,
        'solutions': solutions,
    })