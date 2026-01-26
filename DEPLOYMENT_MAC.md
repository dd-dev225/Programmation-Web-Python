# 🍎 Guide de Déploiement Complet - macOS

> **Objectif** : Guide pas-à-pas pour configurer et lancer le projet Django sur macOS (Apple Silicon M1/M2/M3 ou Intel).

---

## 📌 Prérequis

### 1. Installer Homebrew (si ce n'est pas déjà fait)
Ouvrez le Terminal et collez cette commande :
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Installer Python et Git
```bash
brew install python git
```

### 3. Installer votre Base de Données
Choisissez **UNE** des deux options :

**Option A : PostgreSQL (Recommandé sur Mac)**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Option B : MySQL**
```bash
brew install mysql
brew services start mysql
```

---

## 🚀 ÉTAPES D'INSTALLATION

### Étape 1 : Cloner le projet

```bash
# Aller dans votre dossier de projets (exemple)
cd ~/Documents

# Cloner le dépôt
git clone https://github.com/dd-dev225/Programmation-Web-Python.git

# Entrer dans le dossier
cd Programmation-Web-Python
```

### Étape 2 : Créer l'environnement virtuel

```bash
python3 -m venv .venv
```

### Étape 3 : Activer l'environnement virtuel

```bash
source .venv/bin/activate
```
_Vous devriez voir `(.venv)` au début de votre ligne de commande._

### Étape 4 : Installer les dépendances

```bash
pip install -r requirements.txt
```
_Si vous avez une erreur avec `psycopg2` sur Mac M1/M2, lancez :_
```bash
pip install psycopg2-binary
```

### Étape 5 : Configurer le fichier .env

1. Copier le fichier d'exemple :
   ```bash
   cp .env.example .env
   ```
2. Ouvrir le fichier `.env` avec TextEdit ou nano :
   ```bash
   open -e .env
   # OU
   nano .env
   ```

3. **Modifier les paramètres** selon votre base de données :

#### Pour PostgreSQL (Port 5432)
```env
SECRET_KEY=votre-cle-secrete-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=postgresql
DB_NAME=db_as
DB_USER=votre_nom_utilisateur_mac  # Souvent votre login système par défaut
DB_PASSWORD=             # Souvent vide en local sur Mac, sinon configurer
DB_HOST=localhost
DB_PORT=5432
```

#### Pour MySQL (Port 3306)
```env
DB_ENGINE=mysql
DB_NAME=db_as
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

### Étape 6 : Créer la base de données

**Pour PostgreSQL :**
```bash
createdb db_as
```

**Pour MySQL :**
```bash
mysql -u root -p -e "CREATE DATABASE db_as CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### Étape 7 : Appliquer les migrations

```bash
python manage.py migrate
```

### Étape 8 : Remplir la base de données (Chargement CSV)

```bash
python manage.py remplirdb
```
_Patientez quelques minutes pendant l'importation (~10 000 lignes)._

### Étape 9 : Créer un compte administrateur

```bash
python manage.py createsuperuser
```

### Étape 10 : Lancer le serveur

```bash
python manage.py runserver
```

Accédez à : [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)

---

## 🔄 WORKFLOW GIT QUOTIDIEN

### Chaque matin (Récupérer le travail des autres)
```bash
# 1. Ouvrir le terminal dans le dossier
cd ~/Documents/Programmation-Web-Python

# 2. Activer l'environnement
source .venv/bin/activate

# 3. Récupérer les changements
git pull origin main
```

### Après avoir codé (Envoyer son travail)
```bash
# 1. Ajouter les fichiers modifiés
git add .

# 2. Enregistrer (Commit)
git commit -m "Description de ce que j'ai fait"

# 3. Envoyer (Push)
git push origin main
```

---

## 🛠 RÉSOLUTION DE PROBLÈMES (Mac)

### 1. "Command not found: python"
Utilisez `python3` au lieu de `python`.

### 2. Erreur d'installation `pg_config` (PostgreSQL)
Si `pip install psycopg2` échoue :
```bash
brew install libpq
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
pip install psycopg2
```

### 3. Port déjà utilisé
Si le port 8000 est pris :
```bash
python manage.py runserver 8080
```
Puis aller sur http://127.0.0.1:8080/dashboard/
