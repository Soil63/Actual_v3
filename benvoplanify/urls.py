from django.contrib import admin
from django.urls import include, path
from benvoplanify import views  
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', views.index, name='index'),  # Example root view
    path('home/', views.home, name='home'), # added
    path('register/', views.register, name='register'),
    path('success/', views.success, name='success'),
    path('espace-personnel/', views.espace_perso, name='espace_perso'),
    path('modifier-benevole/',views.modif_benev, name='modif_benev'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout_view,name='logout'),
    
    
    

    path('messagerie/', views.messagerie, name='messagerie'),
    path('messagerie/<int:message_id>/', views.messagerie, name='messagerie'),

    
    path('saisie/', views.saisie, name='saisie'),
    
]
