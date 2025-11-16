"""
Script de diagnóstico para verificar conexión a SQL Server
y credenciales del sistema
"""
from app import create_app, db
from app.models.user import Usuario
from sqlalchemy import text

def diagnostico_completo():
    """Ejecuta diagnóstico completo del sistema"""
    
    print("="*60)
    print("🔍 DIAGNÓSTICO DEL SISTEMA VETERINARIA")
    print("="*60)
    print()
    
    app = create_app()
    
    with app.app_context():
        # 1. VERIFICAR CONEXIÓN A BASE DE DATOS
        print("📌 1. VERIFICANDO CONEXIÓN A SQL SERVER...")
        print("-"*60)
        try:
            # Intentar una consulta simple
            result = db.session.execute(text("SELECT 1"))
            print("✅ Conexión a SQL Server: EXITOSA")
            print(f"   Servidor: {app.config['SQLALCHEMY_DATABASE_URI'][:50]}...")
        except Exception as e:
            print("❌ Error de conexión a SQL Server:")
            print(f"   {str(e)}")
            return False
        
        print()
        
        # 2. VERIFICAR TABLAS
        print("📌 2. VERIFICANDO TABLAS...")
        print("-"*60)
        try:
            inspector = db.inspect(db.engine)
            tablas = inspector.get_table_names()
            print(f"✅ Tablas encontradas: {len(tablas)}")
            for tabla in tablas:
                print(f"   • {tabla}")
        except Exception as e:
            print(f"❌ Error al verificar tablas: {str(e)}")
        
        print()
        
        # 3. VERIFICAR USUARIOS
        print("📌 3. VERIFICANDO USUARIOS EN LA BASE DE DATOS...")
        print("-"*60)
        try:
            total_usuarios = Usuario.query.count()
            print(f"✅ Total de usuarios: {total_usuarios}")
            print()
            
            if total_usuarios == 0:
                print("⚠️  NO HAY USUARIOS EN LA BASE DE DATOS")
                print("   Solución: Ejecuta init_db.py para crear usuarios")
                return False
            
            # Listar todos los usuarios
            usuarios = Usuario.query.all()
            print("👥 USUARIOS REGISTRADOS:")
            print()
            for u in usuarios:
                print(f"   ID: {u.id}")
                print(f"   Usuario: {u.username}")
                print(f"   Email: {u.email}")
                print(f"   Nombre: {u.nombre_completo}")
                print(f"   Rol: {u.rol}")
                print(f"   Activo: {'✅ Sí' if u.activo else '❌ No'}")
                print(f"   Password Hash: {u.password_hash[:50]}...")
                print()
                
        except Exception as e:
            print(f"❌ Error al consultar usuarios: {str(e)}")
            return False
        
        print()
        
        # 4. PROBAR CREDENCIALES DEL ADMIN
        print("📌 4. PROBANDO CREDENCIALES DEL ADMINISTRADOR...")
        print("-"*60)
        try:
            admin = Usuario.query.filter_by(username='admin').first()
            
            if not admin:
                print("❌ Usuario 'admin' NO ENCONTRADO")
                print("   Solución: Ejecuta el script SQL de nuevo")
                return False
            
            print(f"✅ Usuario admin encontrado:")
            print(f"   ID: {admin.id}")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Activo: {admin.activo}")
            print()
            
            # Probar contraseña
            print("🔐 Probando contraseña 'admin123'...")
            if admin.check_password('admin123'):
                print("✅ ¡CONTRASEÑA CORRECTA!")
                print("   El login debería funcionar.")
            else:
                print("❌ CONTRASEÑA INCORRECTA")
                print("   El hash almacenado no coincide con 'admin123'")
                print()
                print("💡 SOLUCIÓN:")
                print("   Ejecuta: python resetear_admin.py")
                
        except Exception as e:
            print(f"❌ Error al verificar admin: {str(e)}")
            return False
        
        print()
        
        # 5. VERIFICAR OTROS USUARIOS
        print("📌 5. PROBANDO CREDENCIALES DE OTROS USUARIOS...")
        print("-"*60)
        
        credenciales_prueba = [
            ('admin', 'admin123'),
            ('dra.martinez', 'vet123'),
            ('juan.perez', 'tutor123')
        ]
        
        for username, password in credenciales_prueba:
            user = Usuario.query.filter_by(username=username).first()
            if user:
                resultado = "✅" if user.check_password(password) else "❌"
                print(f"{resultado} {username} / {password}")
            else:
                print(f"⚠️  {username} no encontrado")
        
        print()
        print("="*60)
        print("✅ DIAGNÓSTICO COMPLETADO")
        print("="*60)
        
        return True

if __name__ == '__main__':
    diagnostico_completo()
