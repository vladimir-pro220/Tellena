import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

class Config:
    """Configuration de base commune à tous les environnements."""

    # Clé secrète pour la sécurité des sessions et des formulaires
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'changez-cette-cle-en-production'

    # Base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///thenella.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration Email (Flask-Mail)
    MAIL_SERVER   = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT     = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS  = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or \
        'contact@thenellaministries.com'

    # Email de l'administrateur (reçoit les notifications de réservation)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@thenellaministries.com'

    # Nom du site
    SITE_NAME = 'THENELLA Ministries'


class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///thenella_dev.db'


class ProductionConfig(Config):
    """Configuration pour l'environnement de production."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///thenella.db'


class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///thenella_test.db'
    WTF_CSRF_ENABLED = False


# Dictionnaire pour sélectionner la config selon l'environnement
config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     DevelopmentConfig
}