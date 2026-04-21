from datetime import datetime
from app import db


class Booking(db.Model):
    """
    Modèle représentant une demande de réservation/contact
    soumise via le formulaire du site de THENELLA.
    """

    __tablename__ = 'bookings'

    # ----------------------------------------------------------------
    # Colonnes
    # ----------------------------------------------------------------
    id         = db.Column(db.Integer, primary_key=True)

    # Informations du demandeur
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), nullable=False)
    phone      = db.Column(db.String(20),  nullable=True)

    # Informations de l'événement
    event_type = db.Column(db.String(50),  nullable=False)
    message    = db.Column(db.Text,        nullable=False)

    # Statut de la réservation
    # Valeurs possibles : 'pending', 'confirmed', 'rejected'
    status     = db.Column(db.String(20),  nullable=False, default='pending')

    # Langue utilisée lors de la soumission du formulaire (EN ou FR)
    language   = db.Column(db.String(5),   nullable=True,  default='fr')

    # Dates
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # ----------------------------------------------------------------
    # Méthodes utilitaires
    # ----------------------------------------------------------------

    def __repr__(self):
        return f'<Booking {self.id} | {self.name} | {self.event_type} | {self.status}>'

    def to_dict(self):
        """Convertit l'objet en dictionnaire (utile pour l'API REST)."""
        return {
            'id':         self.id,
            'name':       self.name,
            'email':      self.email,
            'phone':      self.phone,
            'event_type': self.event_type,
            'message':    self.message,
            'status':     self.status,
            'language':   self.language,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M'),
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M'),
        }

    @property
    def status_label(self):
        """Retourne le libellé français du statut."""
        labels = {
            'pending':   'En attente',
            'confirmed': 'Confirmée',
            'rejected':  'Refusée',
        }
        return labels.get(self.status, 'Inconnu')

    @property
    def status_color(self):
        """Retourne la couleur Bootstrap associée au statut (pour le dashboard)."""
        colors = {
            'pending':   'warning',
            'confirmed': 'success',
            'rejected':  'danger',
        }
        return colors.get(self.status, 'secondary')

    @property
    def event_type_label(self):
        """Retourne le libellé français du type d'événement."""
        labels = {
            'concert':        'Concert',
            'church-service': 'Culte d\'Église',
            'conference':     'Conférence',
            'wedding':        'Mariage',
            'other':          'Autre',
        }
        return labels.get(self.event_type, self.event_type)