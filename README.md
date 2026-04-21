# THENELLA Ministries — Site de réservation & Administration

[![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-blue)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Site web professionnel pour THENELLA Ministries, une artiste gospel camerounaise.  
Ce projet permet aux visiteurs de soumettre des demandes de réservation et aux administrateurs de gérer ces demandes via un dashboard sécurisé.

---

## ✨ Fonctionnalités

### Côté public
- 🎨 Site responsive avec design élégant (couleurs brun/doré)
- 🌍 Bilingue français/anglais (sélecteur de langue)
- 📝 Formulaire de réservation avec validation AJAX
- 🖼️ Galerie d'images avec slider automatique
- 🎵 Intégration des albums et singles (liens Apple Music)
- 📱 Menu mobile adapté

### Côté administration
- 🔐 Connexion sécurisée (Flask-Login)
- 📊 Dashboard avec statistiques (total, en attente, confirmées, refusées)
- 📋 Gestion complète des réservations (liste, filtres, mise à jour statut, suppression)
- 📧 Emails automatiques (confirmation client + notification admin)
- 🔌 API REST pour les réservations

### Technique
- 🐍 Flask 3.0 (architecture Blueprint)
- 🗄️ SQLite + SQLAlchemy (ORM)
- 🔄 Flask-Migrate pour les migrations
- 📧 Flask-Mail pour l'envoi d'emails
- 🎨 HTML/CSS/JS natifs (sans framework)

---

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

```bash
# 1. Cloner le projet
cd thenella

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer les variables d'environnement
# Créer un fichier .env à la racine avec :
# FLASK_APP=run.py
# FLASK_ENV=development
# SECRET_KEY=votre_cle_secrete_unique
# DATABASE_URL=sqlite:///thenella.db
# MAIL_USERNAME=votre_email@gmail.com
# MAIL_PASSWORD=votre_mot_de_passe_application
# ADMIN_EMAIL=admin@thenellaministries.com

# 6. Initialiser la base de données
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 7. Créer le compte administrateur
python create_admin.py

# 8. Lancer l'application
python run.py