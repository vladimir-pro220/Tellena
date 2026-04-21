# Ce fichier est cohérent avec :

# Flask-Login → UserMixin + get_id()
# Werkzeug → hachage sécurisé du mot de passe
# __init__.py → login.login_view = 'admin.login'
# booking.py → même style de code


from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """
    Modèle représentant un administrateur du site THENELLA.
    Utilisé pour la connexion au dashboard d'administration.
    """

    __tablename__ = 'users'

    # ----------------------------------------------------------------
    # Colonnes
    # ----------------------------------------------------------------
    id         = db.Column(db.Integer, primary_key=True)

    # Informations de connexion
    username   = db.Column(db.String(64),  nullable=False, unique=True, index=True)
    email      = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # Informations du profil
    full_name  = db.Column(db.String(100), nullable=True)

    # Statut du compte
    is_active  = db.Column(db.Boolean, nullable=False, default=True)
    is_superadmin = db.Column(db.Boolean, nullable=False, default=False)

    # Dates
    created_at    = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)

    # ----------------------------------------------------------------
    # Gestion du mot de passe
    # ----------------------------------------------------------------

    def set_password(self, password):
        """Hache et enregistre le mot de passe."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe en clair contre le hash stocké."""
        return check_password_hash(self.password_hash, password)

    # ----------------------------------------------------------------
    # Flask-Login : méthode requise
    # ----------------------------------------------------------------

    def get_id(self):
        """Retourne l'identifiant unique de l'utilisateur (requis par Flask-Login)."""
        return str(self.id)

    # ----------------------------------------------------------------
    # Méthodes utilitaires
    # ----------------------------------------------------------------

    def __repr__(self):
        return f'<User {self.id} | {self.username} | superadmin={self.is_superadmin}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire (utile pour l'API REST)."""
        return {
            'id':            self.id,
            'username':      self.username,
            'email':         self.email,
            'full_name':     self.full_name,
            'is_active':     self.is_active,
            'is_superadmin': self.is_superadmin,
            'created_at':    self.created_at.strftime('%d/%m/%Y %H:%M'),
            'last_login_at': self.last_login_at.strftime('%d/%m/%Y %H:%M')
                             if self.last_login_at else None,
        }

    def update_last_login(self):
        """Met à jour la date de dernière connexion."""
        self.last_login_at = datetime.utcnow()