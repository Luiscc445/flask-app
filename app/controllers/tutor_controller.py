"""
Controlador de Tutor
Gestiona las acciones de los tutores de mascotas
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import Usuario
from app.models.mascota import Mascota
from app.models.cita import Cita
from datetime import datetime

tutor_bp = Blueprint('tutor', __name__)


def tutor_required(f):
    """Decorador para rutas que requieren rol de tutor"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_tutor():
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function


@tutor_bp.route('/dashboard')
@tutor_required
def dashboard():
    """Dashboard del tutor"""
    # Obtener estadísticas
    total_mascotas = Mascota.query.filter_by(tutor_id=current_user.id, activo=True).count()
    total_citas = Cita.query.filter_by(tutor_id=current_user.id).count()
    citas_pendientes = Cita.query.filter_by(
        tutor_id=current_user.id,
        estado='pendiente'
    ).count()
    citas_proximas = Cita.query.filter_by(
        tutor_id=current_user.id,
        estado='aceptada'
    ).filter(
        Cita.fecha_hora >= datetime.now()
    ).order_by(Cita.fecha_hora.asc()).limit(5).all()

    return render_template('tutor/dashboard.html',
                         total_mascotas=total_mascotas,
                         total_citas=total_citas,
                         citas_pendientes=citas_pendientes,
                         citas_proximas=citas_proximas)


@tutor_bp.route('/mascotas')
@tutor_required
def mascotas():
    """Lista de mascotas del tutor"""
    mis_mascotas = Mascota.query.filter_by(
        tutor_id=current_user.id,
        activo=True
    ).order_by(Mascota.nombre.asc()).all()

    return render_template('tutor/mascotas.html', mascotas=mis_mascotas)


@tutor_bp.route('/mascota/nueva', methods=['GET', 'POST'])
@tutor_required
def nueva_mascota():
    """Registrar nueva mascota"""
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        especie = request.form.get('especie')
        raza = request.form.get('raza')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        sexo = request.form.get('sexo')
        color = request.form.get('color')
        peso = request.form.get('peso')
        esterilizado = request.form.get('esterilizado') == 'on'
        chip = request.form.get('chip')
        observaciones = request.form.get('observaciones')

        # Validaciones
        if not nombre or not especie:
            flash('Nombre y especie son obligatorios.', 'danger')
            return render_template('tutor/nueva_mascota.html')

        # Convertir fecha
        fecha_nac = None
        if fecha_nacimiento:
            try:
                fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha inválido.', 'danger')
                return render_template('tutor/nueva_mascota.html')

        # Convertir peso
        peso_float = None
        if peso:
            try:
                peso_float = float(peso)
            except ValueError:
                flash('El peso debe ser un número válido.', 'danger')
                return render_template('tutor/nueva_mascota.html')

        # Crear mascota
        nueva_mascota = Mascota(
            nombre=nombre,
            especie=especie,
            tutor_id=current_user.id,
            raza=raza,
            fecha_nacimiento=fecha_nac,
            sexo=sexo,
            color=color,
            peso=peso_float,
            esterilizado=esterilizado,
            chip_identificacion=chip,
            observaciones=observaciones
        )

        try:
            db.session.add(nueva_mascota)
            db.session.commit()
            flash(f'¡Mascota {nombre} registrada exitosamente!', 'success')
            return redirect(url_for('tutor.mascotas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar mascota: {str(e)}', 'danger')

    return render_template('tutor/nueva_mascota.html')


@tutor_bp.route('/mascota/<int:id>')
@tutor_required
def ver_mascota(id):
    """Ver detalles de una mascota"""
    mascota = Mascota.query.get_or_404(id)

    # Verificar que la mascota pertenece al tutor
    if mascota.tutor_id != current_user.id:
        flash('No tienes permiso para ver esta mascota.', 'danger')
        return redirect(url_for('tutor.mascotas'))

    # Obtener historial de citas
    citas = Cita.query.filter_by(mascota_id=id).order_by(Cita.fecha_hora.desc()).all()

    return render_template('tutor/ver_mascota.html', mascota=mascota, citas=citas)


@tutor_bp.route('/mascota/<int:id>/editar', methods=['GET', 'POST'])
@tutor_required
def editar_mascota(id):
    """Editar información de mascota"""
    mascota = Mascota.query.get_or_404(id)

    # Verificar que la mascota pertenece al tutor
    if mascota.tutor_id != current_user.id:
        flash('No tienes permiso para editar esta mascota.', 'danger')
        return redirect(url_for('tutor.mascotas'))

    if request.method == 'POST':
        # Actualizar datos
        mascota.nombre = request.form.get('nombre')
        mascota.especie = request.form.get('especie')
        mascota.raza = request.form.get('raza')
        mascota.sexo = request.form.get('sexo')
        mascota.color = request.form.get('color')
        mascota.esterilizado = request.form.get('esterilizado') == 'on'
        mascota.chip_identificacion = request.form.get('chip')
        mascota.observaciones = request.form.get('observaciones')

        # Fecha de nacimiento
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        if fecha_nacimiento:
            try:
                mascota.fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                pass

        # Peso
        peso = request.form.get('peso')
        if peso:
            try:
                mascota.peso = float(peso)
            except ValueError:
                pass

        try:
            db.session.commit()
            flash('Información de mascota actualizada exitosamente.', 'success')
            return redirect(url_for('tutor.ver_mascota', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar mascota: {str(e)}', 'danger')

    return render_template('tutor/editar_mascota.html', mascota=mascota)


@tutor_bp.route('/citas')
@tutor_required
def citas():
    """Lista de citas del tutor"""
    mis_citas = Cita.query.filter_by(tutor_id=current_user.id).order_by(Cita.fecha_hora.desc()).all()
    return render_template('tutor/citas.html', citas=mis_citas)


@tutor_bp.route('/cita/nueva', methods=['GET', 'POST'])
@tutor_required
def nueva_cita():
    """Solicitar nueva cita médica"""
    # Obtener mascotas del tutor
    mascotas = Mascota.query.filter_by(tutor_id=current_user.id, activo=True).all()

    if not mascotas:
        flash('Debes registrar al menos una mascota antes de solicitar una cita.', 'warning')
        return redirect(url_for('tutor.nueva_mascota'))

    # Obtener veterinarios activos
    veterinarios = Usuario.query.filter_by(rol='veterinario', activo=True).all()

    if request.method == 'POST':
        mascota_id = request.form.get('mascota_id')
        veterinario_id = request.form.get('veterinario_id')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        motivo = request.form.get('motivo')

        # Validaciones
        if not all([mascota_id, veterinario_id, fecha, hora, motivo]):
            flash('Por favor complete todos los campos.', 'danger')
            return render_template('tutor/nueva_cita.html', mascotas=mascotas, veterinarios=veterinarios)

        # Verificar que la mascota pertenece al tutor
        mascota = Mascota.query.get(mascota_id)
        if not mascota or mascota.tutor_id != current_user.id:
            flash('Mascota no válida.', 'danger')
            return render_template('tutor/nueva_cita.html', mascotas=mascotas, veterinarios=veterinarios)

        # Verificar que el veterinario existe
        veterinario = Usuario.query.get(veterinario_id)
        if not veterinario or veterinario.rol != 'veterinario':
            flash('Veterinario no válido.', 'danger')
            return render_template('tutor/nueva_cita.html', mascotas=mascotas, veterinarios=veterinarios)

        # Combinar fecha y hora
        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
        except ValueError:
            flash('Formato de fecha u hora inválido.', 'danger')
            return render_template('tutor/nueva_cita.html', mascotas=mascotas, veterinarios=veterinarios)

        # Verificar que la fecha sea futura
        if fecha_hora < datetime.now():
            flash('La fecha de la cita debe ser futura.', 'danger')
            return render_template('tutor/nueva_cita.html', mascotas=mascotas, veterinarios=veterinarios)

        # Crear cita con veterinario asignado
        nueva_cita = Cita(
            mascota_id=mascota_id,
            tutor_id=current_user.id,
            veterinario_id=veterinario_id,
            fecha_hora=fecha_hora,
            motivo=motivo,
            estado='pendiente'
        )

        try:
            db.session.add(nueva_cita)
            db.session.commit()
            flash(f'¡Cita solicitada exitosamente con Dr(a). {veterinario.nombre_completo}! Espera la confirmación.', 'success')
            return redirect(url_for('tutor.citas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al solicitar cita: {str(e)}', 'danger')

    return render_template('tutor/nueva_cita.html', mascotas=mascotas, veterinarios=veterinarios)


@tutor_bp.route('/cita/<int:id>')
@tutor_required
def ver_cita(id):
    """Ver detalles de una cita"""
    cita = Cita.query.get_or_404(id)

    # Verificar que la cita pertenece al tutor
    if cita.tutor_id != current_user.id:
        flash('No tienes permiso para ver esta cita.', 'danger')
        return redirect(url_for('tutor.citas'))

    return render_template('tutor/ver_cita.html', cita=cita)


@tutor_bp.route('/perfil', methods=['GET', 'POST'])
@tutor_required
def perfil():
    """Ver y editar perfil del tutor"""
    if request.method == 'POST':
        # Actualizar información
        current_user.nombre = request.form.get('nombre')
        current_user.apellido = request.form.get('apellido')
        current_user.email = request.form.get('email')
        current_user.telefono = request.form.get('telefono')
        current_user.direccion = request.form.get('direccion')

        # Cambiar contraseña si se proporciona
        password_actual = request.form.get('password_actual')
        password_nueva = request.form.get('password_nueva')
        password_confirmar = request.form.get('password_confirmar')

        if password_actual and password_nueva:
            if not current_user.check_password(password_actual):
                flash('La contraseña actual es incorrecta.', 'danger')
                return render_template('tutor/perfil.html')

            if password_nueva != password_confirmar:
                flash('Las contraseñas nuevas no coinciden.', 'danger')
                return render_template('tutor/perfil.html')

            if len(password_nueva) < 6:
                flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
                return render_template('tutor/perfil.html')

            current_user.set_password(password_nueva)

        try:
            db.session.commit()
            flash('Perfil actualizado exitosamente.', 'success')
            return redirect(url_for('tutor.perfil'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar perfil: {str(e)}', 'danger')

    return render_template('tutor/perfil.html')
