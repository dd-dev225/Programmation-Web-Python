# Guide Exercice : Gestion des Groupes d'Utilisateurs et Contrôle d'Accès

> **Objectif de l'exercice** : Implémenter un système complet de gestion des groupes d'utilisateurs avec contrôle d'accès et gestion des sessions dans Django.

---

## Table des Matières

1. [Objectifs Pédagogiques](#1-objectifs-pédagogiques)
2. [Prérequis](#2-prérequis)
3. [Étape 1 : Création des Groupes](#3-étape-1--création-des-groupes)
4. [Étape 2 : Création des Décorateurs de Contrôle d'Accès](#4-étape-2--création-des-décorateurs-de-contrôle-daccès)
5. [Étape 3 : Gestion des Sessions](#5-étape-3--gestion-des-sessions)
6. [Étape 4 : Modification des Vues](#6-étape-4--modification-des-vues)
7. [Étape 5 : Configuration des URLs](#7-étape-5--configuration-des-urls)
8. [Étape 6 : Création des Templates de Gestion](#8-étape-6--création-des-templates-de-gestion)
9. [Étape 7 : Configuration Admin](#9-étape-7--configuration-admin)
10. [Tests et Validation](#10-tests-et-validation)

---

## 1. Objectifs Pédagogiques

À la fin de cet exercice, vous saurez :

- **Créer des groupes d'utilisateurs** avec Django's auth system
- **Attribuer des permissions** différentes selon les groupes
- **Restreindre l'accès** aux vues avec des décorateurs personnalisés
- **Gérer les variables de session** à la connexion/déconnexion
- **Créer des interfaces** pour administrer utilisateurs et groupes

### Groupes à Créer

| Groupe | Permissions | Accès |
|--------|-------------|-------|
| **Administrateurs** | Toutes (add, change, delete, view) | Tableau de bord + Gestion |
| **Utilisateurs Standard** | Lecture seule (view) | Tableau de bord uniquement |

---

## 2. Prérequis

Votre projet Django doit avoir :
- Une application `dashboard` existante
- Le système d'authentification Django activé (`django.contrib.auth` dans `INSTALLED_APPS`)
- Des modèles définis (Segment, Produit, etc.)

---

## 3. Étape 1 : Création des Groupes

### Pourquoi créer des groupes ?

> **Justification** : Django fournit un système de groupes natif via `django.contrib.auth.models.Group`. Les groupes permettent de regrouper des utilisateurs avec des permissions communes, évitant d'assigner des permissions individuellement à chaque utilisateur.

### 3.1 Méthode via le Shell Django

Ouvrez le terminal et exécutez :

```bash
python manage.py shell
```

Puis tapez le code suivant :

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Pourquoi get_or_create ? → Évite les erreurs si le groupe existe déjà
administrateurs, created = Group.objects.get_or_create(name='Administrateurs')
utilisateurs_standard, created = Group.objects.get_or_create(name='Utilisateurs Standard')

print(f"Groupes créés : Administrateurs={administrateurs.id}, Utilisateurs Standard={utilisateurs_standard.id}")
```

### 3.2 Attribution des Permissions

```python
# Récupérer toutes les permissions existantes
all_permissions = Permission.objects.all()

# Permissions de lecture uniquement (commencent par 'view_')
view_permissions = Permission.objects.filter(codename__startswith='view_')

# Pourquoi cette approche ?
# → Les permissions Django suivent le format : add_model, change_model, delete_model, view_model
# → En filtrant sur 'view_', on obtient uniquement les permissions de consultation

# Assigner toutes les permissions aux Administrateurs
administrateurs.permissions.set(all_permissions)

# Assigner uniquement les permissions de lecture aux Utilisateurs Standard
utilisateurs_standard.permissions.set(view_permissions)

print(f"Administrateurs : {administrateurs.permissions.count()} permissions")
print(f"Utilisateurs Standard : {utilisateurs_standard.permissions.count()} permissions")
```

### 3.3 Création d'Utilisateurs de Test

```python
from django.contrib.auth.models import User

# Créer un administrateur
# Pourquoi is_staff=True ? → Permet l'accès à l'interface admin Django
admin_user = User.objects.create_user(
    username='admin_test',
    email='admin@test.com',
    password='Admin@123',
    first_name='Admin',
    last_name='Test'
)
admin_user.is_staff = True
admin_user.save()
admin_user.groups.add(administrateurs)

# Créer un utilisateur standard
# Pourquoi is_staff=False (défaut) ? → Pas d'accès à l'admin Django
standard_user = User.objects.create_user(
    username='user_test',
    email='user@test.com',
    password='User@123',
    first_name='User',
    last_name='Test'
)
standard_user.groups.add(utilisateurs_standard)

print("Utilisateurs créés avec succès!")
```

---

## 4. Étape 2 : Création des Décorateurs de Contrôle d'Accès

### Pourquoi des décorateurs personnalisés ?

> **Justification** : Django fournit `@login_required` et `@permission_required`, mais ils ne vérifient pas l'appartenance à un groupe. Créer nos propres décorateurs permet un contrôle précis basé sur les groupes, avec des messages d'erreur personnalisés.

### 4.1 Créer le fichier `dashboard/decorators.py`

```python
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps


def group_required(*group_names):
    """
    Décorateur vérifiant l'appartenance à un ou plusieurs groupes.
    
    Pourquoi *group_names (tuple) ?
    → Permet de spécifier plusieurs groupes : @group_required('Admin', 'Manager')
    → L'utilisateur doit appartenir à AU MOINS UN des groupes listés
    
    Usage:
        @group_required('Administrateurs', 'Utilisateurs Standard')
        def ma_vue(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)  # Préserve le nom et la docstring de la fonction originale
        @login_required   # Vérifie d'abord que l'utilisateur est connecté
        def wrapper(request, *args, **kwargs):
            # Récupérer les noms des groupes de l'utilisateur
            user_groups = request.user.groups.values_list('name', flat=True)
            
            # Pourquoi vérifier is_superuser ?
            # → Le superuser a tous les droits, même sans groupe
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Vérifier si l'utilisateur appartient à au moins un groupe requis
            if any(group in user_groups for group in group_names):
                return view_func(request, *args, **kwargs)
            else:
                # Pourquoi PermissionDenied ?
                # → Django affiche automatiquement une page 403 Forbidden
                raise PermissionDenied("Vous n'avez pas les permissions nécessaires.")
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Décorateur spécifique pour les administrateurs uniquement.
    
    Pourquoi un décorateur séparé ?
    → Plus lisible que @group_required('Administrateurs') répété partout
    → Intention claire dans le code
    
    Usage:
        @admin_required
        def vue_admin(request):
            ...
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        # Vérification superuser OU groupe Administrateurs
        is_admin = (
            request.user.is_superuser or 
            request.user.groups.filter(name='Administrateurs').exists()
        )
        
        if is_admin:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied("Accès réservé aux administrateurs.")
    
    return wrapper
```

---

## 5. Étape 3 : Gestion des Sessions

### Pourquoi gérer les sessions manuellement ?

> **Justification** : Django gère automatiquement la session d'authentification, mais pour des données personnalisées (groupes, heure de connexion, etc.), il faut les stocker manuellement. Un middleware permet de le faire automatiquement à chaque requête.

### 5.1 Créer le fichier `dashboard/middleware.py`

```python
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime


class UserSessionMiddleware(MiddlewareMixin):
    """
    Middleware gérant les variables de session personnalisées.
    
    Pourquoi un middleware ?
    → Exécuté automatiquement à CHAQUE requête
    → Pas besoin de répéter le code dans chaque vue
    → Centralise la logique de session
    
    Variables créées :
    - user_session_data : dict avec infos utilisateur
    - last_activity : timestamp de dernière activité
    """
    
    def process_request(self, request):
        """
        Appelé AVANT que la vue ne soit exécutée.
        """
        # Vérifier que l'utilisateur est authentifié
        if request.user.is_authenticated:
            
            # Créer les données de session si première visite après connexion
            if 'user_session_data' not in request.session:
                # Pourquoi stocker ces données ?
                # → Évite des requêtes DB répétées pour avoir les groupes
                # → Permet d'afficher les infos dans les templates
                request.session['user_session_data'] = {
                    'user_id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'groups': list(request.user.groups.values_list('name', flat=True)),
                    'login_time': datetime.now().isoformat(),
                    'is_admin': (
                        request.user.groups.filter(name='Administrateurs').exists() or 
                        request.user.is_superuser
                    ),
                }
                # Pourquoi modified = True ?
                # → Indique à Django de sauvegarder la session
                request.session.modified = True
            
            # Mettre à jour l'heure de dernière activité
            request.session['last_activity'] = datetime.now().isoformat()
        
        return None  # Continue le traitement normal
    
    def process_response(self, request, response):
        """
        Appelé APRÈS que la vue ait renvoyé une réponse.
        """
        return response  # Pas de modification de la réponse
```

### 5.2 Activer le Middleware

Dans `DjangoProject/settings.py`, ajouter à la fin de `MIDDLEWARE` :

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Pourquoi en dernier ?
    # → Doit être après AuthenticationMiddleware pour que request.user existe
    'dashboard.middleware.UserSessionMiddleware',
]
```

---

## 6. Étape 4 : Modification des Vues

### 6.1 Importer les décorateurs et modifier les vues existantes

Dans `dashboard/views.py`, ajouter en haut :

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from datetime import datetime

# Importer nos décorateurs personnalisés
from .decorators import group_required, admin_required
```

### 6.2 Protéger les vues existantes

```python
# Pourquoi deux décorateurs ?
# → @login_required : vérifie que l'utilisateur est connecté
# → @group_required : vérifie l'appartenance au groupe
# L'ordre est important : login_required est intégré dans group_required

@login_required
@group_required('Administrateurs', 'Utilisateurs Standard')
def dashboard_1(request):
    """Dashboard principal - Accessible aux deux groupes"""
    # ... votre code existant ...
    
    # Ajouter au context pour utilisation dans le template
    context['is_admin'] = (
        request.user.groups.filter(name='Administrateurs').exists() or 
        request.user.is_superuser
    )
    return render(request, "dashboard/dashboard_1.html", context)
```

### 6.3 Créer les vues de gestion (Admin uniquement)

```python
@login_required
@admin_required  # Pourquoi pas group_required ? → Plus explicite pour "admin only"
def gestion_utilisateurs(request):
    """
    Gestion des utilisateurs - ADMIN UNIQUEMENT
    
    Pourquoi prefetch_related('groups') ?
    → Optimise les requêtes : charge les groupes en une seule requête
    → Sans ça, Django ferait une requête par utilisateur pour ses groupes
    """
    users = User.objects.all().prefetch_related('groups')
    
    context = {
        'users': users,
        'is_admin': True,
    }
    return render(request, 'dashboard/gestion_utilisateurs.html', context)


@login_required
@admin_required
def gestion_groupes(request):
    """Gestion des groupes - ADMIN UNIQUEMENT"""
    groups = Group.objects.all().prefetch_related('permissions')
    
    context = {
        'groups': groups,
        'is_admin': True,
    }
    return render(request, 'dashboard/gestion_groupes.html', context)
```

### 6.4 Vues de connexion/déconnexion personnalisées

```python
def custom_login(request):
    """
    Vue de connexion avec création de variables de session.
    
    Pourquoi une vue personnalisée au lieu de auth_views.LoginView ?
    → Contrôle total sur la création des variables de session
    → Messages flash personnalisés
    → Redirection personnalisée
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Créer les variables de session personnalisées
            # Pourquoi ici et pas dans le middleware ?
            # → Le middleware s'exécute à chaque requête
            # → Ici, on initialise au moment exact de la connexion
            request.session['user_session_data'] = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'groups': list(user.groups.values_list('name', flat=True)),
                'login_time': datetime.now().isoformat(),
                'is_admin': (
                    user.groups.filter(name='Administrateurs').exists() or 
                    user.is_superuser
                ),
            }
            
            messages.success(request, f'Bienvenue {user.username}!')
            return redirect('dashboard:dashboard_1')
        else:
            messages.error(request, 'Identifiant ou mot de passe incorrect.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard/login2.html', {'form': form})


def custom_logout(request):
    """
    Vue de déconnexion avec suppression des variables de session.
    
    Pourquoi supprimer manuellement les variables ?
    → logout() supprime la session d'auth mais pas nos variables custom
    → Assure un nettoyage complet
    """
    username = request.user.username if request.user.is_authenticated else "Utilisateur"
    
    # Supprimer les variables de session personnalisées
    if 'user_session_data' in request.session:
        del request.session['user_session_data']
    
    if 'last_activity' in request.session:
        del request.session['last_activity']
    
    # Déconnexion Django (supprime la session d'auth)
    logout(request)
    
    messages.info(request, f'Au revoir {username}!')
    return redirect('dashboard:login')
```

---

## 7. Étape 5 : Configuration des URLs

Dans `dashboard/urls.py` :

```python
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'dashboard'

urlpatterns = [
    # Dashboards (accessibles aux deux groupes)
    path("", views.dashboard_1, name="dashboard_1"),
    path("dashbord_2/", views.dashboard_2, name="dashboard_2"),
    path("<str:segment>/liste/", views.segmentliste, name="segmentliste"),
    
    # Gestion (Admin uniquement)
    # Pourquoi un préfixe 'gestion/' ?
    # → Organise logiquement les URLs d'administration
    # → Facilite le contrôle d'accès par URL si besoin
    path('gestion/utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('gestion/groupes/', views.gestion_groupes, name='gestion_groupes'),
    
    # Authentification personnalisée
    # Pourquoi views.custom_login au lieu de auth_views.LoginView ?
    # → Gestion personnalisée des sessions comme expliqué plus haut
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', TemplateView.as_view(template_name='dashboard/register2.html'), name='register'),
]
```

---

## 8. Étape 6 : Création des Templates de Gestion

### 8.1 Template `gestion_utilisateurs.html`

Créer `dashboard/templates/dashboard/gestion_utilisateurs.html` :

```html
{% extends 'dashboard/base.html' %}
{% block title %}Gestion des Utilisateurs{% endblock %}

{% block content %}
<div class="white-box">
    <h3>Gestion des Utilisateurs</h3>
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Groupes</th>
                <th>Statut</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for user in users %}
            <tr>
                <td>{{ user.username }}</td>
                <td>{{ user.email|default:"-" }}</td>
                <td>
                    {# Pourquoi user.groups.all ? #}
                    {# → Récupère tous les groupes de l'utilisateur #}
                    {% for group in user.groups.all %}
                    <span class="label label-info">{{ group.name }}</span>
                    {% empty %}
                    <em>Aucun groupe</em>
                    {% endfor %}
                </td>
                <td>
                    {% if user.is_superuser %}
                    <span class="label label-danger">Superuser</span>
                    {% elif user.is_staff %}
                    <span class="label label-warning">Staff</span>
                    {% else %}
                    <span class="label label-default">Standard</span>
                    {% endif %}
                </td>
                <td>
                    {# Pourquoi lien vers /admin/ ? #}
                    {# → Réutilise l'interface admin Django existante #}
                    <a href="/admin/auth/user/{{ user.id }}/change/">Modifier</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <a href="/admin/auth/user/add/" class="btn btn-success">Ajouter</a>
</div>
{% endblock %}
```

### 8.2 Template `gestion_groupes.html`

Créer `dashboard/templates/dashboard/gestion_groupes.html` :

```html
{% extends 'dashboard/base.html' %}
{% block title %}Gestion des Groupes{% endblock %}

{% block content %}
<div class="white-box">
    <h3>Gestion des Groupes</h3>
    
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Nom du Groupe</th>
                <th>Utilisateurs</th>
                <th>Permissions</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for group in groups %}
            <tr>
                <td><strong>{{ group.name }}</strong></td>
                <td>{{ group.user_set.count }} utilisateur(s)</td>
                <td>{{ group.permissions.count }} permission(s)</td>
                <td>
                    <a href="/admin/auth/group/{{ group.id }}/change/">Modifier</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <a href="/admin/auth/group/add/" class="btn btn-success">Ajouter</a>
</div>
{% endblock %}
```

---

## 9. Étape 7 : Configuration Admin

Dans `dashboard/admin.py`, améliorer l'affichage :

```python
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    """
    Pourquoi personnaliser UserAdmin ?
    → Afficher les groupes directement dans la liste des utilisateurs
    → Faciliter la gestion sans ouvrir chaque utilisateur
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    
    def get_groups(self, obj):
        """Retourne les groupes de l'utilisateur sous forme de chaîne"""
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groupes'  # Titre de la colonne


# Pourquoi unregister puis register ?
# → User est déjà enregistré par Django
# → On doit le retirer avant d'ajouter notre version personnalisée
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
```

---

## 10. Tests et Validation

### 10.1 Vérifications à Effectuer

1. **Accès admin_test** :
   - URL : `http://127.0.0.1:8000/dashboard/login/`
   - Doit pouvoir accéder à `/dashboard/gestion/utilisateurs/`
   - Doit pouvoir accéder à `/dashboard/gestion/groupes/`

2. **Accès user_test** :
   - Doit pouvoir accéder au dashboard
   - Doit recevoir erreur 403 sur `/dashboard/gestion/utilisateurs/`

3. **Sessions** :
   - Après connexion, `request.session['user_session_data']` doit exister
   - Après déconnexion, cette variable doit être supprimée

### 10.2 Commandes de Test (Shell)

```python
# Vérifier les groupes
from django.contrib.auth.models import Group
for g in Group.objects.all():
    print(f"{g.name}: {g.permissions.count()} perms, {g.user_set.count()} users")

# Vérifier l'appartenance d'un utilisateur
from django.contrib.auth.models import User
user = User.objects.get(username='admin_test')
print(f"Groupes: {list(user.groups.values_list('name', flat=True))}")
print(f"Est admin: {user.groups.filter(name='Administrateurs').exists()}")
```

---

## Résumé des Fichiers à Créer/Modifier

| Fichier | Action |
|---------|--------|
| `dashboard/decorators.py` | **CRÉER** - Décorateurs de contrôle d'accès |
| `dashboard/middleware.py` | **CRÉER** - Middleware de session |
| `dashboard/views.py` | **MODIFIER** - Ajouter décorateurs et nouvelles vues |
| `dashboard/urls.py` | **MODIFIER** - Ajouter routes gestion |
| `dashboard/admin.py` | **MODIFIER** - Personnaliser affichage User |
| `DjangoProject/settings.py` | **MODIFIER** - Ajouter middleware |
| `dashboard/templates/dashboard/gestion_utilisateurs.html` | **CRÉER** |
| `dashboard/templates/dashboard/gestion_groupes.html` | **CRÉER** |

---

## Utilisateurs de Test

| Username | Password | Groupe | Accès |
|----------|----------|--------|-------|
| admin_test | Admin@123 | Administrateurs | Tout + Gestion |
| user_test | User@123 | Utilisateurs Standard | Dashboard uniquement |
