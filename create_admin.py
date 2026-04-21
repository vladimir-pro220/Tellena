#!/usr/bin/env python
"""Script pour créer le premier administrateur de THENELLA Ministries."""

from app import create_app, db
from app.models.user import User

app = create_app('development')

with app.app_context():
    # Vérifier si un admin existe déjà
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        print("⚠️ Un compte administrateur existe déjà !")
        print(f"   Nom d'utilisateur : {admin.username}")
        print(f"   Email : {admin.email}")
    else:
        # Création du compte admin
        admin = User(
            username='admin',
            email='admin@thenellaministries.com',
            full_name='Administrateur THENELLA',
            is_superadmin=True,
            is_active=True
        )
        # Mot de passe temporaire (à changer après première connexion)
        admin.set_password('Thenella2025!')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Compte administrateur créé avec succès !")
        print("   ┌─────────────────────────────────────────┐")
        print("   │  Identifiant : admin                    │")
        print("   │  Mot de passe : Thenella2025!           │")
        print("   └─────────────────────────────────────────┘")
        print("\n⚠️ Pense à changer ce mot de passe après ta première connexion !")