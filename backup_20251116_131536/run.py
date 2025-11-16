"""
Punto de entrada principal de la aplicación
"""
from app import create_app

# Crear la aplicación usando la configuración por defecto
app = create_app()

if __name__ == '__main__':
    # Ejecutar la aplicación en modo desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
