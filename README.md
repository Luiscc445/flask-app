# Sistema de Gestión Veterinaria - Flask MVC

## 🏥 Descripción
Sistema web completo para gestión de clínica veterinaria con arquitectura MVC usando Flask y PostgreSQL.

## 👥 Roles del Sistema

### 1. **Tutor** (Usuario Cliente)
- Registro automático en el sistema
- Login con usuario y contraseña
- Reservar citas médicas para sus mascotas
- Ver historial de citas
- Gestionar sus mascotas

### 2. **Veterinario** (Médico)
- Login con credenciales asignadas por admin
- Ver solicitudes de citas pendientes
- Aceptar o posponer citas
- Atender mascotas
- Recetar medicamentos (reduce stock automáticamente)
- Ver historial de atenciones

### 3. **Administrador**
- Login con credenciales de admin
- Gestión completa de tutores (CRUD)
- Gestión completa de veterinarios (CRUD)
- Crear usuarios y contraseñas para veterinarios
- Gestión de inventario de medicamentos (CRUD)
- Ver todos los tutores registrados automáticamente
- Editar información de tutores si es necesario

## 🚀 Características
- ✅ Arquitectura MVC bien definida
- ✅ Autenticación y autorización por roles
- ✅ Diseño responsive y moderno
- ✅ Control de inventario automático
- ✅ Sistema de citas médicas
- ✅ Dashboard para cada rol
- ✅ CRUD completo para administrador
- ✅ Validaciones de formularios
- ✅ Mensajes flash para feedback

## 📋 Requisitos Previos
- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar o descomprimir el proyecto
```bash
cd veterinaria_flask
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos PostgreSQL

#### Opción A: Desde psql
```sql
-- Conectarse a PostgreSQL
psql -U postgres

-- Crear base de datos
CREATE DATABASE veterinaria_db;

-- Crear usuario (opcional)
CREATE USER vet_admin WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE veterinaria_db TO vet_admin;
```

#### Opción B: Desde pgAdmin
1. Abrir pgAdmin
2. Crear nueva base de datos: `veterinaria_db`
3. Configurar las credenciales en `config.py`

### 5. Configurar variables de entorno
Editar el archivo `config.py` con tus credenciales de PostgreSQL:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://usuario:password@localhost/veterinaria_db'
```

### 6. Inicializar la base de datos
```bash
python init_db.py
```

Esto creará:
- Todas las tablas necesarias
- Usuario administrador por defecto:
  - **Usuario:** admin
  - **Contraseña:** admin123
- Datos de ejemplo (opcional)

### 7. Ejecutar la aplicación
```bash
python run.py
```

La aplicación estará disponible en: `http://localhost:5000`

## 🔐 Credenciales por Defecto

### Administrador
- **Usuario:** admin
- **Contraseña:** admin123

### Tutor de Ejemplo
- **Usuario:** juan.perez
- **Contraseña:** tutor123

### Veterinario de Ejemplo
- **Usuario:** dra.martinez
- **Contraseña:** vet123

## 📁 Estructura del Proyecto
```
veterinaria_flask/
├── app/
│   ├── __init__.py
│   ├── models/              # Modelos (Model)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── mascota.py
│   │   ├── cita.py
│   │   └── medicamento.py
│   ├── controllers/         # Controladores (Controller)
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── admin_controller.py
│   │   ├── tutor_controller.py
│   │   └── veterinario_controller.py
│   ├── templates/           # Vistas HTML (View)
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── tutor/
│   │   └── veterinario/
│   └── static/              # CSS, JS, imágenes
│       ├── css/
│       └── js/
├── config.py                # Configuración
├── init_db.py              # Inicializador de BD
├── run.py                  # Punto de entrada
└── requirements.txt        # Dependencias
```

## 🎯 Uso del Sistema

### Como Tutor
1. Registrarse en la página principal
2. Iniciar sesión
3. Registrar mascotas
4. Solicitar citas médicas
5. Ver historial

### Como Veterinario
1. Iniciar sesión con credenciales asignadas
2. Ver citas pendientes
3. Aceptar o posponer citas
4. Atender mascotas
5. Recetar medicamentos

### Como Administrador
1. Iniciar sesión
2. Gestionar veterinarios (crear, editar, eliminar)
3. Gestionar tutores (ver, editar, eliminar)
4. Gestionar inventario de medicamentos
5. Ver reportes del sistema

## 🛠️ Tecnologías Utilizadas
- **Backend:** Flask 3.0
- **Base de Datos:** PostgreSQL
- **ORM:** SQLAlchemy
- **Autenticación:** Flask-Login
- **Formularios:** Flask-WTF
- **Frontend:** HTML5, CSS3, JavaScript
- **Diseño:** Bootstrap 5

## 📝 Notas Importantes
- Cambiar las credenciales por defecto en producción
- Configurar SECRET_KEY segura en `config.py`
- Realizar backups periódicos de la base de datos
- El stock de medicamentos se reduce automáticamente al recetar

## 🐛 Solución de Problemas

### Error de conexión a PostgreSQL
- Verificar que PostgreSQL esté ejecutándose
- Verificar credenciales en `config.py`
- Verificar que la base de datos exista

### Error de dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 👨‍💻 Autor
Sistema creado para gestión veterinaria con Flask MVC

## 📄 Licencia
Este proyecto es de uso educativo y profesional
