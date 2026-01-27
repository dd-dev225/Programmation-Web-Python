from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'dashboard'   # ← IMPORTANT Car permettant de spécifier le namespace de l'application pour définir les urls dans les pages web

urlpatterns = [
    path("", views.dashboard_1, name="dashboard_1"),
    path("dashbord_2", views.dashboard_2, name="dashboard_2"),
    path("<str:segment>/liste/", views.segmentliste, name="segmentliste"),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard:login'), name='logout'),
]
