# planning/admin.py
#from django.contrib import admin

from django.contrib import admin
from .models import Benevole

@admin.register(Benevole)
class BenevoleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'is_active', 'nb_permanences', 'volontaire_plus']
    list_filter = ['is_active', 'volontaire_plus']
    search_fields = ['nom', 'prenom', 'email']





# Register your models here.
