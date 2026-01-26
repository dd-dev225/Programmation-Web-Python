from django.contrib import admin
from .models import Client, Localite, Produit, Commande, Ligne

# Enregistrement simple (sans surcharge personnalisée)
admin.site.register(Client)
admin.site.register(Localite)
admin.site.register(Produit)
admin.site.register(Commande)
admin.site.register(Ligne)