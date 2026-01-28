from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'dashboard'

urlpatterns = [
    # Dashboards - Accessibles aux deux groupes
    path("", views.dashboard_1, name="dashboard_1"),
    path("dashbord_2/", views.dashboard_2, name="dashboard_2"),
    path("<str:segment>/liste/", views.segmentliste, name="segmentliste"),
    
    # Gestion - Administrateurs uniquement
    path('gestion/utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('gestion/groupes/', views.gestion_groupes, name='gestion_groupes'),
    
    # Authentification personnalisée
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', TemplateView.as_view(template_name='dashboard/register2.html'), name='register'),
]
