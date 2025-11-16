"""
Script para resetear las contraseñas de todos los usuarios
"""
from app import create_app, db
from app.models.user import Usuario

def resetear_contraseñas():
    """Resetea las contraseñas de todos los usuarios"""
    
    app = create_app()
    
    with app.app_context():
        print("🔐 Reseteando contraseñas...")
        print("-" * 60)
        
        # Resetear admin
        admin = Usuario.query.filter_by(username='admin').first()
        if admin:
            admin.set_password('admin123')
            print("✅ admin -> admin123")
        
        # Resetear veterinarios
        vet1 = Usuario.query.filter_by(username='dra.martinez').first()
        if vet1:
            vet1.set_password('vet123')
            print("✅ dra.martinez -> vet123")
        
        vet2 = Usuario.query.filter_by(username='dr.gonzalez').first()
        if vet2:
            vet2.set_password('vet123')
            print("✅ dr.gonzalez -> vet123")
        
        # Resetear tutores
        tutor1 = Usuario.query.filter_by(username='juan.perez').first()
        if tutor1:
            tutor1.set_password('tutor123')
            print("✅ juan.perez -> tutor123")
        
        tutor2 = Usuario.query.filter_by(username='maria.lopez').first()
        if tutor2:
            tutor2.set_password('tutor123')
            print("✅ maria.lopez -> tutor123")
        
        tutor3 = Usuario.query.filter_by(username='pedro.garcia').first()
        if tutor3:
            tutor3.set_password('tutor123')
            print("✅ pedro.garcia -> tutor123")
        
        # Guardar cambios
        db.session.commit()
        
        print("-" * 60)
        print("✅ ¡Todas las contraseñas reseteadas!")
        print()
        print("🔐 CREDENCIALES:")
        print("   admin / admin123")
        print("   dra.martinez / vet123")
        print("   juan.perez / tutor123")
        print()
        print("🚀 Ahora ejecuta: python run.py")

if __name__ == '__main__':
    resetear_contraseñas()
