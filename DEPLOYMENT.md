# Guide de Déploiement - Collaboration Multi-BD

Ce projet permet à plusieurs développeurs d'utiliser **MySQL** ou **PostgreSQL** en local.

## Prérequis

- Python 3.10+
- MySQL 8.0+ **OU** PostgreSQL 13+
- Git

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/dd-dev225/Programmation-Web-Python.git
cd Programmation-Web-Python
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer l'environnement

```bash
# Copier le modèle
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Éditer `.env` selon votre base de données :

**Pour MySQL :**
```env
DB_ENGINE=mysql
DB_NAME=data_pwp
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

**Pour PostgreSQL :**
```env
DB_ENGINE=postgresql
DB_NAME=data_pwp
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

### 5. Créer la base de données

**MySQL :**
```sql
CREATE DATABASE data_pwp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**PostgreSQL :**
```sql
CREATE DATABASE data_pwp;
```

### 6. Appliquer les migrations

```bash
python manage.py migrate
```

### 7. Lancer le serveur

```bash
python manage.py runserver
```

Accéder à : http://127.0.0.1:8000/

---

## Workflow Git

```bash
# Avant de travailler
git pull origin main

# Après modifications
git add .
git commit -m "Description des changements"
git push origin main
```

> ⚠️ **Important** : Ne jamais commiter le fichier `.env` ! Il contient vos identifiants locaux.

---

## Résolution de problèmes

### Erreur de connexion BD
- Vérifier que votre serveur de BD tourne
- Vérifier les paramètres dans `.env`
- Vérifier que la base `data_pwp` existe

### Conflit de migrations
```bash
python manage.py migrate --run-syncdb
```
