# Ce fichier couvre :

# Connexion / déconnexion → utilise check_password() et update_last_login() de user.py
# Dashboard → statistiques + 5 dernières réservations
# Liste des réservations → avec filtre par statut
# Mise à jour du statut → pending / confirmed / rejected
# Suppression d'une réservation


from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.models.booking import Booking

# Création du Blueprint admin
admin = Blueprint('admin', __name__)


# ----------------------------------------------------------------
# Authentification
# ----------------------------------------------------------------

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion administrateur."""

    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'danger')
            return redirect(url_for('admin.login'))

        if not user.is_active:
            flash('Ce compte est désactivé.', 'warning')
            return redirect(url_for('admin.login'))

        # Connexion réussie
        login_user(user)
        user.update_last_login()
        db.session.commit()

        # Redirection vers la page demandée ou le dashboard
        next_page = request.args.get('next')
        return redirect(next_page or url_for('admin.dashboard'))

    return render_template('admin/login.html')


@admin.route('/logout')
@login_required
def logout():
    """Déconnexion de l'administrateur."""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('admin.login'))


# ----------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------

@admin.route('/dashboard')
@login_required
def dashboard():
    """Tableau de bord principal."""

    # Statistiques générales
    total     = Booking.query.count()
    pending   = Booking.query.filter_by(status='pending').count()
    confirmed = Booking.query.filter_by(status='confirmed').count()
    rejected  = Booking.query.filter_by(status='rejected').count()

    # 5 dernières réservations
    recent_bookings = Booking.query.order_by(
        Booking.created_at.desc()
    ).limit(5).all()

    stats = {
        'total':     total,
        'pending':   pending,
        'confirmed': confirmed,
        'rejected':  rejected,
    }

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_bookings=recent_bookings
    )


# ----------------------------------------------------------------
# Gestion des réservations
# ----------------------------------------------------------------

@admin.route('/bookings')
@login_required
def bookings():
    """Liste complète des réservations avec filtrage par statut."""

    status_filter = request.args.get('status', 'all')

    if status_filter == 'all':
        bookings_list = Booking.query.order_by(Booking.created_at.desc()).all()
    else:
        bookings_list = Booking.query.filter_by(status=status_filter)\
                                     .order_by(Booking.created_at.desc()).all()

    return render_template(
        'admin/bookings.html',
        bookings=bookings_list,
        current_filter=status_filter
    )


@admin.route('/bookings/<int:booking_id>/update', methods=['POST'])
@login_required
def update_booking(booking_id):
    """Met à jour le statut d'une réservation."""

    booking = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')

    allowed_statuses = ['pending', 'confirmed', 'rejected']
    if new_status not in allowed_statuses:
        flash('Statut invalide.', 'danger')
        return redirect(url_for('admin.bookings'))

    booking.status = new_status
    booking.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f'Réservation #{booking.id} mise à jour : {booking.status_label}.', 'success')
    return redirect(url_for('admin.bookings'))


@admin.route('/bookings/<int:booking_id>/delete', methods=['POST'])
@login_required
def delete_booking(booking_id):
    """Supprime une réservation."""

    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()

    flash(f'Réservation #{booking_id} supprimée.', 'success')
    return redirect(url_for('admin.bookings'))