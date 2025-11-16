"""
Controlador de Autenticación
Gestiona login, logout y registro de tutores
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import Usuario
from urllib.parse import urlparse  # ← CAMBIADO

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Página principal que redirige según el usuario"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_veterinario():
            return redirect(url_for('veterinario.dashboard'))
        elif current_user.is_tutor():
            return redirect(url_for('tutor.dashboard'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Validar campos
        if not username or not password:
            flash('Por favor complete todos los campos.', 'danger')
            return render_template('auth/login.html')
        
        # Buscar usuario
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Verificar usuario y contraseña
        if usuario is None or not usuario.check_password(password):
            flash('Usuario o contraseña incorrectos.', 'danger')
            return render_template('auth/login.html')
        
        # Verificar si está activo
        if not usuario.activo:
            flash('Tu cuenta está inactiva. Contacta al administrador.', 'warning')
            return render_template('auth/login.html')
        
        # Iniciar sesión
        login_user(usuario, remember=remember)
        
        flash(f'¡Bienvenido {usuario.nombre}!', 'success')
        
        # Redirigir a la página solicitada o al dashboard correspondiente
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':  # ← CAMBIADO
            if usuario.is_admin():
                next_page = url_for('admin.dashboard')
            elif usuario.is_veterinario():
                next_page = url_for('veterinario.dashboard')
            else:
                next_page = url_for('tutor.dashboard')
        
        return redirect(next_page)
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos tutores"""
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        
        # Validaciones
        if not all([username, email, password, confirm_password, nombre, apellido]):
            flash('Por favor complete todos los campos obligatorios.', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return render_template('auth/register.html')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('auth/register.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado.', 'danger')
            return render_template('auth/register.html')
        
        # Crear nuevo tutor
        nuevo_tutor = Usuario(
            username=username,
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            rol='tutor'
        )
        
        try:
            db.session.add(nuevo_tutor)
            db.session.commit()
            
            flash(f'¡Registro exitoso! Bienvenido {nombre}.', 'success')
            
            # Iniciar sesión automáticamente
            login_user(nuevo_tutor)
            
            return redirect(url_for('tutor.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar usuario: {str(e)}', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('auth.login'))