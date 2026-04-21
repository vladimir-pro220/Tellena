# Simple et propre — ce Blueprint gère uniquement la page d'accueil. 
# Le formulaire de réservation sera géré séparément 
# dans contact.py (Étape 10).


from flask import Blueprint, render_template

# Création du Blueprint principal
main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Page d'accueil du site THENELLA."""
    return render_template('index.html')