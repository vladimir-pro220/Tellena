# Ce fichier couvre :

# GET /api/bookings → liste paginée avec filtre optionnel par statut
# GET /api/bookings/<id> → détail d'une réservation
# PATCH /api/bookings/<id>/status → mise à jour du statut
# DELETE /api/bookings/<id> → suppression
# GET /api/stats → statistiques générales


from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.models.booking import Booking

# Création du Blueprint API
api = Blueprint('api', __name__)


# ----------------------------------------------------------------
# Réservations
# ----------------------------------------------------------------

@api.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    """Retourne la liste de toutes les réservations."""

    status_filter = request.args.get('status')
    page          = request.args.get('page', 1, type=int)
    per_page      = request.args.get('per_page', 10, type=int)

    query = Booking.query.order_by(Booking.created_at.desc())

    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'success'  : True,
        'bookings' : [b.to_dict() for b in pagination.items],
        'total'    : pagination.total,
        'pages'    : pagination.pages,
        'page'     : pagination.page,
        'per_page' : per_page,
    }), 200


@api.route('/bookings/<int:booking_id>', methods=['GET'])
@login_required
def get_booking(booking_id):
    """Retourne les détails d'une réservation."""

    booking = Booking.query.get_or_404(booking_id)
    return jsonify({
        'success': True,
        'booking': booking.to_dict()
    }), 200


@api.route('/bookings/<int:booking_id>/status', methods=['PATCH'])
@login_required
def update_booking_status(booking_id):
    """Met à jour le statut d'une réservation via l'API."""

    booking    = Booking.query.get_or_404(booking_id)
    data       = request.get_json()
    new_status = data.get('status')

    allowed_statuses = ['pending', 'confirmed', 'rejected']
    if new_status not in allowed_statuses:
        return jsonify({
            'success': False,
            'message': f'Statut invalide. Valeurs acceptées : {allowed_statuses}'
        }), 400

    booking.status = new_status
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Statut mis à jour : {booking.status_label}',
        'booking': booking.to_dict()
    }), 200


@api.route('/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    """Supprime une réservation via l'API."""

    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Réservation #{booking_id} supprimée.'
    }), 200


# ----------------------------------------------------------------
# Statistiques
# ----------------------------------------------------------------

@api.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Retourne les statistiques générales des réservations."""

    return jsonify({
        'success': True,
        'stats': {
            'total'    : Booking.query.count(),
            'pending'  : Booking.query.filter_by(status='pending').count(),
            'confirmed': Booking.query.filter_by(status='confirmed').count(),
            'rejected' : Booking.query.filter_by(status='rejected').count(),
        }
    }), 200