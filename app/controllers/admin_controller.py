"""
Controlador de Administrador con funcionalidades completas
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, or_
from app import db
from app.models import (
    Usuario, Mascota, Cita, HistorialClinico, 
    Servicio, Medicamento, Notificacion, Vacuna,
    ConfiguracionSistema, AuditoriaAccion, DocumentoMascota,
    ServicioCita
)

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def registrar_auditoria(accion, entidad, entidad_id, descripcion, datos_anteriores=None, datos_nuevos=None):
    """Registra una acción en el sistema de auditoría"""
    auditoria = AuditoriaAccion(
        usuario_id=current_user.id,
        accion=accion,
        entidad=entidad,
        entidad_id=entidad_id,
        descripcion=descripcion,
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(auditoria)

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard principal del administrador con estadísticas"""
    # Estadísticas generales
    stats = {
        'total_usuarios': Usuario.query.count(),
        'total_veterinarios': Usuario.query.filter_by(rol='veterinario').count(),
        'total_tutores': Usuario.query.filter_by(rol='tutor').count(),
        'total_mascotas': Mascota.query.filter_by(activo=True).count(),
        'citas_hoy': Cita.query.filter(func.date(Cita.fecha) == date.today()).count(),
        'citas_pendientes': Cita.query.filter_by(estado='pendiente').count(),
        'citas_completadas_mes': Cita.query.filter(
            Cita.estado == 'completada',
            func.extract('month', Cita.fecha) == datetime.now().month,
            func.extract('year', Cita.fecha) == datetime.now().year
        ).count(),
        'medicamentos_bajo_stock': Medicamento.query.filter(
            Medicamento.stock_actual <= Medicamento.stock_minimo
        ).count()
    }
    
    # Ingresos del mes
    ingresos_mes = db.session.query(func.sum(Cita.costo)).filter(
        Cita.estado == 'completada',
        Cita.pagado == True,
        func.extract('month', Cita.fecha) == datetime.now().month,
        func.extract('year', Cita.fecha) == datetime.now().year
    ).scalar() or 0
    stats['ingresos_mes'] = ingresos_mes
    
    # Citas recientes
    citas_recientes = Cita.query.order_by(Cita.fecha_creacion.desc()).limit(5).all()
    
    # Próximas citas de hoy
    proximas_citas = Cita.query.filter(
        func.date(Cita.fecha) == date.today(),
        Cita.estado.in_(['pendiente', 'confirmada'])
    ).order_by(Cita.fecha).limit(10).all()
    
    # Gráficos de estadísticas
    # Datos para gráfico de citas por día (últimos 7 días)
    citas_semana = []
    for i in range(6, -1, -1):
        fecha = date.today() - timedelta(days=i)
        count = Cita.query.filter(func.date(Cita.fecha) == fecha).count()
        citas_semana.append({
            'fecha': fecha.strftime('%d/%m'),
            'cantidad': count
        })
    
    # Datos para gráfico de especies
    especies_data = db.session.query(
        Mascota.especie,
        func.count(Mascota.id)
    ).filter(Mascota.activo == True).group_by(Mascota.especie).all()
    
    # Top veterinarios por citas atendidas este mes
    top_veterinarios = db.session.query(
        Usuario,
        func.count(Cita.id).label('total_citas')
    ).join(
        Cita, Usuario.id == Cita.veterinario_id
    ).filter(
        Usuario.rol == 'veterinario',
        Cita.estado == 'completada',
        func.extract('month', Cita.fecha) == datetime.now().month
    ).group_by(Usuario.id).order_by(func.count(Cita.id).desc()).limit(5).all()
    
    # Notificaciones del sistema
    notificaciones_sistema = Notificacion.query.filter_by(
        usuario_id=current_user.id,
        leida=False
    ).order_by(Notificacion.fecha_creacion.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         citas_recientes=citas_recientes,
                         proximas_citas=proximas_citas,
                         citas_semana=citas_semana,
                         especies_data=especies_data,
                         top_veterinarios=top_veterinarios,
                         notificaciones_sistema=notificaciones_sistema)

@admin_bp.route('/tutores')
@admin_required
def tutores():
    """Lista de tutores con sus mascotas"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Usuario.query.filter_by(rol='tutor')
    
    if search:
        query = query.filter(
            or_(
                Usuario.nombre.ilike(f'%{search}%'),
                Usuario.apellido.ilike(f'%{search}%'),
                Usuario.email.ilike(f'%{search}%'),
                Usuario.cedula.ilike(f'%{search}%')
            )
        )
    
    tutores = query.paginate(page=page, per_page=10, error_out=False)
    
    # Agregar estadísticas para cada tutor
    for tutor in tutores.items:
        tutor.total_mascotas = tutor.mascotas.count()
        tutor.mascotas_activas = tutor.mascotas.filter_by(activo=True).count()
        tutor.total_citas = tutor.citas_como_tutor.count()
    
    return render_template('admin/tutores/lista.html', tutores=tutores, search=search)

@admin_bp.route('/tutor/<int:tutor_id>')
@admin_required
def ver_tutor(tutor_id):
    """Ver detalles de un tutor y sus mascotas"""
    tutor = Usuario.query.get_or_404(tutor_id)
    
    if tutor.rol != 'tutor':
        flash('El usuario especificado no es un tutor', 'warning')
        return redirect(url_for('admin.tutores'))
    
    # Obtener todas las mascotas del tutor
    mascotas = tutor.mascotas.all()
    
    # Obtener historial de citas
    citas = tutor.citas_como_tutor.order_by(Cita.fecha.desc()).limit(10).all()
    
    # Estadísticas del tutor
    stats = {
        'total_mascotas': len(mascotas),
        'mascotas_activas': sum(1 for m in mascotas if m.activo),
        'total_citas': tutor.citas_como_tutor.count(),
        'citas_completadas': tutor.citas_como_tutor.filter_by(estado='completada').count(),
        'proxima_cita': tutor.citas_como_tutor.filter(
            Cita.fecha >= datetime.now(),
            Cita.estado == 'pendiente'
        ).order_by(Cita.fecha).first()
    }
    
    registrar_auditoria('ver_tutor', 'usuario', tutor_id, f'Visualización de tutor: {tutor.nombre_completo}')
    
    return render_template('admin/tutores/ver.html',
                         tutor=tutor,
                         mascotas=mascotas,
                         citas=citas,
                         stats=stats)

@admin_bp.route('/mascota/<int:mascota_id>')
@admin_required
def ver_mascota(mascota_id):
    """Ver detalles completos de una mascota"""
    mascota = Mascota.query.get_or_404(mascota_id)
    
    # Historial médico
    historiales = mascota.historiales.order_by(HistorialClinico.fecha.desc()).limit(10).all()
    
    # Vacunas
    vacunas = mascota.vacunas.order_by(Vacuna.fecha_aplicacion.desc()).all()
    vacunas_pendientes = [v for v in vacunas if not v.aplicada and v.fecha_proxima <= date.today()]
    
    # Citas
    citas = mascota.citas.order_by(Cita.fecha.desc()).limit(10).all()
    proxima_cita = mascota.get_proxima_cita()
    
    # Documentos
    documentos = mascota.documentos.order_by(DocumentoMascota.fecha_subida.desc()).all()
    
    # Gráfico de peso
    historial_peso = mascota.get_historial_peso()
    
    registrar_auditoria('ver_mascota', 'mascota', mascota_id, f'Visualización de mascota: {mascota.nombre}')
    
    return render_template('admin/mascotas/ver.html',
                         mascota=mascota,
                         historiales=historiales,
                         vacunas=vacunas,
                         vacunas_pendientes=vacunas_pendientes,
                         citas=citas,
                         proxima_cita=proxima_cita,
                         documentos=documentos,
                         historial_peso=historial_peso)

@admin_bp.route('/veterinarios')
@admin_required
def veterinarios():
    """Lista de veterinarios con estadísticas"""
    page = request.args.get('page', 1, type=int)
    veterinarios = Usuario.query.filter_by(rol='veterinario').paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Agregar estadísticas para cada veterinario
    for vet in veterinarios.items:
        stats = vet.get_estadisticas_veterinario()
        vet.stats = stats
    
    return render_template('admin/veterinarios/lista.html', veterinarios=veterinarios)

@admin_bp.route('/veterinario/<int:vet_id>/estadisticas')
@admin_required
def estadisticas_veterinario(vet_id):
    """Ver estadísticas detalladas de un veterinario"""
    veterinario = Usuario.query.get_or_404(vet_id)
    
    if not veterinario.is_veterinario():
        flash('El usuario especificado no es un veterinario', 'warning')
        return redirect(url_for('admin.veterinarios'))
    
    # Estadísticas generales
    stats = veterinario.get_estadisticas_veterinario()
    
    # Citas por día de la semana
    citas_por_dia = db.session.query(
        func.strftime('%w', Cita.fecha).label('dia_semana'),
        func.count(Cita.id).label('total')
    ).filter(
        Cita.veterinario_id == vet_id,
        Cita.estado == 'completada'
    ).group_by('dia_semana').all()
    
    # Tipos de consulta más frecuentes
    tipos_consulta = db.session.query(
        Cita.tipo,
        func.count(Cita.id).label('total')
    ).filter(
        Cita.veterinario_id == vet_id
    ).group_by(Cita.tipo).order_by(func.count(Cita.id).desc()).limit(5).all()
    
    # Pacientes recurrentes
    pacientes_recurrentes = db.session.query(
        Mascota,
        func.count(Cita.id).label('total_visitas')
    ).join(Cita).filter(
        Cita.veterinario_id == vet_id,
        Cita.estado == 'completada'
    ).group_by(Mascota.id).order_by(func.count(Cita.id).desc()).limit(10).all()
    
    # Ingresos por mes (últimos 6 meses)
    ingresos_mensuales = []
    for i in range(5, -1, -1):
        fecha = datetime.now() - timedelta(days=i*30)
        ingresos = db.session.query(func.sum(Cita.costo)).filter(
            Cita.veterinario_id == vet_id,
            Cita.estado == 'completada',
            func.extract('month', Cita.fecha) == fecha.month,
            func.extract('year', Cita.fecha) == fecha.year
        ).scalar() or 0
        ingresos_mensuales.append({
            'mes': fecha.strftime('%B'),
            'ingresos': ingresos
        })
    
    return render_template('admin/veterinarios/estadisticas.html',
                         veterinario=veterinario,
                         stats=stats,
                         citas_por_dia=citas_por_dia,
                         tipos_consulta=tipos_consulta,
                         pacientes_recurrentes=pacientes_recurrentes,
                         ingresos_mensuales=ingresos_mensuales)

# API endpoints para gráficos dinámicos
@admin_bp.route('/api/estadisticas/citas-mes')
@admin_required
def api_estadisticas_citas_mes():
    """API para obtener estadísticas de citas del mes actual"""
    mes_actual = datetime.now().month
    año_actual = datetime.now().year
    
    # Citas por día del mes
    dias_mes = []
    for dia in range(1, 32):
        try:
            fecha = date(año_actual, mes_actual, dia)
            cantidad = Cita.query.filter(func.date(Cita.fecha) == fecha).count()
            dias_mes.append({
                'dia': dia,
                'cantidad': cantidad
            })
        except ValueError:
            break
    
    return jsonify(dias_mes)

@admin_bp.route('/api/estadisticas/especies')
@admin_required
def api_estadisticas_especies():
    """API para obtener distribución de especies"""
    especies = db.session.query(
        Mascota.especie,
        func.count(Mascota.id).label('cantidad')
    ).filter(Mascota.activo == True).group_by(Mascota.especie).all()
    
    return jsonify([{
        'especie': e.especie,
        'cantidad': e.cantidad
    } for e in especies])

# Más funciones continúan...
