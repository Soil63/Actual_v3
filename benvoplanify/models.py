from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naiss = models.DateField()
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'date_naiss']

    def __str__(self):
        return self.email


'''class Benevole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_naiss = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"'''
    

class Benevole(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Relation 1-1 avec CustomUser
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_naiss = models.DateField()



    #constraints et preferences :
#Ces champs permettent de stocker des données structurées (comme des jours ou des heures) sous forme de dictionnaire JSON.
#Exemple de valeur pour constraints :
#{"indisponibilites": ["Lundi matin", "Vendredi après-midi"]}
    constraints = models.JSONField(default=dict, blank=True)  # Stocke les contraintes sous forme de dictionnaire
    preferences = models.JSONField(default=dict, blank=True)  # Stocke les préférences sous forme de dictionnaire
    
    
    #Utile pour suivre le nombre de permanences effectuées par le bénévole.
    nb_permanences = models.PositiveIntegerField(default=0)  # Nombre de permanences effectuées
    
    #is_active : Permet de désactiver un bénévole sans le supprimer.
    is_active = models.BooleanField(default=True)  # Statut actif/inactif
    
    #phone_number et address : Fournissent des informations de contact supplémentaires.
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Numéro de téléphone
    address = models.TextField(blank=True, null=True)  # Adresse du bénévole
    
    #joined_date : Permet de savoir depuis quand le bénévole est inscrit.
    joined_date = models.DateField(auto_now_add=True)  # Date d'inscription
    
    #volontaire_plus : Indique si le bénévole est volontaire pour effectuer plus de permanences que prévu.
    volontaire_plus = models.BooleanField(default=False)  # Volontaire pour plus de permanences


    def __str__(self):
        return f"{self.prenom} {self.nom}"
#-------------------------------------------------

class Permanence(models.Model):
    date = models.DateField()
    time_slot = models.CharField(max_length=50)  # Matin, Après-midi
    benevole = models.ForeignKey(Benevole, on_delete=models.SET_NULL, null=True, blank=True)
    is_filled = models.BooleanField(default=False)
    #im not sure about this one
    
    def __str__(self):
        return f"Permanence {self.date} - {self.time_slot}"


    
    #-------------------------------------------------
class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilise le modèle utilisateur personnalisé
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilise le modèle utilisateur personnalisé
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message de {self.sender.email} à {self.receiver.email}"

    #-------------------------------------------------

