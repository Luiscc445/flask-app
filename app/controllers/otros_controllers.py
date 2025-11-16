"""
Controladores adicionales para el sistema
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
from app import db
from app.models import *

# Controlador de Veterinario
veterinario_bp = Blueprint('veterinario', __name__)

def veterinario_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_veterinario():
            flash('Acceso denegado', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@veterinario_bp.route('/dashboard')
@veterinario_required
def dashboard():
    stats = current_user.get_estadisticas_veterinario()
    citas_hoy = current_user.citas_como_veterinario.filter(
        func.date(Cita.fecha) == date.today()
    ).all()
    return render_template('veterinario/dashboard.html', stats=stats, citas_hoy=citas_hoy)

@veterinario_bp.route('/citas_hoy')
@veterinario_required
def citas_hoy():
    citas = current_user.citas_como_veterinario.filter(
        func.date(Cita.fecha) == date.today()
    ).order_by(Cita.fecha).all()
    return render_template('veterinario/citas_hoy.html', citas=citas)

@veterinario_bp.route('/mis_citas')
@veterinario_required
def mis_citas():
    page = request.args.get('page', 1, type=int)
    citas = current_user.citas_como_veterinario.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('veterinario/mis_citas.html', citas=citas)

@veterinario_bp.route('/historial_pacientes')
@veterinario_required
def historial_pacientes():
    # Obtener pacientes únicos atendidos
    pacientes = db.session.query(Mascota).join(Cita).filter(
        Cita.veterinario_id == current_user.id
    ).distinct().all()
    return render_template('veterinario/historial_pacientes.html', pacientes=pacientes)

@veterinario_bp.route('/estadisticas')
@veterinario_required
def estadisticas():
    stats = current_user.get_estadisticas_veterinario()
    return render_template('veterinario/estadisticas.html', stats=stats)

@veterinario_bp.route('/perfil')
@veterinario_required
def perfil():
    return render_template('veterinario/perfil.html')

@veterinario_bp.route('/notificaciones')
@veterinario_required
def notificaciones():
    notifs = current_user.notificaciones.order_by(
        Notificacion.fecha_creacion.desc()
    ).all()
    return render_template('veterinario/notificaciones.html', notificaciones=notifs)

# Controlador de Tutor
tutor_bp = Blueprint('tutor', __name__)

def tutor_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_tutor():
            flash('Acceso denegado', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@tutor_bp.route('/dashboard')
@tutor_required
def dashboard():
    stats = current_user.get_estadisticas_tutor()
    return render_template('tutor/dashboard.html', stats=stats)

@tutor_bp.route('/mascotas')
@tutor_required
def mascotas():
    mascotas = current_user.mascotas.all()
    return render_template('tutor/mascotas.html', mascotas=mascotas)

@tutor_bp.route('/citas')
@tutor_required
def citas():
    page = request.args.get('page', 1, type=int)
    citas = current_user.citas_como_tutor.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('tutor/citas.html', citas=citas)

@tutor_bp.route('/nueva_cita')
@tutor_required
def nueva_cita():
    mascotas = current_user.mascotas.filter_by(activo=True).all()
    servicios = Servicio.query.filter_by(activo=True).all()
    return render_template('tutor/nueva_cita.html', mascotas=mascotas, servicios=servicios)

@tutor_bp.route('/historial')
@tutor_required
def historial():
    historiales = []
    for mascota in current_user.mascotas:
        for h in mascota.historiales:
            historiales.append(h)
    historiales.sort(key=lambda x: x.fecha, reverse=True)
    return render_template('tutor/historial.html', historiales=historiales[:20])

@tutor_bp.route('/perfil')
@tutor_required
def perfil():
    return render_template('tutor/perfil.html')

@tutor_bp.route('/notificaciones')
@tutor_required
def notificaciones():
    notifs = current_user.notificaciones.order_by(
        Notificacion.fecha_creacion.desc()
    ).all()
    return render_template('tutor/notificaciones.html', notificaciones=notifs)

# Controlador de Recepcionista
recepcionista_bp = Blueprint('recepcionista', __name__)

def recepcionista_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_recepcionista():
            flash('Acceso denegado', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@recepcionista_bp.route('/dashboard')
@recepcionista_required
def dashboard():
    citas_hoy = Cita.query.filter(
        func.date(Cita.fecha) == date.today()
    ).all()
    return render_template('recepcionista/dashboard.html', citas_hoy=citas_hoy)

# Controlador API
api_bp = Blueprint('api', __name__)

@api_bp.route('/mascotas/<int:tutor_id>')
@login_required
def get_mascotas_tutor(tutor_id):
    if not current_user.is_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    tutor = Usuario.query.get_or_404(tutor_id)
    mascotas = [{
        'id': m.id,
        'nombre': m.nombre,
        'especie': m.especie,
        'raza': m.raza,
        'edad': m.edad_detallada,
        'activo': m.activo
    } for m in tutor.mascotas]
    
    return jsonify(mascotas)

@api_bp.route('/estadisticas/dashboard')
@login_required
def estadisticas_dashboard():
    if not current_user.is_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    stats = {
        'citas_semana': [],
        'especies': [],
        'ingresos_dia': []
    }
    
    # Lógica para obtener estadísticas
    
    return jsonify(stats)
