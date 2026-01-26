# 📋 Guide de Déploiement Complet - Projet Django Multi-BD

> **Objectif** : Permettre à 3 développeurs (2 MySQL + 1 PostgreSQL) de collaborer sur le même projet via GitHub.

---

## 📌 Prérequis

### Logiciels requis

| Logiciel | Version minimale | Téléchargement |
|----------|------------------|----------------|
| Python | 3.10+ | https://www.python.org/downloads/ |
| Git | 2.30+ | https://git-scm.com/downloads |
| MySQL **OU** PostgreSQL | MySQL 8.0+ / PostgreSQL 13+ | Selon votre choix |

### Vérification des installations

```powershell
# Vérifier Python
python --version

# Vérifier Git
git --version

# Vérifier pip
pip --version
```

---

## 🚀 ÉTAPES D'INSTALLATION

### Étape 1 : Cloner le projet

```powershell
# Se placer dans le dossier où vous voulez le projet
cd C:\Users\VotreNom\Downloads

# Cloner depuis GitHub
git clone https://github.com/dd-dev225/Programmation-Web-Python.git

# Entrer dans le dossier
cd Programmation-Web-Python
```

---

### Étape 2 : Autoriser l'exécution des scripts PowerShell

> ⚠️ **Important** : Cette étape est obligatoire sur Windows pour activer l'environnement virtuel.

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Répondre **O** (Oui) si demandé.

---

### Étape 3 : Créer l'environnement virtuel

```powershell
python -m venv .venv
```

---

### Étape 4 : Activer l'environnement virtuel

```powershell
.venv\Scripts\activate
```

Vous devriez voir `(.venv)` apparaître au début de votre ligne de commande.

---

### Étape 5 : Installer les dépendances

```powershell
pip install -r requirements.txt
```

---

### Étape 6 : Configurer votre fichier .env

```powershell
# Copier le modèle
copy .env.example .env
```

Ouvrir le fichier `.env` et modifier selon votre base de données :

#### Configuration MySQL (pour 2 membres)

```env
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=mysql
DB_NAME=db_as
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

#### Configuration PostgreSQL (pour 1 membre)

```env
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=postgresql
DB_NAME=db_as
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

---

### Étape 7 : Créer la base de données

#### Pour MySQL (via phpMyAdmin ou MySQL Workbench)

```sql
CREATE DATABASE db_as CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Ou via la ligne de commande MySQL :
```powershell
mysql -u root -p -e "CREATE DATABASE db_as CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

#### Pour PostgreSQL (via pgAdmin ou psql)

```sql
CREATE DATABASE db_as;
```

---

### Étape 8 : Appliquer les migrations

```powershell
python manage.py migrate
```

Résultat attendu :
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, dashboard, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

---

### Étape 9 : Remplir la base de données

```powershell
python manage.py remplirdb
```

> ⏱️ Cette commande prend **5-10 minutes** car elle importe ~10 000 lignes.

Résultat attendu :
```
Bonjour ! Début de l'enregistrement des lignes de commande...
9994 lignes lues dans le CSV.
Partie 1 : création des entités uniques
...
Résultat final :
   - Lignes créées : 9994
   - Erreurs rencontrées : 0
Base de données remplie avec succès !
```

---

### Étape 10 : Créer un compte administrateur

```powershell
python manage.py createsuperuser
```

Suivre les instructions :
- Username : `admin`
- Email : `admin@example.com`
- Password : `admin123` (ou autre)

---

### Étape 11 : Lancer le serveur

```powershell
python manage.py runserver
```

Résultat attendu :
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 PAGES DISPONIBLES

| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/dashboard/ | Dashboard principal avec graphiques |
| http://127.0.0.1:8000/dashboard/dashbord_2 | Dashboard secondaire |
| http://127.0.0.1:8000/admin/ | Interface d'administration Django |

---

## 🔄 WORKFLOW GIT QUOTIDIEN

### Avant de commencer à travailler

```powershell
# Activer l'environnement
.venv\Scripts\activate

# Récupérer les dernières modifications
git pull origin main
```

### Après avoir fait des modifications

```powershell
git add .
git commit -m "Description de vos changements"
git push origin main
```

---

## ⚠️ RÉSOLUTION DE PROBLÈMES

### Erreur : "Script cannot be loaded because running scripts is disabled"

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erreur : "Unknown database 'db_as'"

La base de données n'existe pas. Créez-la :
- MySQL : `CREATE DATABASE db_as CHARACTER SET utf8mb4;`
- PostgreSQL : `CREATE DATABASE db_as;`

### Erreur : "ModuleNotFoundError: No module named 'xxx'"

```powershell
pip install -r requirements.txt
```

### Erreur : "Access denied for user 'root'"

Vérifiez le mot de passe dans votre fichier `.env` :
```env
DB_PASSWORD=votre_vrai_mot_de_passe
```

### Le serveur ne démarre pas

Vérifiez que :
1. L'environnement virtuel est activé (vous voyez `(.venv)`)
2. Le serveur MySQL/PostgreSQL tourne
3. La base de données existe

---

## 📁 STRUCTURE DU PROJET

```
Programmation-Web-Python/
├── .env                  # 🔒 Config locale (NE PAS COMMITER)
├── .env.example          # Modèle de configuration
├── .gitignore            # Fichiers ignorés par Git
├── .venv/                # Environnement virtuel (local)
├── requirements.txt      # Dépendances Python
├── manage.py             # Script Django principal
├── DEPLOYMENT.md         # Ce guide
├── DjangoProject/        # Configuration Django
│   ├── settings.py       # Paramètres (lit .env)
│   ├── urls.py           # Routes principales
│   └── data/             # Fichiers CSV de données
└── dashboard/            # Application principale
    ├── views.py          # Logique des pages
    ├── models.py         # Modèles de données
    ├── urls.py           # Routes du dashboard
    └── templates/        # Fichiers HTML
```

---

## 👥 RÔLE DE CHAQUE FICHIER

| Fichier | Rôle | Partagé sur Git ? |
|---------|------|-------------------|
| `.env` | Vos identifiants locaux | ❌ Non |
| `.env.example` | Modèle pour créer .env | ✅ Oui |
| `.venv/` | Packages Python | ❌ Non |
| `requirements.txt` | Liste des packages | ✅ Oui |
| Code source | Le projet | ✅ Oui |

---

## ✅ CHECKLIST RAPIDE

- [ ] Python 3.10+ installé
- [ ] Git installé
- [ ] MySQL ou PostgreSQL installé et démarré
- [ ] Projet cloné depuis GitHub
- [ ] ExecutionPolicy configurée
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` configuré
- [ ] Base de données `db_as` créée
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Données importées (`python manage.py remplirdb`)
- [ ] Compte admin créé (`python manage.py createsuperuser`)
- [ ] Serveur lancé (`python manage.py runserver`)
- [ ] Dashboard accessible sur http://127.0.0.1:8000/dashboard/
