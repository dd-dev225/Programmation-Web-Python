
#1# Créer un fichier nommé urls.py dans votre application et inserer le code suivant:
from django.urls import path
from . import views

app_name = 'dashboard'   # ← IMPORTANT Car permettant de spécifier le namespace de l'application pour définir les urls dans les pages web

urlpatterns = [
    path("", views.dashboard_1, name="dashboard_1"),
    path("dashbord_2", views.dashboard_2, name="dashboard_2"),
    path("<str:segment>/liste/", views.segmentliste, name="segmentliste"),
]