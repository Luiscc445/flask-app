"""
Controlador de Administrador
Gestiona todas las acciones del administrador (CRUD completo)
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import Usuario
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.medicamento import Medicamento
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorador para rutas que requieren rol de administrador"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('No tienes permisos para acceder a esta pÃ¡gina.', 'danger')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Dashboard del administrador"""
    # EstadÃ­sticas generales
    total_tutores = Usuario.query.filter_by(rol='tutor').count()
    total_veterinarios = Usuario.query.filter_by(rol='veterinario').count()
    total_mascotas = Mascota.query.count()
    total_citas = Cita.query.count()
    total_medicamentos = Medicamento.query.filter_by(activo=True).count()
    
    # Citas pendientes
    citas_pendientes = Cita.query.filter_by(estado='pendiente').count()
    
    # Medicamentos con stock bajo
    medicamentos_bajo_stock = Medicamento.query.filter(
        Medicamento.stock <= Medicamento.stock_minimo,
        Medicamento.activo == True
    ).count()
    
    # Ãšltimos tutores registrados
    ultimos_tutores = Usuario.query.filter_by(rol='tutor').order_by(
        Usuario.fecha_registro.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_tutores=total_tutores,
                         total_veterinarios=total_veterinarios,
                         total_mascotas=total_mascotas,
                         total_citas=total_citas,
                         total_medicamentos=total_medicamentos,
                         citas_pendientes=citas_pendientes,
                         medicamentos_bajo_stock=medicamentos_bajo_stock,
                         ultimos_tutores=ultimos_tutores)


# ============= GESTIÃ“N DE TUTORES =============

@admin_bp.route('/tutores')
@admin_required
def tutores():
    """Lista de tutores"""
    tutores = Usuario.query.filter_by(rol='tutor').order_by(Usuario.fecha_registro.desc()).all()
    return render_template('admin/tutores/lista.html', tutores=tutores)


@admin_bp.route('/tutor/<int:id>')
@admin_required
def ver_tutor(id):
    """Ver detalles de un tutor"""
    tutor = Usuario.query.get_or_404(id)
    
    if tutor.rol != 'tutor':
        flash('Usuario no es un tutor.', 'danger')
        return redirect(url_for('admin.tutores'))
    
    # Obtener mascotas y citas del tutor
    mascotas = Mascota.query.filter_by(tutor_id=id).all()
    citas = Cita.query.filter_by(tutor_id=id).order_by(Cita.fecha_hora.desc()).limit(10).all()
    
    return render_template('admin/tutores/ver.html', tutor=tutor, mascotas=mascotas, citas=citas)


@admin_bp.route('/tutor/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_tutor():
    """Crear nuevo tutor"""
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        
        # Validaciones
        if not all([username, email, password, nombre, apellido]):
            flash('Por favor complete todos los campos obligatorios.', 'danger')
            return render_template('admin/tutores/nuevo.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
            return render_template('admin/tutores/nuevo.html')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso.', 'danger')
            return render_template('admin/tutores/nuevo.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado.', 'danger')
            return render_template('admin/tutores/nuevo.html')
        
        # Crear nuevo tutor
        try:
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
            
            db.session.add(nuevo_tutor)
            db.session.commit()
            flash(f'Tutor {nombre} {apellido} creado exitosamente. Usuario: {username}', 'success')
            return redirect(url_for('admin.tutores'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear tutor: {str(e)}', 'danger')
    
    return render_template('admin/tutores/nuevo.html')


@admin_bp.route('/tutor/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_tutor(id):
    """Editar informaciÃ³n de un tutor"""
    tutor = Usuario.query.get_or_404(id)
    
    if tutor.rol != 'tutor':
        flash('Usuario no es un tutor.', 'danger')
        return redirect(url_for('admin.tutores'))
    
    if request.method == 'POST':
        # Actualizar informaciÃ³n
        tutor.nombre = request.form.get('nombre')
        tutor.apellido = request.form.get('apellido')
        tutor.email = request.form.get('email')
        tutor.telefono = request.form.get('telefono')
        tutor.direccion = request.form.get('direccion')
        tutor.activo = request.form.get('activo') == 'on'
        
        # Cambiar contraseÃ±a si se proporciona
        nueva_password = request.form.get('nueva_password')
        if nueva_password:
            if len(nueva_password) < 6:
                flash('La contraseÃ±a debe tener al menos 6 caracteres.', 'danger')
                return render_template('admin/tutores/editar.html', tutor=tutor)
            tutor.set_password(nueva_password)
        
        try:
            db.session.commit()
            flash('Tutor actualizado exitosamente.', 'success')
            return redirect(url_for('admin.ver_tutor', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar tutor: {str(e)}', 'danger')
    
    return render_template('admin/tutores/editar.html', tutor=tutor)


@admin_bp.route('/tutor/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_tutor(id):
    """Eliminar (desactivar) un tutor"""
    tutor = Usuario.query.get_or_404(id)
    
    if tutor.rol != 'tutor':
        flash('Usuario no es un tutor.', 'danger')
        return redirect(url_for('admin.tutores'))
    
    try:
        # En lugar de eliminar, desactivar
        tutor.activo = False
        db.session.commit()
        flash('Tutor desactivado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desactivar tutor: {str(e)}', 'danger')
    
    return redirect(url_for('admin.tutores'))


# ============= GESTIÃ“N DE VETERINARIOS =============

@admin_bp.route('/veterinarios')
@admin_required
def veterinarios():
    """Lista de veterinarios"""
    veterinarios = Usuario.query.filter_by(rol='veterinario').order_by(Usuario.nombre.asc()).all()
    return render_template('admin/veterinarios/lista.html', veterinarios=veterinarios)


@admin_bp.route('/veterinario/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_veterinario():
    """Crear nuevo veterinario"""
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        especialidad = request.form.get('especialidad')
        licencia = request.form.get('licencia')
        
        # Validaciones
        if not all([username, email, password, nombre, apellido]):
            flash('Por favor complete todos los campos obligatorios.', 'danger')
            return render_template('admin/veterinarios/nuevo.html')
        
        if len(password) < 6:
            flash('La contraseÃ±a debe tener al menos 6 caracteres.', 'danger')
            return render_template('admin/veterinarios/nuevo.html')
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya estÃ¡ en uso.', 'danger')
            return render_template('admin/veterinarios/nuevo.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrÃ³nico ya estÃ¡ registrado.', 'danger')
            return render_template('admin/veterinarios/nuevo.html')
        
        # Crear nuevo veterinario
        try:
            nuevo_vet = Usuario(
                username=username,
                email=email,
                password=password,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                rol='veterinario',
                especialidad=especialidad,
                licencia_profesional=licencia
            )
            
            db.session.add(nuevo_vet)
            db.session.commit()
            flash(f'Veterinario {nombre} {apellido} creado exitosamente. Usuario: {username}', 'success')
            return redirect(url_for('admin.veterinarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear veterinario: {str(e)}', 'danger')
    
    return render_template('admin/veterinarios/nuevo.html')


@admin_bp.route('/veterinario/<int:id>')
@admin_required
def ver_veterinario(id):
    """Ver detalles de un veterinario"""
    veterinario = Usuario.query.get_or_404(id)
    
    if veterinario.rol != 'veterinario':
        flash('Usuario no es un veterinario.', 'danger')
        return redirect(url_for('admin.veterinarios'))
    
    # Obtener citas atendidas
    citas = Cita.query.filter_by(veterinario_id=id).order_by(Cita.fecha_hora.desc()).limit(10).all()
    
    return render_template('admin/veterinarios/ver.html', veterinario=veterinario, citas=citas)


@admin_bp.route('/veterinario/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_veterinario(id):
    """Editar informaciÃ³n de un veterinario"""
    veterinario = Usuario.query.get_or_404(id)
    
    if veterinario.rol != 'veterinario':
        flash('Usuario no es un veterinario.', 'danger')
        return redirect(url_for('admin.veterinarios'))
    
    if request.method == 'POST':
        # Actualizar informaciÃ³n
        veterinario.nombre = request.form.get('nombre')
        veterinario.apellido = request.form.get('apellido')
        veterinario.email = request.form.get('email')
        veterinario.telefono = request.form.get('telefono')
        veterinario.especialidad = request.form.get('especialidad')
        veterinario.licencia_profesional = request.form.get('licencia')
        veterinario.activo = request.form.get('activo') == 'on'
        
        # Cambiar contraseÃ±a si se proporciona
        nueva_password = request.form.get('nueva_password')
        if nueva_password:
            if len(nueva_password) < 6:
                flash('La contraseÃ±a debe tener al menos 6 caracteres.', 'danger')
                return render_template('admin/veterinarios/editar.html', veterinario=veterinario)
            veterinario.set_password(nueva_password)
        
        try:
            db.session.commit()
            flash('Veterinario actualizado exitosamente.', 'success')
            return redirect(url_for('admin.ver_veterinario', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar veterinario: {str(e)}', 'danger')
    
    return render_template('admin/veterinarios/editar.html', veterinario=veterinario)


@admin_bp.route('/veterinario/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_veterinario(id):
    """Eliminar (desactivar) un veterinario"""
    veterinario = Usuario.query.get_or_404(id)
    
    if veterinario.rol != 'veterinario':
        flash('Usuario no es un veterinario.', 'danger')
        return redirect(url_for('admin.veterinarios'))
    
    try:
        # En lugar de eliminar, desactivar
        veterinario.activo = False
        db.session.commit()
        flash('Veterinario desactivado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desactivar veterinario: {str(e)}', 'danger')
    
    return redirect(url_for('admin.veterinarios'))


# ============= GESTIÃ“N DE INVENTARIO (MEDICAMENTOS) =============

@admin_bp.route('/inventario')
@admin_required
def inventario():
    """Lista de medicamentos"""
    medicamentos = Medicamento.query.order_by(Medicamento.nombre.asc()).all()
    return render_template('admin/inventario/lista.html', medicamentos=medicamentos)


@admin_bp.route('/medicamento/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_medicamento():
    """Crear nuevo medicamento"""
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        principio_activo = request.form.get('principio_activo')
        presentacion = request.form.get('presentacion')
        concentracion = request.form.get('concentracion')
        stock = request.form.get('stock', 0)
        stock_minimo = request.form.get('stock_minimo', 10)
        unidad_medida = request.form.get('unidad_medida', 'unidades')
        lote = request.form.get('lote')
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        proveedor = request.form.get('proveedor')
        precio = request.form.get('precio')
        
        # Validaciones
        if not nombre:
            flash('El nombre del medicamento es obligatorio.', 'danger')
            return render_template('admin/inventario/nuevo.html')
        
        # Convertir valores numÃ©ricos
        try:
            stock = int(stock)
            stock_minimo = int(stock_minimo)
        except ValueError:
            flash('Stock debe ser un nÃºmero entero.', 'danger')
            return render_template('admin/inventario/nuevo.html')
        
        precio_float = None
        if precio:
            try:
                precio_float = float(precio)
            except ValueError:
                flash('Precio debe ser un nÃºmero vÃ¡lido.', 'danger')
                return render_template('admin/inventario/nuevo.html')
        
        # Fecha de vencimiento
        fecha_venc = None
        if fecha_vencimiento:
            try:
                fecha_venc = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha invÃ¡lido.', 'danger')
                return render_template('admin/inventario/nuevo.html')
        
        # Crear medicamento
        nuevo_med = Medicamento(
            nombre=nombre,
            descripcion=descripcion,
            principio_activo=principio_activo,
            presentacion=presentacion,
            concentracion=concentracion,
            stock=stock,
            stock_minimo=stock_minimo,
            unidad_medida=unidad_medida,
            lote=lote,
            fecha_vencimiento=fecha_venc,
            proveedor=proveedor,
            precio_unitario=precio_float
        )
        
        try:
            db.session.add(nuevo_med)
            db.session.commit()
            flash(f'Medicamento {nombre} creado exitosamente.', 'success')
            return redirect(url_for('admin.inventario'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear medicamento: {str(e)}', 'danger')
    
    return render_template('admin/inventario/nuevo.html')


@admin_bp.route('/medicamento/<int:id>')
@admin_required
def ver_medicamento(id):
    """Ver detalles de un medicamento"""
    medicamento = Medicamento.query.get_or_404(id)
    return render_template('admin/inventario/ver.html', medicamento=medicamento)


@admin_bp.route('/medicamento/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def editar_medicamento(id):
    """Editar informaciÃ³n de un medicamento"""
    medicamento = Medicamento.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizar informaciÃ³n
        medicamento.nombre = request.form.get('nombre')
        medicamento.descripcion = request.form.get('descripcion')
        medicamento.principio_activo = request.form.get('principio_activo')
        medicamento.presentacion = request.form.get('presentacion')
        medicamento.concentracion = request.form.get('concentracion')
        medicamento.unidad_medida = request.form.get('unidad_medida')
        medicamento.lote = request.form.get('lote')
        medicamento.proveedor = request.form.get('proveedor')
        medicamento.activo = request.form.get('activo') == 'on'
        
        # Stock
        stock = request.form.get('stock')
        if stock:
            try:
                medicamento.stock = int(stock)
            except ValueError:
                flash('Stock debe ser un nÃºmero entero.', 'danger')
                return render_template('admin/inventario/editar.html', medicamento=medicamento)
        
        # Stock mÃ­nimo
        stock_minimo = request.form.get('stock_minimo')
        if stock_minimo:
            try:
                medicamento.stock_minimo = int(stock_minimo)
            except ValueError:
                flash('Stock mÃ­nimo debe ser un nÃºmero entero.', 'danger')
                return render_template('admin/inventario/editar.html', medicamento=medicamento)
        
        # Precio
        precio = request.form.get('precio')
        if precio:
            try:
                medicamento.precio_unitario = float(precio)
            except ValueError:
                pass
        
        # Fecha de vencimiento
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        if fecha_vencimiento:
            try:
                medicamento.fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        try:
            db.session.commit()
            flash('Medicamento actualizado exitosamente.', 'success')
            return redirect(url_for('admin.ver_medicamento', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar medicamento: {str(e)}', 'danger')
    
    return render_template('admin/inventario/editar.html', medicamento=medicamento)


@admin_bp.route('/medicamento/<int:id>/eliminar', methods=['POST'])
@admin_required
def eliminar_medicamento(id):
    """Eliminar (desactivar) un medicamento"""
    medicamento = Medicamento.query.get_or_404(id)
    
    try:
        # En lugar de eliminar, desactivar
        medicamento.activo = False
        db.session.commit()
        flash('Medicamento desactivado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desactivar medicamento: {str(e)}', 'danger')
    
    return redirect(url_for('admin.inventario'))


# ============= REPORTES Y ESTADÃSTICAS =============

@admin_bp.route('/reportes')
@admin_required
def reportes():
    """PÃ¡gina de reportes"""
    # Citas por estado
    citas_por_estado = db.session.query(
        Cita.estado,
        db.func.count(Cita.id)
    ).group_by(Cita.estado).all()
    
    # Medicamentos con stock bajo
    medicamentos_bajo_stock = Medicamento.query.filter(
        Medicamento.stock <= Medicamento.stock_minimo,
        Medicamento.activo == True
    ).all()
    
    # Veterinarios mÃ¡s activos
    veterinarios_activos = db.session.query(
        Usuario,
        db.func.count(Cita.id).label('total_citas')
    ).join(Cita, Usuario.id == Cita.veterinario_id).filter(
        Usuario.rol == 'veterinario'
    ).group_by(
        Usuario.id,
        Usuario.username,
        Usuario.email,
        Usuario.password_hash,
        Usuario.nombre,
        Usuario.apellido,
        Usuario.telefono,
        Usuario.direccion,
        Usuario.rol,
        Usuario.activo,
        Usuario.especialidad,
        Usuario.licencia_profesional,
        Usuario.fecha_registro,
        Usuario.ultima_actualizacion
    ).order_by(db.desc('total_citas')).limit(5).all()
    
    return render_template('admin/reportes.html',
                         citas_por_estado=citas_por_estado,
                         medicamentos_bajo_stock=medicamentos_bajo_stock,
                         veterinarios_activos=veterinarios_activos)

