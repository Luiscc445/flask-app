"""
Controlador de Veterinario
Gestiona las acciones de los veterinarios
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.cita import Cita
from app.models.medicamento import Medicamento, Receta
from datetime import datetime

veterinario_bp = Blueprint('veterinario', __name__)


def veterinario_required(f):
    """Decorador para rutas que requieren rol de veterinario"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_veterinario():
            flash('No tienes permisos para acceder a esta página.', 'danger')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function


@veterinario_bp.route('/dashboard')
@veterinario_required
def dashboard():
    """Dashboard del veterinario"""
    # Estadísticas
    citas_pendientes = Cita.query.filter_by(
        veterinario_id=current_user.id,
        estado='pendiente'
    ).count()

    citas_aceptadas = Cita.query.filter_by(
        veterinario_id=current_user.id,
        estado='aceptada'
    ).count()

    total_atendidas = Cita.query.filter_by(
        veterinario_id=current_user.id,
        estado='atendida'
    ).count()

    # Citas de hoy - CORREGIDO para SQL Server
    hoy = datetime.now().date()
    citas_hoy = Cita.query.filter_by(
        veterinario_id=current_user.id,
        estado='aceptada'
    ).filter(
        db.func.cast(Cita.fecha_hora, db.Date) == hoy
    ).order_by(Cita.fecha_hora.asc()).all()

    return render_template('veterinario/dashboard.html',
                         citas_pendientes=citas_pendientes,
                         citas_aceptadas=citas_aceptadas,
                         total_atendidas=total_atendidas,
                         citas_hoy=citas_hoy)


@veterinario_bp.route('/citas/pendientes')
@veterinario_required
def citas_pendientes():
    """Ver citas pendientes"""
    citas = Cita.query.filter_by(estado='pendiente').order_by(Cita.fecha_hora.asc()).all()
    return render_template('veterinario/citas_pendientes.html', citas=citas)


@veterinario_bp.route('/citas/mis-citas')
@veterinario_required
def mis_citas():
    """Ver mis citas aceptadas y atendidas"""
    citas = Cita.query.filter_by(veterinario_id=current_user.id).filter(
        Cita.estado.in_(['aceptada', 'atendida'])
    ).order_by(Cita.fecha_hora.desc()).all()

    return render_template('veterinario/mis_citas.html', citas=citas)


@veterinario_bp.route('/cita/<int:id>/aceptar', methods=['POST'])
@veterinario_required
def aceptar_cita(id):
    """Aceptar una cita pendiente"""
    cita = Cita.query.get_or_404(id)

    if cita.estado != 'pendiente':
        flash('Esta cita ya no está pendiente.', 'warning')
        return redirect(url_for('veterinario.citas_pendientes'))

    try:
        cita.aceptar(current_user.id)
        db.session.commit()
        flash('Cita aceptada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al aceptar cita: {str(e)}', 'danger')

    return redirect(url_for('veterinario.citas_pendientes'))


@veterinario_bp.route('/cita/<int:id>/posponer', methods=['GET', 'POST'])
@veterinario_required
def posponer_cita(id):
    """Posponer una cita"""
    cita = Cita.query.get_or_404(id)

    if cita.estado not in ['pendiente', 'aceptada']:
        flash('Esta cita no puede ser pospuesta.', 'warning')
        return redirect(url_for('veterinario.citas_pendientes'))

    if request.method == 'POST':
        motivo = request.form.get('motivo')
        nueva_fecha = request.form.get('nueva_fecha')
        nueva_hora = request.form.get('nueva_hora')

        if not motivo:
            flash('Debes proporcionar un motivo para posponer.', 'danger')
            return render_template('veterinario/posponer_cita.html', cita=cita)

        # Nueva fecha sugerida (opcional)
        nueva_fecha_hora = None
        if nueva_fecha and nueva_hora:
            try:
                nueva_fecha_hora = datetime.strptime(f"{nueva_fecha} {nueva_hora}", '%Y-%m-%d %H:%M')
            except ValueError:
                flash('Formato de fecha u hora inválido.', 'danger')
                return render_template('veterinario/posponer_cita.html', cita=cita)

        try:
            cita.posponer(motivo, nueva_fecha_hora)
            db.session.commit()
            flash('Cita pospuesta. El tutor será notificado.', 'success')
            return redirect(url_for('veterinario.citas_pendientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al posponer cita: {str(e)}', 'danger')

    return render_template('veterinario/posponer_cita.html', cita=cita)


@veterinario_bp.route('/cita/<int:id>/atender', methods=['GET', 'POST'])
@veterinario_required
def atender_cita(id):
    """Atender una cita"""
    cita = Cita.query.get_or_404(id)

    # Verificar que la cita está aceptada y asignada a este veterinario
    if cita.veterinario_id != current_user.id:
        flash('No tienes permiso para atender esta cita.', 'danger')
        return redirect(url_for('veterinario.mis_citas'))

    if cita.estado != 'aceptada':
        flash('Esta cita no puede ser atendida.', 'warning')
        return redirect(url_for('veterinario.mis_citas'))

    # Obtener medicamentos disponibles
    medicamentos = Medicamento.query.filter_by(activo=True).order_by(Medicamento.nombre.asc()).all()

    if request.method == 'POST':
        diagnostico = request.form.get('diagnostico')
        tratamiento = request.form.get('tratamiento')
        observaciones = request.form.get('observaciones')

        # Validaciones
        if not diagnostico or not tratamiento:
            flash('Diagnóstico y tratamiento son obligatorios.', 'danger')
            return render_template('veterinario/atender_cita.html', cita=cita, medicamentos=medicamentos)

        try:
            # Atender la cita
            cita.atender(diagnostico, tratamiento, observaciones)

            # Procesar medicamentos recetados
            medicamentos_ids = request.form.getlist('medicamento_id[]')
            cantidades = request.form.getlist('cantidad[]')
            dosis_list = request.form.getlist('dosis[]')
            duraciones = request.form.getlist('duracion[]')
            indicaciones = request.form.getlist('indicaciones[]')

            for i, med_id in enumerate(medicamentos_ids):
                if med_id and cantidades[i]:
                    medicamento = Medicamento.query.get(int(med_id))
                    cantidad = int(cantidades[i])

                    if medicamento and cantidad > 0:
                        # Verificar stock
                        if medicamento.stock < cantidad:
                            flash(f'Stock insuficiente de {medicamento.nombre}. Disponible: {medicamento.stock}', 'warning')
                            continue

                        # Crear receta
                        receta = Receta(
                            cita_id=cita.id,
                            medicamento_id=medicamento.id,
                            cantidad=cantidad,
                            dosis=dosis_list[i] if i < len(dosis_list) else None,
                            duracion=duraciones[i] if i < len(duraciones) else None,
                            indicaciones=indicaciones[i] if i < len(indicaciones) else None
                        )
                        db.session.add(receta)

                        # Reducir stock automáticamente
                        medicamento.reducir_stock(cantidad)

            db.session.commit()
            flash('Cita atendida exitosamente. Stock actualizado.', 'success')
            return redirect(url_for('veterinario.mis_citas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al atender cita: {str(e)}', 'danger')

    return render_template('veterinario/atender_cita.html', cita=cita, medicamentos=medicamentos)


@veterinario_bp.route('/cita/<int:id>')
@veterinario_required
def ver_cita(id):
    """Ver detalles de una cita"""
    cita = Cita.query.get_or_404(id)

    # Verificar permiso
    if cita.veterinario_id != current_user.id and cita.estado == 'pendiente':
        # Puede ver citas pendientes sin asignar
        pass
    elif cita.veterinario_id != current_user.id:
        flash('No tienes permiso para ver esta cita.', 'danger')
        return redirect(url_for('veterinario.dashboard'))

    return render_template('veterinario/ver_cita.html', cita=cita)


@veterinario_bp.route('/perfil', methods=['GET', 'POST'])
@veterinario_required
def perfil():
    """Ver y editar perfil del veterinario"""
    if request.method == 'POST':
        # Actualizar información
        current_user.nombre = request.form.get('nombre')
        current_user.apellido = request.form.get('apellido')
        current_user.email = request.form.get('email')
        current_user.telefono = request.form.get('telefono')
        current_user.especialidad = request.form.get('especialidad')
        current_user.licencia_profesional = request.form.get('licencia_profesional')

        # Cambiar contraseña si se proporciona
        password_actual = request.form.get('password_actual')
        password_nueva = request.form.get('password_nueva')
        password_confirmar = request.form.get('password_confirmar')

        if password_actual and password_nueva:
            if not current_user.check_password(password_actual):
                flash('La contraseña actual es incorrecta.', 'danger')
                return render_template('veterinario/perfil.html')

            if password_nueva != password_confirmar:
                flash('Las contraseñas nuevas no coinciden.', 'danger')
                return render_template('veterinario/perfil.html')

            if len(password_nueva) < 6:
                flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
                return render_template('veterinario/perfil.html')

            current_user.set_password(password_nueva)

        try:
            db.session.commit()
            flash('Perfil actualizado exitosamente.', 'success')
            return redirect(url_for('veterinario.perfil'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar perfil: {str(e)}', 'danger')

    return render_template('veterinario/perfil.html')
