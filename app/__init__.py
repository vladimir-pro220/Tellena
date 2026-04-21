from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from config import config

# Initialisation des extensions (sans app pour l'instant)
db       = SQLAlchemy()
migrate  = Migrate()
login    = LoginManager()
mail     = Mail()

# Configuration de Flask-Login
login.login_view     = 'admin.login'        # Route de connexion admin
login.login_message  = 'Veuillez vous connecter pour accéder à cette page.'
login.login_message_category = 'warning'


def create_app(config_name='default'):
    """
    Factory function — crée et configure l'application Flask.
    Permet de créer plusieurs instances de l'app (dev, test, prod).
    """

    app = Flask(__name__)

    # Chargement de la configuration selon l'environnement
    app.config.from_object(config[config_name])

    # Initialisation des extensions avec l'app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # ----------------------------------------------------------------
    # Enregistrement des Blueprints (routes)
    # ----------------------------------------------------------------

    # Routes principales (page d'accueil, etc.)
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Routes du formulaire de contact/réservation
    from app.routes.contact import contact as contact_blueprint
    app.register_blueprint(contact_blueprint)

    # Routes du dashboard administrateur
    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Routes de l'API REST
    from app.routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app