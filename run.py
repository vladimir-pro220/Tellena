import os
from app import create_app

# Sélection de la configuration selon la variable d'environnement FLASK_ENV
config_name = os.environ.get('FLASK_ENV') or 'default'

# Création de l'application Flask
app = create_app(config_name)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',   # Accessible sur le réseau local
        port=5000,         # Port par défaut Flask
        debug=app.config['DEBUG']
    )