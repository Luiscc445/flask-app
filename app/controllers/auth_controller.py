"""
Controlador de Autenticación
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Usuario
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.rol}.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = Usuario.query.filter_by(username=username).first()
        
        if not user:
            # Intentar con email
            user = Usuario.query.filter_by(email=username).first()
        
        if user and user.check_password(password):
            if not user.activo:
                flash('Tu cuenta ha sido desactivada. Contacta al administrador.', 'warning')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=remember)
            user.actualizar_ultimo_acceso()
            
            # Registrar en auditoría
            from app.controllers.admin_controller import registrar_auditoria
            registrar_auditoria('login', 'usuario', user.id, f'Inicio de sesión: {user.nombre_completo}')
            
            flash(f'Bienvenido, {user.nombre}!', 'success')
            
            # Redirigir según el rol
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for(f'{user.rol}.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    from app.controllers.admin_controller import registrar_auditoria
    registrar_auditoria('logout', 'usuario', current_user.id, f'Cierre de sesión: {current_user.nombre_completo}')
    
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos usuarios (solo tutores)"""
    if current_user.is_authenticated:
        return redirect(url_for(f'{current_user.rol}.dashboard'))
    
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
        errors = []
        
        if Usuario.query.filter_by(username=username).first():
            errors.append('El nombre de usuario ya está registrado')
        
        if Usuario.query.filter_by(email=email).first():
            errors.append('El email ya está registrado')
        
        if password != confirm_password:
            errors.append('Las contraseñas no coinciden')
        
        if len(password) < 6:
            errors.append('La contraseña debe tener al menos 6 caracteres')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/register.html')
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            direccion=direccion,
            rol='tutor',
            activo=True
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Recuperación de contraseña"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = Usuario.query.filter_by(email=email).first()
        
        if user:
            # Aquí implementarías el envío de email con token de recuperación
            flash('Se ha enviado un enlace de recuperación a tu email', 'info')
        else:
            flash('No se encontró ninguna cuenta con ese email', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')
