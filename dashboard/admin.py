from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Client, Localite, Produit, Commande, Ligne


class CustomUserAdmin(BaseUserAdmin):
    """Affichage personnalisé des utilisateurs avec les groupes visibles"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groupes'


# Remplacement de l'admin User par défaut
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Enregistrement des modèles métier
admin.site.register(Client)
admin.site.register(Localite)
admin.site.register(Produit)
admin.site.register(Commande)
admin.site.register(Ligne)