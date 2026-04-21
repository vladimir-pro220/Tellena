# Ce fichier est cohérent avec :

# Booking → utilise tous les champs définis dans booking.py
# Flask-Mail → utilise ADMIN_EMAIL défini dans config.py
# Templates emails → prépare déjà les appels vers confirmation.html et notification.html (Étapes 18 & 19)


from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from app import db, mail
from app.models.booking import Booking

# Création du Blueprint contact
contact = Blueprint('contact', __name__)


@contact.route('/contact', methods=['POST'])
def submit():
    """
    Reçoit les données du formulaire de réservation,
    les enregistre en base et envoie les emails de confirmation.
    """

    data = request.get_json()

    # ----------------------------------------------------------------
    # Validation des champs obligatoires
    # ----------------------------------------------------------------
    required_fields = ['name', 'email', 'event_type', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'Le champ "{field}" est obligatoire.'
            }), 400

    # ----------------------------------------------------------------
    # Création et enregistrement de la réservation
    # ----------------------------------------------------------------
    booking = Booking(
        name       = data.get('name'),
        email      = data.get('email'),
        phone      = data.get('phone'),
        event_type = data.get('event_type'),
        message    = data.get('message'),
        language   = data.get('language', 'fr'),
        status     = 'pending'
    )

    db.session.add(booking)
    db.session.commit()

    # ----------------------------------------------------------------
    # Envoi des emails
    # ----------------------------------------------------------------
    try:
        _send_confirmation_email(booking)
        _send_notification_email(booking)
    except Exception as e:
        current_app.logger.error(f'Erreur envoi email : {e}')
        # On ne bloque pas la réservation si l'email échoue

    return jsonify({
        'success': True,
        'message': 'Votre demande a bien été enregistrée. Nous vous contacterons bientôt.',
        'booking_id': booking.id
    }), 201


# ----------------------------------------------------------------
# Fonctions utilitaires (emails)
# ----------------------------------------------------------------

def _send_confirmation_email(booking):
    """Envoie un email de confirmation au client."""
    msg = Message(
        subject = 'Confirmation de votre demande — THENELLA Ministries',
        recipients = [booking.email],
        html = _render_confirmation(booking)
    )
    mail.send(msg)


def _send_notification_email(booking):
    """Envoie une notification à l'administrateur."""
    admin_email = current_app.config['ADMIN_EMAIL']
    msg = Message(
        subject = f'Nouvelle réservation #{booking.id} — {booking.event_type_label}',
        recipients = [admin_email],
        html = _render_notification(booking)
    )
    mail.send(msg)


def _render_confirmation(booking):
    """Génère le contenu HTML de l'email de confirmation client."""
    from flask import render_template
    return render_template('emails/confirmation.html', booking=booking)


def _render_notification(booking):
    """Génère le contenu HTML de l'email de notification admin."""
    from flask import render_template
    return render_template('emails/notification.html', booking=booking)