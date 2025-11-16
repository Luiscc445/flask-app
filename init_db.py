"""
Script para inicializar la base de datos
Crea todas las tablas y datos iniciales
"""
from app import create_app, db
from app.models.user import Usuario
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.medicamento import Medicamento, Receta
from datetime import datetime, timedelta

def init_database():
    """
    Inicializa la base de datos con datos de ejemplo
    """
    app = create_app()
    
    with app.app_context():
        print("🔄 Eliminando tablas existentes...")
        db.drop_all()
        
        print("🔄 Creando tablas...")
        db.create_all()
        
        print("👤 Creando usuario administrador...")
        admin = Usuario(
            username='admin',
            email='admin@veterinaria.com',
            password='admin123',
            nombre='Administrador',
            apellido='Sistema',
            rol='admin'
        )
        db.session.add(admin)
        
        print("👨‍⚕️ Creando veterinarios de ejemplo...")
        vet1 = Usuario(
            username='dra.martinez',
            email='martinez@veterinaria.com',
            password='vet123',
            nombre='María',
            apellido='Martínez',
            telefono='71234567',
            rol='veterinario',
            especialidad='Medicina General',
            licencia_profesional='MV-12345'
        )
        
        vet2 = Usuario(
            username='dr.gonzalez',
            email='gonzalez@veterinaria.com',
            password='vet123',
            nombre='Carlos',
            apellido='González',
            telefono='72345678',
            rol='veterinario',
            especialidad='Cirugía',
            licencia_profesional='MV-67890'
        )
        
        db.session.add(vet1)
        db.session.add(vet2)
        
        print("👥 Creando tutores de ejemplo...")
        tutor1 = Usuario(
            username='juan.perez',
            email='juan@email.com',
            password='tutor123',
            nombre='Juan',
            apellido='Pérez',
            telefono='73456789',
            direccion='Calle Principal #123, La Paz',
            rol='tutor'
        )
        
        tutor2 = Usuario(
            username='maria.lopez',
            email='maria@email.com',
            password='tutor123',
            nombre='María',
            apellido='López',
            telefono='74567890',
            direccion='Av. Arce #456, La Paz',
            rol='tutor'
        )
        
        tutor3 = Usuario(
            username='pedro.garcia',
            email='pedro@email.com',
            password='tutor123',
            nombre='Pedro',
            apellido='García',
            telefono='75678901',
            direccion='Zona Sur #789, La Paz',
            rol='tutor'
        )
        
        db.session.add(tutor1)
        db.session.add(tutor2)
        db.session.add(tutor3)
        
        # Commit para obtener IDs
        db.session.commit()
        
        print("🐕 Creando mascotas de ejemplo...")
        mascota1 = Mascota(
            nombre='Max',
            especie='Perro',
            raza='Labrador',
            tutor_id=tutor1.id,
            fecha_nacimiento=datetime(2020, 3, 15).date(),
            sexo='Macho',
            color='Dorado',
            peso=30.5,
            esterilizado=True
        )
        
        mascota2 = Mascota(
            nombre='Luna',
            especie='Gato',
            raza='Siamés',
            tutor_id=tutor1.id,
            fecha_nacimiento=datetime(2021, 7, 20).date(),
            sexo='Hembra',
            color='Blanco con puntos oscuros',
            peso=4.2,
            esterilizado=True
        )
        
        mascota3 = Mascota(
            nombre='Rocky',
            especie='Perro',
            raza='Pastor Alemán',
            tutor_id=tutor2.id,
            fecha_nacimiento=datetime(2019, 11, 5).date(),
            sexo='Macho',
            color='Negro y café',
            peso=35.0,
            esterilizado=False
        )
        
        mascota4 = Mascota(
            nombre='Michi',
            especie='Gato',
            raza='Mestizo',
            tutor_id=tutor2.id,
            fecha_nacimiento=datetime(2022, 2, 14).date(),
            sexo='Hembra',
            color='Naranja',
            peso=3.8
        )
        
        mascota5 = Mascota(
            nombre='Toby',
            especie='Perro',
            raza='Beagle',
            tutor_id=tutor3.id,
            fecha_nacimiento=datetime(2021, 5, 10).date(),
            sexo='Macho',
            color='Tricolor',
            peso=12.5
        )
        
        db.session.add_all([mascota1, mascota2, mascota3, mascota4, mascota5])
        db.session.commit()
        
        print("💊 Creando medicamentos de ejemplo...")
        medicamentos_data = [
            {
                'nombre': 'Amoxicilina 500mg',
                'principio_activo': 'Amoxicilina',
                'presentacion': 'Tabletas',
                'concentracion': '500mg',
                'stock': 100,
                'stock_minimo': 20,
                'precio_unitario': 2.5
            },
            {
                'nombre': 'Ibuprofeno Veterinario',
                'principio_activo': 'Ibuprofeno',
                'presentacion': 'Tabletas',
                'concentracion': '200mg',
                'stock': 80,
                'stock_minimo': 15,
                'precio_unitario': 1.8
            },
            {
                'nombre': 'Antiparasitario Interno',
                'principio_activo': 'Fenbendazol',
                'presentacion': 'Suspensión',
                'concentracion': '10%',
                'stock': 50,
                'stock_minimo': 10,
                'precio_unitario': 15.0
            },
            {
                'nombre': 'Vacuna Triple Felina',
                'principio_activo': 'Virus inactivados',
                'presentacion': 'Inyectable',
                'concentracion': '1ml',
                'stock': 30,
                'stock_minimo': 5,
                'precio_unitario': 45.0
            },
            {
                'nombre': 'Vacuna Antirrábica',
                'principio_activo': 'Virus inactivado',
                'presentacion': 'Inyectable',
                'concentracion': '1ml',
                'stock': 40,
                'stock_minimo': 10,
                'precio_unitario': 35.0
            },
            {
                'nombre': 'Gotas Oftálmicas',
                'principio_activo': 'Tobramicina',
                'presentacion': 'Solución',
                'concentracion': '0.3%',
                'stock': 25,
                'stock_minimo': 8,
                'precio_unitario': 12.0
            },
            {
                'nombre': 'Antiinflamatorio Injectable',
                'principio_activo': 'Meloxicam',
                'presentacion': 'Inyectable',
                'concentracion': '5mg/ml',
                'stock': 8,  # Stock bajo para demostrar alerta
                'stock_minimo': 10,
                'precio_unitario': 25.0
            },
            {
                'nombre': 'Suplemento Vitamínico',
                'principio_activo': 'Complejo B',
                'presentacion': 'Jarabe',
                'concentracion': '100ml',
                'stock': 60,
                'stock_minimo': 12,
                'precio_unitario': 18.0
            }
        ]
        
        for med_data in medicamentos_data:
            medicamento = Medicamento(**med_data)
            db.session.add(medicamento)
        
        db.session.commit()
        
        print("📅 Creando citas de ejemplo...")
        # Cita pendiente
        cita1 = Cita(
            mascota_id=mascota1.id,
            tutor_id=tutor1.id,
            fecha_hora=datetime.now() + timedelta(days=2, hours=10),
            motivo='Revisión general y vacunación',
            estado='pendiente'
        )
        
        # Cita aceptada
        cita2 = Cita(
            mascota_id=mascota3.id,
            tutor_id=tutor2.id,
            fecha_hora=datetime.now() + timedelta(days=1, hours=15),
            motivo='Control post-operatorio',
            estado='aceptada',
            veterinario_id=vet2.id
        )
        
        # Cita atendida
        cita3 = Cita(
            mascota_id=mascota2.id,
            tutor_id=tutor1.id,
            fecha_hora=datetime.now() - timedelta(days=5),
            motivo='Vacunación antirrábica',
            estado='atendida',
            veterinario_id=vet1.id,
            diagnostico='Mascota en buen estado de salud',
            tratamiento='Vacunación antirrábica administrada',
            observaciones='Próxima vacunación en 1 año',
            fecha_atencion=datetime.now() - timedelta(days=5)
        )
        
        # Cita pospuesta
        cita4 = Cita(
            mascota_id=mascota4.id,
            tutor_id=tutor2.id,
            fecha_hora=datetime.now() + timedelta(days=3),
            motivo='Esterilización',
            estado='pospuesta',
            motivo_posposicion='Cirugías reprogramadas por mantenimiento de sala',
            nueva_fecha_sugerida=datetime.now() + timedelta(days=10)
        )
        
        db.session.add_all([cita1, cita2, cita3, cita4])
        db.session.commit()
        
        print("✅ ¡Base de datos inicializada exitosamente!")
        print("\n📊 Resumen:")
        print(f"  • Administradores: 1")
        print(f"  • Veterinarios: 2")
        print(f"  • Tutores: 3")
        print(f"  • Mascotas: 5")
        print(f"  • Medicamentos: {len(medicamentos_data)}")
        print(f"  • Citas: 4")
        print("\n🔐 Credenciales de acceso:")
        print("\n  ADMINISTRADOR:")
        print("    Usuario: admin")
        print("    Contraseña: admin123")
        print("\n  VETERINARIO:")
        print("    Usuario: dra.martinez")
        print("    Contraseña: vet123")
        print("\n  TUTOR:")
        print("    Usuario: juan.perez")
        print("    Contraseña: tutor123")
        print("\n🚀 Ejecuta 'python run.py' para iniciar la aplicación\n")

if __name__ == '__main__':
    init_database()
