# Simple et cohérent avec app/models/__init__.py — 
#ce fichier expose tous les Blueprints pour qu'ils soient facilement importables.



from app.routes.main import main
from app.routes.contact import contact
from app.routes.admin import admin
from app.routes.api import api