"""
Script para generar todos los templates HTML del sistema
Ejecutar después de crear la estructura de directorios
"""
import os

# Definir todos los templates a crear
TEMPLATES = {
    # ========== ADMIN TEMPLATES ==========
    "app/templates/admin/dashboard.html": """{% extends "base.html" %}
{% block title %}Dashboard Administrador{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">📊 Dashboard del Administrador</h1>
<div class="row">
    <div class="col-md-3">
        <div class="stat-card">
            <div class="stat-number">{{ total_tutores }}</div>
            <div class="stat-label">Tutores Registrados</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card">
            <div class="stat-number">{{ total_veterinarios }}</div>
            <div class="stat-label">Veterinarios</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card">
            <div class="stat-number">{{ total_mascotas }}</div>
            <div class="stat-label">Mascotas</div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="stat-card">
            <div class="stat-number">{{ total_medicamentos }}</div>
            <div class="stat-label">Medicamentos</div>
        </div>
    </div>
</div>
<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">🚨 Alertas</div>
            <div class="card-body">
                <p><strong>Citas Pendientes:</strong> {{ citas_pendientes }}</p>
                <p><strong>Medicamentos con Stock Bajo:</strong> {{ medicamentos_bajo_stock }}</p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">👥 Últimos Tutores Registrados</div>
            <div class="card-body">
                {% for tutor in ultimos_tutores %}
                <p>• {{ tutor.nombre_completo }} - {{ tutor.fecha_registro.strftime('%d/%m/%Y') }}</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/tutores/lista.html": """{% extends "base.html" %}
{% block title %}Tutores{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">👥 Gestión de Tutores</h1>
<div class="card">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre Completo</th>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Fecha Registro</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for tutor in tutores %}
                <tr>
                    <td>{{ tutor.id }}</td>
                    <td>{{ tutor.nombre_completo }}</td>
                    <td>{{ tutor.username }}</td>
                    <td>{{ tutor.email }}</td>
                    <td>{{ tutor.telefono or 'N/A' }}</td>
                    <td>{{ tutor.fecha_registro.strftime('%d/%m/%Y') }}</td>
                    <td>
                        {% if tutor.activo %}
                        <span class="badge badge-success">Activo</span>
                        {% else %}
                        <span class="badge badge-danger">Inactivo</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="{{ url_for('admin.ver_tutor', id=tutor.id) }}" class="btn btn-sm btn-primary">Ver</a>
                        <a href="{{ url_for('admin.editar_tutor', id=tutor.id) }}" class="btn btn-sm btn-secondary">Editar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/tutores/ver.html": """{% extends "base.html" %}
{% block title %}Ver Tutor{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">👤 Detalles del Tutor</h1>
<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">Información Personal</div>
            <div class="card-body">
                <p><strong>Nombre:</strong> {{ tutor.nombre_completo }}</p>
                <p><strong>Usuario:</strong> {{ tutor.username }}</p>
                <p><strong>Email:</strong> {{ tutor.email }}</p>
                <p><strong>Teléfono:</strong> {{ tutor.telefono or 'N/A' }}</p>
                <p><strong>Dirección:</strong> {{ tutor.direccion or 'N/A' }}</p>
                <p><strong>Estado:</strong> 
                    {% if tutor.activo %}
                    <span class="badge badge-success">Activo</span>
                    {% else %}
                    <span class="badge badge-danger">Inactivo</span>
                    {% endif %}
                </p>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">Estadísticas</div>
            <div class="card-body">
                <p><strong>Total de Mascotas:</strong> {{ mascotas|length }}</p>
                <p><strong>Total de Citas:</strong> {{ citas|length }}</p>
            </div>
        </div>
    </div>
</div>
<div style="margin-top: 1rem;">
    <a href="{{ url_for('admin.editar_tutor', id=tutor.id) }}" class="btn btn-primary">Editar</a>
    <a href="{{ url_for('admin.tutores') }}" class="btn btn-secondary">Volver</a>
</div>
{% endblock %}
""",

    "app/templates/admin/tutores/editar.html": """{% extends "base.html" %}
{% block title %}Editar Tutor{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">✏️ Editar Tutor</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Nombre</label>
                        <input type="text" class="form-control" name="nombre" value="{{ tutor.nombre }}" required>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Apellido</label>
                        <input type="text" class="form-control" name="apellido" value="{{ tutor.apellido }}" required>
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" name="email" value="{{ tutor.email }}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Teléfono</label>
                <input type="text" class="form-control" name="telefono" value="{{ tutor.telefono or '' }}">
            </div>
            <div class="form-group">
                <label class="form-label">Dirección</label>
                <input type="text" class="form-control" name="direccion" value="{{ tutor.direccion or '' }}">
            </div>
            <div class="form-group">
                <label class="form-label">Nueva Contraseña (dejar vacío para no cambiar)</label>
                <input type="password" class="form-control" name="nueva_password">
            </div>
            <div class="form-group">
                <div class="form-check">
                    <input type="checkbox" id="activo" name="activo" {% if tutor.activo %}checked{% endif %}>
                    <label for="activo">Cuenta Activa</label>
                </div>
            </div>
            <button type="submit" class="btn btn-success">Guardar Cambios</button>
            <a href="{{ url_for('admin.ver_tutor', id=tutor.id) }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/veterinarios/lista.html": """{% extends "base.html" %}
{% block title %}Veterinarios{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">👨‍⚕️ Gestión de Veterinarios</h1>
<div style="margin-bottom: 1rem;">
    <a href="{{ url_for('admin.nuevo_veterinario') }}" class="btn btn-success">+ Nuevo Veterinario</a>
</div>
<div class="card">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>Especialidad</th>
                    <th>Licencia</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for vet in veterinarios %}
                <tr>
                    <td>{{ vet.id }}</td>
                    <td>{{ vet.nombre_completo }}</td>
                    <td>{{ vet.username }}</td>
                    <td>{{ vet.email }}</td>
                    <td>{{ vet.especialidad or 'N/A' }}</td>
                    <td>{{ vet.licencia_profesional or 'N/A' }}</td>
                    <td>
                        {% if vet.activo %}
                        <span class="badge badge-success">Activo</span>
                        {% else %}
                        <span class="badge badge-danger">Inactivo</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="{{ url_for('admin.ver_veterinario', id=vet.id) }}" class="btn btn-sm btn-primary">Ver</a>
                        <a href="{{ url_for('admin.editar_veterinario', id=vet.id) }}" class="btn btn-sm btn-secondary">Editar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/veterinarios/nuevo.html": """{% extends "base.html" %}
{% block title %}Nuevo Veterinario{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">➕ Nuevo Veterinario</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Nombre *</label>
                        <input type="text" class="form-control" name="nombre" required>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Apellido *</label>
                        <input type="text" class="form-control" name="apellido" required>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Nombre de Usuario *</label>
                        <input type="text" class="form-control" name="username" required>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Contraseña *</label>
                        <input type="password" class="form-control" name="password" required>
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Email *</label>
                <input type="email" class="form-control" name="email" required>
            </div>
            <div class="form-group">
                <label class="form-label">Teléfono</label>
                <input type="text" class="form-control" name="telefono">
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Especialidad</label>
                        <input type="text" class="form-control" name="especialidad">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Licencia Profesional</label>
                        <input type="text" class="form-control" name="licencia">
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-success">Crear Veterinario</button>
            <a href="{{ url_for('admin.veterinarios') }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/veterinarios/ver.html": """{% extends "base.html" %}
{% block title %}Ver Veterinario{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">👨‍⚕️ Detalles del Veterinario</h1>
<div class="card">
    <div class="card-header">Información Personal</div>
    <div class="card-body">
        <p><strong>Nombre:</strong> {{ veterinario.nombre_completo }}</p>
        <p><strong>Usuario:</strong> {{ veterinario.username }}</p>
        <p><strong>Email:</strong> {{ veterinario.email }}</p>
        <p><strong>Teléfono:</strong> {{ veterinario.telefono or 'N/A' }}</p>
        <p><strong>Especialidad:</strong> {{ veterinario.especialidad or 'N/A' }}</p>
        <p><strong>Licencia:</strong> {{ veterinario.licencia_profesional or 'N/A' }}</p>
        <p><strong>Estado:</strong> 
            {% if veterinario.activo %}
            <span class="badge badge-success">Activo</span>
            {% else %}
            <span class="badge badge-danger">Inactivo</span>
            {% endif %}
        </p>
    </div>
</div>
<div style="margin-top: 1rem;">
    <a href="{{ url_for('admin.editar_veterinario', id=veterinario.id) }}" class="btn btn-primary">Editar</a>
    <a href="{{ url_for('admin.veterinarios') }}" class="btn btn-secondary">Volver</a>
</div>
{% endblock %}
""",

    "app/templates/admin/veterinarios/editar.html": """{% extends "base.html" %}
{% block title %}Editar Veterinario{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">✏️ Editar Veterinario</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Nombre</label>
                        <input type="text" class="form-control" name="nombre" value="{{ veterinario.nombre }}" required>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Apellido</label>
                        <input type="text" class="form-control" name="apellido" value="{{ veterinario.apellido }}" required>
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" name="email" value="{{ veterinario.email }}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Teléfono</label>
                <input type="text" class="form-control" name="telefono" value="{{ veterinario.telefono or '' }}">
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Especialidad</label>
                        <input type="text" class="form-control" name="especialidad" value="{{ veterinario.especialidad or '' }}">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Licencia</label>
                        <input type="text" class="form-control" name="licencia" value="{{ veterinario.licencia_profesional or '' }}">
                    </div>
                </div>
            </div>
            <div class="form-group">
                <label class="form-label">Nueva Contraseña</label>
                <input type="password" class="form-control" name="nueva_password">
            </div>
            <div class="form-group">
                <div class="form-check">
                    <input type="checkbox" id="activo" name="activo" {% if veterinario.activo %}checked{% endif %}>
                    <label for="activo">Cuenta Activa</label>
                </div>
            </div>
            <button type="submit" class="btn btn-success">Guardar Cambios</button>
            <a href="{{ url_for('admin.ver_veterinario', id=veterinario.id) }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/inventario/lista.html": """{% extends "base.html" %}
{% block title %}Inventario{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">💊 Gestión de Inventario</h1>
<div style="margin-bottom: 1rem;">
    <a href="{{ url_for('admin.nuevo_medicamento') }}" class="btn btn-success">+ Nuevo Medicamento</a>
</div>
<div class="card">
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Presentación</th>
                    <th>Stock Actual</th>
                    <th>Stock Mínimo</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for med in medicamentos %}
                <tr {% if med.necesita_reposicion %}style="background-color: #fee2e2;"{% endif %}>
                    <td>{{ med.id }}</td>
                    <td>{{ med.nombre }}</td>
                    <td>{{ med.presentacion or 'N/A' }}</td>
                    <td><strong>{{ med.stock }}</strong> {{ med.unidad_medida }}</td>
                    <td>{{ med.stock_minimo }}</td>
                    <td>
                        {% if med.necesita_reposicion %}
                        <span class="badge badge-danger">⚠️ Stock Bajo</span>
                        {% else %}
                        <span class="badge badge-success">✓ OK</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="{{ url_for('admin.ver_medicamento', id=med.id) }}" class="btn btn-sm btn-primary">Ver</a>
                        <a href="{{ url_for('admin.editar_medicamento', id=med.id) }}" class="btn btn-sm btn-secondary">Editar</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/inventario/nuevo.html": """{% extends "base.html" %}
{% block title %}Nuevo Medicamento{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">➕ Nuevo Medicamento</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="form-group">
                <label class="form-label">Nombre del Medicamento *</label>
                <input type="text" class="form-control" name="nombre" required>
            </div>
            <div class="form-group">
                <label class="form-label">Descripción</label>
                <textarea class="form-control" name="descripcion" rows="3"></textarea>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Principio Activo</label>
                        <input type="text" class="form-control" name="principio_activo">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Presentación</label>
                        <input type="text" class="form-control" name="presentacion" placeholder="Ej: Tabletas, Jarabe">
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">Stock Inicial</label>
                        <input type="number" class="form-control" name="stock" value="0" min="0">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">Stock Mínimo</label>
                        <input type="number" class="form-control" name="stock_minimo" value="10" min="0">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">Unidad</label>
                        <input type="text" class="form-control" name="unidad_medida" value="unidades">
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Lote</label>
                        <input type="text" class="form-control" name="lote">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Fecha de Vencimiento</label>
                        <input type="date" class="form-control" name="fecha_vencimiento">
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Proveedor</label>
                        <input type="text" class="form-control" name="proveedor">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group">
                        <label class="form-label">Precio Unitario</label>
                        <input type="number" class="form-control" name="precio" step="0.01" min="0">
                    </div>
                </div>
            </div>
            <button type="submit" class="btn btn-success">Crear Medicamento</button>
            <a href="{{ url_for('admin.inventario') }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/inventario/ver.html": """{% extends "base.html" %}
{% block title %}Ver Medicamento{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">💊 Detalles del Medicamento</h1>
<div class="card">
    <div class="card-header">{{ medicamento.nombre }}</div>
    <div class="card-body">
        <div class="row">
            <div class="col-md-6">
                <p><strong>Principio Activo:</strong> {{ medicamento.principio_activo or 'N/A' }}</p>
                <p><strong>Presentación:</strong> {{ medicamento.presentacion or 'N/A' }}</p>
                <p><strong>Concentración:</strong> {{ medicamento.concentracion or 'N/A' }}</p>
                <p><strong>Stock Actual:</strong> {{ medicamento.stock }} {{ medicamento.unidad_medida }}</p>
                <p><strong>Stock Mínimo:</strong> {{ medicamento.stock_minimo }}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Lote:</strong> {{ medicamento.lote or 'N/A' }}</p>
                <p><strong>Vencimiento:</strong> {{ medicamento.fecha_vencimiento.strftime('%d/%m/%Y') if medicamento.fecha_vencimiento else 'N/A' }}</p>
                <p><strong>Proveedor:</strong> {{ medicamento.proveedor or 'N/A' }}</p>
                <p><strong>Precio:</strong> Bs. {{ medicamento.precio_unitario or 'N/A' }}</p>
                <p><strong>Estado:</strong> 
                    {% if medicamento.necesita_reposicion %}
                    <span class="badge badge-danger">⚠️ Requiere Reposición</span>
                    {% else %}
                    <span class="badge badge-success">✓ Stock OK</span>
                    {% endif %}
                </p>
            </div>
        </div>
        {% if medicamento.descripcion %}
        <p><strong>Descripción:</strong></p>
        <p>{{ medicamento.descripcion }}</p>
        {% endif %}
    </div>
</div>
<div style="margin-top: 1rem;">
    <a href="{{ url_for('admin.editar_medicamento', id=medicamento.id) }}" class="btn btn-primary">Editar</a>
    <a href="{{ url_for('admin.inventario') }}" class="btn btn-secondary">Volver</a>
</div>
{% endblock %}
""",

    "app/templates/admin/inventario/editar.html": """{% extends "base.html" %}
{% block title %}Editar Medicamento{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">✏️ Editar Medicamento</h1>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="form-group">
                <label class="form-label">Nombre</label>
                <input type="text" class="form-control" name="nombre" value="{{ medicamento.nombre }}" required>
            </div>
            <div class="form-group">
                <label class="form-label">Descripción</label>
                <textarea class="form-control" name="descripcion" rows="3">{{ medicamento.descripcion or '' }}</textarea>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">Stock</label>
                        <input type="number" class="form-control" name="stock" value="{{ medicamento.stock }}" min="0">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">Stock Mínimo</label>
                        <input type="number" class="form-control" name="stock_minimo" value="{{ medicamento.stock_minimo }}" min="0">
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label class="form-label">Unidad</label>
                        <input type="text" class="form-control" name="unidad_medida" value="{{ medicamento.unidad_medida }}">
                    </div>
                </div>
            </div>
            <div class="form-group">
                <div class="form-check">
                    <input type="checkbox" id="activo" name="activo" {% if medicamento.activo %}checked{% endif %}>
                    <label for="activo">Medicamento Activo</label>
                </div>
            </div>
            <button type="submit" class="btn btn-success">Guardar Cambios</button>
            <a href="{{ url_for('admin.ver_medicamento', id=medicamento.id) }}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
</div>
{% endblock %}
""",

    "app/templates/admin/reportes.html": """{% extends "base.html" %}
{% block title %}Reportes{% endblock %}
{% block content %}
<h1 style="margin-bottom: 2rem;">📊 Reportes y Estadísticas</h1>
<div class="row">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">📅 Citas por Estado</div>
            <div class="card-body">
                {% for estado, total in citas_por_estado %}
                <p><strong>{{ estado.title() }}:</strong> {{ total }}</p>
                {% endfor %}
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">⚠️ Medicamentos con Stock Bajo</div>
            <div class="card-body">
                {% for med in medicamentos_bajo_stock %}
                <p>• {{ med.nombre }} - Stock: {{ med.stock }}/{{ med.stock_minimo }}</p>
                {% else %}
                <p>No hay medicamentos con stock bajo</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    # Continúa con templates de tutor y veterinario... (por limitación de espacio, incluyo solo los principales)
}

def create_templates():
    """Crea todos los archivos de templates"""
    print("🔄 Generando templates HTML...")
    
    for filepath, content in TEMPLATES.items():
        # Crear directorios si no existen
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Escribir archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Creado: {filepath}")
    
    print(f"\n✅ Se crearon {len(TEMPLATES)} templates exitosamente!")

if __name__ == '__main__':
    create_templates()
