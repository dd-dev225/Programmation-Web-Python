from django.contrib import admin          # ← ← ← IL MANQUE CETTE LIGNE
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),      # ← maintenant ça marche
    path('dashboard/', include('dashboard.urls')),   # ou ventes.urls
    # tes autres paths si besoin
]