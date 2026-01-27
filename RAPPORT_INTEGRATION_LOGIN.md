# 📋 Rapport d'Intégration : Interface de Connexion (`login2.html`)

Ce document détaille les étapes techniques pour intégrer le template HTML fourni (`login2.html`) dans le système d'authentification de Django.

---

## 1. Stratégie d'Intégration

Nous allons utiliser la vue native de Django `LoginView` mais en lui fournissant votre template personnalisé. Cela permet de garder la sécurite de Django tout en ayant votre design.

### Architecture cible
*   **Vue** : `django.contrib.auth.views.LoginView`
*   **Template** : `templates/registration/login.html` (Contenant votre code HTML)
*   **URL** : `http://.../dashboard/login/`

---

## 2. Étapes de Transformation du HTML

Le code HTML brut doit être "Djangoisé" pour fonctionner. Voici les transformations nécessaires :

### A. Gestion des Fichiers Statiques (CSS/JS/Images)
Les chemins relatifs (ex: `../plugins/...`) ne fonctionnent pas dans Django. Il faut utiliser le tag `{% static %}`.

**Avant :**
```html
<link href="css/style.css" rel="stylesheet">
<img src="../plugins/images/admin-logo-dark.png" ... />
```

**Après :**
```html
{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">
<img src="{% static 'plugins/images/admin-logo-dark.png' %}" ... />
```

### B. Configuration du Formulaire
Le formulaire HTML doit envoyer les données à Django via la méthode `POST`.

**1. Balise Form**
*   **Action** : Enlever `action="index.html"`. En laissant vide, le formulaire s'envoie à la même URL (ce que Django attend).
*   **Méthode** : Changer en `method="post"`.
*   **Sécurité** : Ajouter `{% csrf_token %}` juste après l'ouverture du form.

**2. Champs de saisie (Inputs)**
Django attend des noms de champs précis pour l'authentification :
*   Champ utilisateur : doit avoir `name="username"`
*   Champ mot de passe : doit avoir `name="password"`

**Exemple de correction :**
```html
<!-- Avant -->
<input class="form-control" type="text" placeholder="Username">

<!-- Après -->
<input class="form-control" type="text" name="username" placeholder="Username" required>
```

### C. Gestion des Erreurs
Pour afficher les erreurs (ex: "Mot de passe incorrect"), nous ajouterons un bloc conditionnel :
```html
{% if form.errors %}
    <p class="text-danger text-center">Identifiant ou mot de passe incorrect.</p>
{% endif %}
```

---

## 3. Configuration des URLs

Dans `dashboard/urls.py`, nous utiliserons la vue standard en pointant vers votre template.

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... autres urls
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

---

## 4. Redirection après connexion

Dans le fichier `settings.py`, nous devons dire à Django où aller une fois connecté :

```python
LOGIN_REDIRECT_URL = 'dashboard:dashboard_1'
LOGOUT_REDIRECT_URL = 'login'
```

---

## ✅ Résumé du plan d'action
1.  Créer le fichier `templates/registration/login.html` avec votre code HTML transformé.
2.  Mettre à jour `dashboard/urls.py`.
3.  Configurer les redirections dans `settings.py`.
