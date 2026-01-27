# Guide Complet du Projet Django - De Zéro à Production

> **Objectif** : Ce guide permet à toute personne de comprendre et reproduire l'ensemble du projet depuis l'installation initiale jusqu'à l'état actuel.

---

## Table des Matières

1. [Préparation de l'Environnement](#1-préparation-de-lenvironnement)
2. [Création du Projet Django](#2-création-du-projet-django)
3. [Configuration Multi-Base de Données](#3-configuration-multi-base-de-données)
4. [Création de l'Application Dashboard](#4-création-de-lapplication-dashboard)
5. [Modèles de Données](#5-modèles-de-données)
6. [Système d'Authentification](#6-système-dauthentification)
7. [Intégration des Templates](#7-intégration-des-templates)
8. [Fichiers Statiques](#8-fichiers-statiques)
9. [Migration vers Login2/Register2](#9-migration-vers-login2register2)
10. [Déploiement et Collaboration](#10-déploiement-et-collaboration)

---

## 1. Préparation de l'Environnement

### 1.1 Installation Python
- **Version requise** : Python 3.9+
- Vérifier l'installation : `python --version`

### 1.2 Création de l'Environnement Virtuel
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 1.3 Installation des Dépendances
Créer `requirements.txt` :
```txt
Django==5.1.4
python-dotenv==1.0.1
PyMySQL==1.1.1
psycopg2-binary==2.9.10
```

Installer :
```bash
pip install -r requirements.txt
```

---

## 2. Création du Projet Django

### 2.1 Initialisation
```bash
django-admin startproject DjangoProject .
```

### 2.2 Structure Initiale
```
DjangoProject/
├── DjangoProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── .venv/
```

---

## 3. Configuration Multi-Base de Données

### 3.1 Fichier `.env`
Créer à la racine du projet :
```env
# Configuration Base de Données
DB_ENGINE=mysql          # ou postgresql
DB_NAME=data_pwp
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306             # 3306 pour MySQL, 5432 pour PostgreSQL

# Django
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3.2 Modification de `settings.py`
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost').split(',')]

# Charger pymysql pour MySQL
DB_ENGINE = os.getenv('DB_ENGINE', 'mysql')
if DB_ENGINE == 'mysql':
    import pymysql
    pymysql.install_as_MySQLdb()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',  # Notre application
]

# Configuration base de données dynamique
DB_ENGINES = {
    'mysql': 'django.db.backends.mysql',
    'postgresql': 'django.db.backends.postgresql',
}

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINES.get(DB_ENGINE, DB_ENGINES['mysql']),
        'NAME': os.getenv('DB_NAME', 'data_pwp'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306' if DB_ENGINE == 'mysql' else '5432'),
    }
}

if DB_ENGINE == 'mysql':
    DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = 'static/'

# Redirections après authentification
LOGIN_REDIRECT_URL = 'dashboard:dashboard_1'
LOGOUT_REDIRECT_URL = 'dashboard:login'
```

### 3.3 `.gitignore`
```gitignore
.env
*.pyc
__pycache__/
.venv/
db.sqlite3
*.log
.idea/
.vscode/
```

---

## 4. Création de l'Application Dashboard

### 4.1 Commande de Création
```bash
python manage.py startapp dashboard
```

### 4.2 Enregistrement dans `settings.py`
Ajouter `'dashboard'` dans `INSTALLED_APPS` (déjà fait ci-dessus).

### 4.3 Structure de l'App
```
dashboard/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py (à créer)
├── migrations/
├── templates/
│   └── dashboard/
│       ├── login2.html
│       ├── register2.html
│       ├── dashboard_1.html
│       └── dashboard_2.html
└── static/
    ├── css/
    ├── js/
    └── plugins/
```

---

## 5. Modèles de Données

### 5.1 Fichier `dashboard/models.py`
```python
from django.db import models

class Segment(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='produits')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nom
```

### 5.2 Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5.3 Enregistrement Admin (`dashboard/admin.py`)
```python
from django.contrib import admin
from .models import Segment, Produit

@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'segment', 'stock')
    list_filter = ('segment',)
```

---

## 6. Système d'Authentification

### 6.1 Configuration dans `DjangoProject/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
]
```

### 6.2 URLs de Dashboard (`dashboard/urls.py`)
```python
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = 'dashboard'

urlpatterns = [
    path("", views.dashboard_1, name="dashboard_1"),
    path("dashbord_2", views.dashboard_2, name="dashboard_2"),
    path("<str:segment>/liste/", views.segmentliste, name="segmentliste"),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login2.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='dashboard/register2.html'), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard:login'), name='logout'),
]
```

### 6.3 Vues (`dashboard/views.py`)
```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Segment, Produit

@login_required
def dashboard_1(request):
    segments = Segment.objects.all()
    return render(request, 'dashboard/dashboard_1.html', {'segments': segments})

@login_required
def dashboard_2(request):
    return render(request, 'dashboard/dashboard_2.html')

@login_required
def segmentliste(request, segment):
    produits = Produit.objects.filter(segment__nom=segment)
    return render(request, 'dashboard/segment_liste.html', {
        'segment': segment,
        'produits': produits
    })
```

### 6.4 Création d'un Superutilisateur
```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@exemple.com
# Password: [votre mot de passe]
```

---

## 7. Intégration des Templates

### 7.1 Template Login (`dashboard/templates/dashboard/login2.html`)

**Points clés** :
- Utilisation de `{% load static %}` en haut du fichier
- Tous les chemins vers CSS/JS/Images utilisent `{% static '...' %}`
- Formulaire Django avec `{% csrf_token %}`
- Affichage des erreurs avec `{% if form.errors %}`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% load static %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Connexion - Dashboard</title>
    
    <!-- CSS -->
    <link href="{% static 'bootstrap/dist/css/bootstrap.min.css' %}" rel="stylesheet">
    <link href="{% static 'css/style.css' %}" rel="stylesheet">
    
    <!-- Background inline pour éviter problèmes de chemins CSS -->
    <style>
        .login-register {
            background: url("{% static 'plugins/images/login-register.jpg' %}") center center/cover no-repeat !important;
            height: 100%;
            position: fixed;
        }
    </style>
</head>
<body>
    <section id="wrapper" class="login-register">
        <div class="login-box login-sidebar">
            <div class="white-box">
                <form class="form-horizontal form-material" method="post">
                    {% csrf_token %}
                    
                    <a href="javascript:void(0)" class="text-center db">
                        <img src="{% static 'plugins/images/admin-logo-dark.png' %}" alt="Logo" />
                    </a>
                    
                    {% if form.errors %}
                    <div class="alert alert-danger m-t-20">
                        Identifiant ou mot de passe incorrect.
                    </div>
                    {% endif %}
                    
                    <div class="form-group m-t-40">
                        <div class="col-xs-12">
                            <input class="form-control" type="text" name="username" 
                                   required placeholder="Username">
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <div class="col-xs-12">
                            <input class="form-control" type="password" name="password" 
                                   required placeholder="Password">
                        </div>
                    </div>
                    
                    <div class="form-group text-center m-t-20">
                        <div class="col-xs-12">
                            <button class="btn btn-info btn-lg btn-block" type="submit">
                                Log In
                            </button>
                        </div>
                    </div>
                    
                    <div class="form-group m-b-0">
                        <div class="col-sm-12 text-center">
                            <p>Don't have an account? 
                                <a href="{% url 'dashboard:register' %}" class="text-primary">
                                    <b>Sign Up</b>
                                </a>
                            </p>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </section>
    
    <!-- Scripts -->
    <script src="{% static 'plugins/bower_components/jquery/dist/jquery.min.js' %}"></script>
    <script src="{% static 'bootstrap/dist/js/bootstrap.min.js' %}"></script>
</body>
</html>
```

### 7.2 Template Register (`dashboard/templates/dashboard/register2.html`)
Structure similaire à `login2.html` avec formulaire d'inscription.

---

## 8. Fichiers Statiques

### 8.1 Organisation
```
dashboard/static/
├── bootstrap/
├── css/
│   ├── style.css
│   ├── animate.css
│   └── colors/
├── js/
│   ├── custom.min.js
│   └── waves.js
└── plugins/
    ├── images/
    │   ├── admin-logo-dark.png
    │   ├── login-register.jpg
    │   └── favicon.png
    └── bower_components/
```

### 8.2 Configuration
Déjà configuré dans `settings.py` :
```python
STATIC_URL = 'static/'
```

### 8.3 Important : Chemins Relatifs vs Absolus
**Problème rencontré** : Les chemins relatifs dans `style.css` (`../../plugins/images/...`) ne fonctionnaient pas correctement.

**Solution** : Injection du CSS background directement dans le template HTML avec `{% static %}` pour garantir la résolution absolue du chemin.

---

## 9. Migration vers Login2/Register2

### 9.1 Contexte
Renommage de `login.html` → `login2.html` et création de `register2.html` avec ajustements.

### 9.2 Étapes Réalisées

#### 9.2.1 Renommage du Template
```bash
mv dashboard/Templates/dashboard/login.html dashboard/templates/dashboard/login2.html
```

#### 9.2.2 Standardisation du Dossier
Renommé `Templates` → `templates` (minuscule) pour respecter les conventions Django.

#### 9.2.3 Mise à Jour des URLs
Dans `dashboard/urls.py` :
```python
path('login/', auth_views.LoginView.as_view(template_name='dashboard/login2.html'), name='login'),
```

#### 9.2.4 Correction des Namespaces
Tous les liens utilisent maintenant le namespace `dashboard:` :
- Dans `login2.html` : `{% url 'dashboard:register' %}`
- Dans `register2.html` : `{% url 'dashboard:login' %}`

---

## 10. Déploiement et Collaboration

### 10.1 Configuration Git
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/votre-username/votre-repo.git
git push -u origin main
```

### 10.2 Fichier `.env.example`
Créer pour partager la structure sans exposer les secrets :
```env
# Configuration Base de Données
DB_ENGINE=mysql
DB_NAME=nom_base
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=3306

# Django
SECRET_KEY=votre-clé-secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 10.3 Instructions pour Nouveaux Collaborateurs

#### Cloner le Projet
```bash
git clone https://github.com/votre-username/votre-repo.git
cd votre-repo
```

#### Créer l'Environnement
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# ou
.venv\Scripts\activate  # Windows
```

#### Installer les Dépendances
```bash
pip install -r requirements.txt
```

#### Configurer `.env`
Copier `.env.example` vers `.env` et ajuster les valeurs.

#### Créer la Base de Données
```sql
-- MySQL
CREATE DATABASE data_pwp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- PostgreSQL
CREATE DATABASE data_pwp ENCODING 'UTF8';
```

#### Migrer et Lancer
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Accéder à : `http://127.0.0.1:8000/dashboard/login/`

---

## 11. Problèmes Courants et Solutions

### 11.1 Image de Fond Non Visible
**Symptôme** : L'image `login-register.jpg` ne s'affiche pas.

**Cause** : Chemins relatifs CSS incorrects selon l'URL.

**Solution** : Utiliser `{% static %}` dans un `<style>` inline du template.

### 11.2 NoReverseMatch Error
**Symptôme** : Erreur lors du clic sur les liens entre pages.

**Cause** : Namespace manquant dans les `{% url %}`.

**Solution** : Utiliser `{% url 'dashboard:nom_vue' %}` au lieu de `{% url 'nom_vue' %}`.

### 11.3 TemplateDoesNotExist
**Symptôme** : Django ne trouve pas le template.

**Cause** : 
- Dossier `Templates` avec majuscule au lieu de `templates`
- Mauvais chemin dans `urls.py`

**Solution** : 
- Renommer en `templates` (minuscule)
- Vérifier `template_name='dashboard/login2.html'`

### 11.4 Static Files Non Chargés
**Symptôme** : CSS/JS ne se chargent pas.

**Cause** : `{% load static %}` manquant ou chemins incorrects.

**Solution** : 
- Ajouter `{% load static %}` en haut du template
- Utiliser `{% static 'chemin/fichier' %}` pour tous les assets

---

## 12. Commandes Utiles

```bash
# Lancer le serveur de développement
python manage.py runserver

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques (production)
python manage.py collectstatic

# Shell Django
python manage.py shell

# Vérifier la configuration
python manage.py check
```

---

## 13. Architecture Finale

```
DjangoProject/
├── .env                         # Config locale (non versionné)
├── .env.example                 # Template de config
├── .gitignore
├── requirements.txt
├── manage.py
├── GUIDE_COMPLET_PROJET.md     # Ce document
├── DjangoProject/
│   ├── settings.py             # Configuration flexible
│   ├── urls.py                 # Routes principales
│   └── wsgi.py
└── dashboard/
    ├── models.py               # Segment, Produit
    ├── views.py                # Vues protégées
    ├── urls.py                 # Routes dashboard
    ├── admin.py                # Interface admin
    ├── templates/
    │   └── dashboard/
    │       ├── login2.html     # Connexion
    │       ├── register2.html  # Inscription
    │       ├── dashboard_1.html
    │       └── dashboard_2.html
    └── static/
        ├── css/
        ├── js/
        └── plugins/
```

---

## 14. Prochaines Étapes Recommandées

1. **Formulaire d'inscription fonctionnel** : Actuellement, `register2.html` est statique. Créer une vue avec `UserCreationForm`.

2. **Validation des données** : Ajouter des validateurs dans les modèles et formulaires.

3. **Tests unitaires** : Créer des tests pour les modèles et vues.

4. **API REST** : Intégrer Django REST Framework si nécessaire.

5. **Déploiement production** : Configurer Gunicorn, Nginx, et collectstatic.

6. **Sécurité** : 
   - Générer une vraie `SECRET_KEY`
   - Mettre `DEBUG=False` en production
   - Configurer HTTPS

---

## Conclusion

Ce guide couvre l'intégralité du projet depuis l'installation initiale jusqu'à l'état actuel avec le système d'authentification fonctionnel. En suivant ces étapes, n'importe quel développeur peut reproduire exactement le même environnement et comprendre les choix techniques effectués.

**Contact** : Pour toute question, consulter les rapports spécifiques :
- `RAPPORT_TECHNIQUE.md` : Détails techniques configuration
- `RAPPORT_AUTH_FORMS.md` : Système d'authentification
- `RAPPORT_MIGRATION_AUTH_V2.md` : Migration templates
- `DEPLOYMENT.md` / `DEPLOYMENT_MAC.md` : Instructions spécifiques OS
