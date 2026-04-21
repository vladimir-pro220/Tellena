# ce fichier sert uniquement à exposer les modèles pour 
# qu'ils soient importables facilement depuis n'importe où 
# dans l'app, et surtout pour que 
# Flask-Migrate les détecte lors des migrations.


from app.models.booking import Booking
from app.models.user import User