#!/bin/bash

# Templates para TUTOR
cat > app/templates/tutor/dashboard.html << 'EOF'
{% extends "base.html" %}
{% block title %}Dashboard Tutor{% endblock %}
{% block content %}
<h1>🏠 Mi Dashboard</h1>
<div class="row">
<div class="col-md-3"><div class="stat-card"><div class="stat-number">{{ total_mascotas }}</div><div class="stat-label">Mis Mascotas</div></div></div>
<div class="col-md-3"><div class="stat-card"><div class="stat-number">{{ total_citas }}</div><div class="stat-label">Total Citas</div></div></div>
<div class="col-md-3"><div class="stat-card"><div class="stat-number">{{ citas_pendientes }}</div><div class="stat-label">Pendientes</div></div></div>
</div>
<div class="card"><div class="card-header">Próximas Citas</div><div class="card-body">
{% for cita in citas_proximas %}
<p>• {{ cita.fecha_hora.strftime('%d/%m/%Y %H:%M') }} - {{ cita.mascota.nombre }}</p>
{% endfor %}
</div></div>
<a href="{{ url_for('tutor.nueva_cita') }}" class="btn btn-success">+ Nueva Cita</a>
<a href="{{ url_for('tutor.nueva_mascota') }}" class="btn btn-primary">+ Registrar Mascota</a>
{% endblock %}
EOF

cat > app/templates/tutor/mascotas.html << 'EOF'
{% extends "base.html" %}
{% block title %}Mis Mascotas{% endblock %}
{% block content %}
<h1>🐾 Mis Mascotas</h1>
<a href="{{ url_for('tutor.nueva_mascota') }}" class="btn btn-success">+ Nueva Mascota</a>
<div class="row" style="margin-top:2rem;">
{% for mascota in mascotas %}
<div class="col-md-4"><div class="card"><div class="card-body">
<h3>{{ mascota.nombre }}</h3>
<p><strong>Especie:</strong> {{ mascota.especie }}</p>
<p><strong>Raza:</strong> {{ mascota.raza or 'N/A' }}</p>
<p><strong>Edad:</strong> {{ mascota.edad or 'N/A' }} años</p>
<a href="{{ url_for('tutor.ver_mascota', id=mascota.id) }}" class="btn btn-sm btn-primary">Ver Detalles</a>
</div></div></div>
{% endfor %}
</div>
{% endblock %}
EOF

cat > app/templates/tutor/nueva_mascota.html << 'EOF'
{% extends "base.html" %}
{% block title %}Nueva Mascota{% endblock %}
{% block content %}
<h1>➕ Registrar Nueva Mascota</h1>
<div class="card"><div class="card-body"><form method="POST">
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Nombre *</label><input type="text" class="form-control" name="nombre" required></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Especie *</label>
<select class="form-control" name="especie" required><option>Perro</option><option>Gato</option><option>Ave</option><option>Otro</option></select></div></div>
</div>
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Raza</label><input type="text" class="form-control" name="raza"></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Fecha Nacimiento</label><input type="date" class="form-control" name="fecha_nacimiento"></div></div>
</div>
<div class="row">
<div class="col-md-4"><div class="form-group"><label class="form-label">Sexo</label><select class="form-control" name="sexo"><option>Macho</option><option>Hembra</option></select></div></div>
<div class="col-md-4"><div class="form-group"><label class="form-label">Color</label><input type="text" class="form-control" name="color"></div></div>
<div class="col-md-4"><div class="form-group"><label class="form-label">Peso (kg)</label><input type="number" class="form-control" name="peso" step="0.1"></div></div>
</div>
<div class="form-group"><div class="form-check"><input type="checkbox" id="esterilizado" name="esterilizado"><label for="esterilizado">Esterilizado</label></div></div>
<button type="submit" class="btn btn-success">Registrar</button>
<a href="{{ url_for('tutor.mascotas') }}" class="btn btn-secondary">Cancelar</a>
</form></div></div>
{% endblock %}
EOF

cat > app/templates/tutor/ver_mascota.html << 'EOF'
{% extends "base.html" %}
{% block title %}{{ mascota.nombre }}{% endblock %}
{% block content %}
<h1>🐕 {{ mascota.nombre }}</h1>
<div class="card"><div class="card-body">
<p><strong>Especie:</strong> {{ mascota.especie }}</p>
<p><strong>Raza:</strong> {{ mascota.raza or 'N/A' }}</p>
<p><strong>Edad:</strong> {{ mascota.edad or 'N/A' }} años</p>
<p><strong>Sexo:</strong> {{ mascota.sexo or 'N/A' }}</p>
<p><strong>Peso:</strong> {{ mascota.peso or 'N/A' }} kg</p>
</div></div>
<a href="{{ url_for('tutor.editar_mascota', id=mascota.id) }}" class="btn btn-primary">Editar</a>
<a href="{{ url_for('tutor.mascotas') }}" class="btn btn-secondary">Volver</a>
{% endblock %}
EOF

cat > app/templates/tutor/editar_mascota.html << 'EOF'
{% extends "base.html" %}
{% block title %}Editar Mascota{% endblock %}
{% block content %}
<h1>✏️ Editar {{ mascota.nombre }}</h1>
<div class="card"><div class="card-body"><form method="POST">
<div class="form-group"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" value="{{ mascota.nombre }}" required></div>
<div class="form-group"><label class="form-label">Especie</label><input type="text" class="form-control" name="especie" value="{{ mascota.especie }}" required></div>
<div class="form-group"><label class="form-label">Peso (kg)</label><input type="number" class="form-control" name="peso" value="{{ mascota.peso or '' }}" step="0.1"></div>
<button type="submit" class="btn btn-success">Guardar</button>
<a href="{{ url_for('tutor.ver_mascota', id=mascota.id) }}" class="btn btn-secondary">Cancelar</a>
</form></div></div>
{% endblock %}
EOF

cat > app/templates/tutor/citas.html << 'EOF'
{% extends "base.html" %}
{% block title %}Mis Citas{% endblock %}
{% block content %}
<h1>📅 Mis Citas Médicas</h1>
<a href="{{ url_for('tutor.nueva_cita') }}" class="btn btn-success">+ Nueva Cita</a>
<div class="card" style="margin-top:2rem;"><div class="card-body"><table class="table">
<thead><tr><th>Fecha/Hora</th><th>Mascota</th><th>Motivo</th><th>Estado</th><th>Acciones</th></tr></thead>
<tbody>
{% for cita in citas %}
<tr><td>{{ cita.fecha_hora.strftime('%d/%m/%Y %H:%M') }}</td><td>{{ cita.mascota.nombre }}</td><td>{{ cita.motivo[:50] }}</td>
<td>
{% if cita.estado == 'pendiente' %}<span class="badge badge-warning">Pendiente</span>
{% elif cita.estado == 'aceptada' %}<span class="badge badge-info">Aceptada</span>
{% elif cita.estado == 'atendida' %}<span class="badge badge-success">Atendida</span>
{% else %}<span class="badge badge-secondary">{{ cita.estado }}</span>
{% endif %}
</td><td><a href="{{ url_for('tutor.ver_cita', id=cita.id) }}" class="btn btn-sm btn-primary">Ver</a></td></tr>
{% endfor %}
</tbody></table></div></div>
{% endblock %}
EOF

cat > app/templates/tutor/nueva_cita.html << 'EOF'
{% extends "base.html" %}
{% block title %}Nueva Cita{% endblock %}
{% block content %}
<h1>➕ Solicitar Nueva Cita</h1>
<div class="card"><div class="card-body"><form method="POST">
<div class="form-group"><label class="form-label">Mascota *</label>
<select class="form-control" name="mascota_id" required>
{% for mascota in mascotas %}
<option value="{{ mascota.id }}">{{ mascota.nombre }} ({{ mascota.especie }})</option>
{% endfor %}
</select></div>
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Fecha *</label><input type="date" class="form-control" name="fecha" required></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Hora *</label><input type="time" class="form-control" name="hora" required></div></div>
</div>
<div class="form-group"><label class="form-label">Motivo de la Consulta *</label>
<textarea class="form-control" name="motivo" rows="4" required></textarea></div>
<button type="submit" class="btn btn-success">Solicitar Cita</button>
<a href="{{ url_for('tutor.citas') }}" class="btn btn-secondary">Cancelar</a>
</form></div></div>
{% endblock %}
EOF

cat > app/templates/tutor/ver_cita.html << 'EOF'
{% extends "base.html" %}
{% block title %}Detalle Cita{% endblock %}
{% block content %}
<h1>📋 Detalle de la Cita</h1>
<div class="card"><div class="card-body">
<p><strong>Mascota:</strong> {{ cita.mascota.nombre }}</p>
<p><strong>Fecha/Hora:</strong> {{ cita.fecha_hora.strftime('%d/%m/%Y %H:%M') }}</p>
<p><strong>Estado:</strong> <span class="badge badge-info">{{ cita.estado }}</span></p>
<p><strong>Motivo:</strong> {{ cita.motivo }}</p>
{% if cita.diagnostico %}
<p><strong>Diagnóstico:</strong> {{ cita.diagnostico }}</p>
<p><strong>Tratamiento:</strong> {{ cita.tratamiento }}</p>
{% endif %}
</div></div>
<a href="{{ url_for('tutor.citas') }}" class="btn btn-secondary">Volver</a>
{% endblock %}
EOF

cat > app/templates/tutor/perfil.html << 'EOF'
{% extends "base.html" %}
{% block title %}Mi Perfil{% endblock %}
{% block content %}
<h1>👤 Mi Perfil</h1>
<div class="card"><div class="card-body"><form method="POST">
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" value="{{ current_user.nombre }}" required></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Apellido</label><input type="text" class="form-control" name="apellido" value="{{ current_user.apellido }}" required></div></div>
</div>
<div class="form-group"><label class="form-label">Email</label><input type="email" class="form-control" name="email" value="{{ current_user.email }}" required></div>
<div class="form-group"><label class="form-label">Teléfono</label><input type="text" class="form-control" name="telefono" value="{{ current_user.telefono or '' }}"></div>
<div class="form-group"><label class="form-label">Dirección</label><input type="text" class="form-control" name="direccion" value="{{ current_user.direccion or '' }}"></div>
<hr><h3>Cambiar Contraseña</h3>
<div class="form-group"><label class="form-label">Contraseña Actual</label><input type="password" class="form-control" name="password_actual"></div>
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Nueva Contraseña</label><input type="password" class="form-control" name="password_nueva"></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Confirmar Nueva</label><input type="password" class="form-control" name="password_confirmar"></div></div>
</div>
<button type="submit" class="btn btn-success">Actualizar Perfil</button>
</form></div></div>
{% endblock %}
EOF

# Templates para VETERINARIO
cat > app/templates/veterinario/dashboard.html << 'EOF'
{% extends "base.html" %}
{% block title %}Dashboard Veterinario{% endblock %}
{% block content %}
<h1>👨‍⚕️ Dashboard del Veterinario</h1>
<div class="row">
<div class="col-md-4"><div class="stat-card"><div class="stat-number">{{ citas_pendientes }}</div><div class="stat-label">Citas Pendientes</div></div></div>
<div class="col-md-4"><div class="stat-card"><div class="stat-number">{{ citas_aceptadas }}</div><div class="stat-label">Mis Citas</div></div></div>
<div class="col-md-4"><div class="stat-card"><div class="stat-number">{{ total_atendidas }}</div><div class="stat-label">Atendidas</div></div></div>
</div>
<div class="card"><div class="card-header">Citas de Hoy</div><div class="card-body">
{% for cita in citas_hoy %}
<p>• {{ cita.fecha_hora.strftime('%H:%M') }} - {{ cita.mascota.nombre }} ({{ cita.tutor.nombre_completo }})</p>
{% else %}
<p>No hay citas para hoy</p>
{% endfor %}
</div></div>
<a href="{{ url_for('veterinario.citas_pendientes') }}" class="btn btn-warning">Ver Pendientes</a>
<a href="{{ url_for('veterinario.mis_citas') }}" class="btn btn-primary">Mis Citas</a>
{% endblock %}
EOF

cat > app/templates/veterinario/citas_pendientes.html << 'EOF'
{% extends "base.html" %}
{% block title %}Citas Pendientes{% endblock %}
{% block content %}
<h1>⏳ Citas Pendientes</h1>
<div class="card"><div class="card-body"><table class="table">
<thead><tr><th>Fecha/Hora</th><th>Mascota</th><th>Tutor</th><th>Motivo</th><th>Acciones</th></tr></thead>
<tbody>
{% for cita in citas %}
<tr><td>{{ cita.fecha_hora.strftime('%d/%m/%Y %H:%M') }}</td><td>{{ cita.mascota.nombre }}</td><td>{{ cita.tutor.nombre_completo }}</td>
<td>{{ cita.motivo[:40] }}</td>
<td>
<form method="POST" action="{{ url_for('veterinario.aceptar_cita', id=cita.id) }}" style="display:inline;">
<button type="submit" class="btn btn-sm btn-success">Aceptar</button>
</form>
<a href="{{ url_for('veterinario.posponer_cita', id=cita.id) }}" class="btn btn-sm btn-warning">Posponer</a>
</td></tr>
{% endfor %}
</tbody></table></div></div>
{% endblock %}
EOF

cat > app/templates/veterinario/mis_citas.html << 'EOF'
{% extends "base.html" %}
{% block title %}Mis Citas{% endblock %}
{% block content %}
<h1>📋 Mis Citas</h1>
<div class="card"><div class="card-body"><table class="table">
<thead><tr><th>Fecha/Hora</th><th>Mascota</th><th>Estado</th><th>Acciones</th></tr></thead>
<tbody>
{% for cita in citas %}
<tr><td>{{ cita.fecha_hora.strftime('%d/%m/%Y %H:%M') }}</td><td>{{ cita.mascota.nombre }}</td>
<td>
{% if cita.estado == 'aceptada' %}<span class="badge badge-info">Aceptada</span>
{% else %}<span class="badge badge-success">Atendida</span>
{% endif %}
</td>
<td>
{% if cita.estado == 'aceptada' %}
<a href="{{ url_for('veterinario.atender_cita', id=cita.id) }}" class="btn btn-sm btn-primary">Atender</a>
{% else %}
<a href="{{ url_for('veterinario.ver_cita', id=cita.id) }}" class="btn btn-sm btn-secondary">Ver</a>
{% endif %}
</td></tr>
{% endfor %}
</tbody></table></div></div>
{% endblock %}
EOF

cat > app/templates/veterinario/atender_cita.html << 'EOF'
{% extends "base.html" %}
{% block title %}Atender Cita{% endblock %}
{% block content %}
<h1>🩺 Atender Cita</h1>
<div class="card"><div class="card-header">Información de la Cita</div><div class="card-body">
<p><strong>Mascota:</strong> {{ cita.mascota.nombre }} ({{ cita.mascota.especie }})</p>
<p><strong>Tutor:</strong> {{ cita.tutor.nombre_completo }}</p>
<p><strong>Motivo:</strong> {{ cita.motivo }}</p>
</div></div>
<div class="card"><div class="card-header">Atención Médica</div><div class="card-body"><form method="POST">
<div class="form-group"><label class="form-label">Diagnóstico *</label><textarea class="form-control" name="diagnostico" rows="3" required></textarea></div>
<div class="form-group"><label class="form-label">Tratamiento *</label><textarea class="form-control" name="tratamiento" rows="3" required></textarea></div>
<div class="form-group"><label class="form-label">Observaciones</label><textarea class="form-control" name="observaciones" rows="2"></textarea></div>
<hr><h3>💊 Recetar Medicamentos</h3>
<div id="medicamentos">
<div class="row"><div class="col-md-4"><label>Medicamento</label><select class="form-control" name="medicamento_id[]">
<option value="">Seleccionar...</option>
{% for med in medicamentos %}
<option value="{{ med.id }}">{{ med.nombre }} (Stock: {{ med.stock }})</option>
{% endfor %}
</select></div>
<div class="col-md-2"><label>Cantidad</label><input type="number" class="form-control" name="cantidad[]" min="0"></div>
<div class="col-md-3"><label>Dosis</label><input type="text" class="form-control" name="dosis[]" placeholder="Ej: 1 cada 8h"></div>
<div class="col-md-3"><label>Duración</label><input type="text" class="form-control" name="duracion[]" placeholder="Ej: 7 días"></div>
</div>
</div>
<button type="button" class="btn btn-sm btn-secondary" onclick="document.getElementById('medicamentos').innerHTML += document.getElementById('medicamentos').innerHTML;">+ Agregar Medicamento</button>
<hr>
<button type="submit" class="btn btn-success">Completar Atención</button>
<a href="{{ url_for('veterinario.mis_citas') }}" class="btn btn-secondary">Cancelar</a>
</form></div></div>
{% endblock %}
EOF

cat > app/templates/veterinario/posponer_cita.html << 'EOF'
{% extends "base.html" %}
{% block title %}Posponer Cita{% endblock %}
{% block content %}
<h1>⏸️ Posponer Cita</h1>
<div class="card"><div class="card-body"><form method="POST">
<div class="form-group"><label class="form-label">Motivo de la Posposición *</label>
<textarea class="form-control" name="motivo" rows="3" required></textarea></div>
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Nueva Fecha Sugerida</label><input type="date" class="form-control" name="nueva_fecha"></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Nueva Hora</label><input type="time" class="form-control" name="nueva_hora"></div></div>
</div>
<button type="submit" class="btn btn-warning">Posponer Cita</button>
<a href="{{ url_for('veterinario.citas_pendientes') }}" class="btn btn-secondary">Cancelar</a>
</form></div></div>
{% endblock %}
EOF

cat > app/templates/veterinario/ver_cita.html << 'EOF'
{% extends "base.html" %}
{% block title %}Detalle Cita{% endblock %}
{% block content %}
<h1>📄 Detalle de la Cita</h1>
<div class="card"><div class="card-body">
<p><strong>Mascota:</strong> {{ cita.mascota.nombre }}</p>
<p><strong>Tutor:</strong> {{ cita.tutor.nombre_completo }}</p>
<p><strong>Fecha:</strong> {{ cita.fecha_hora.strftime('%d/%m/%Y %H:%M') }}</p>
<p><strong>Motivo:</strong> {{ cita.motivo }}</p>
<p><strong>Diagnóstico:</strong> {{ cita.diagnostico }}</p>
<p><strong>Tratamiento:</strong> {{ cita.tratamiento }}</p>
</div></div>
<a href="{{ url_for('veterinario.mis_citas') }}" class="btn btn-secondary">Volver</a>
{% endblock %}
EOF

cat > app/templates/veterinario/perfil.html << 'EOF'
{% extends "base.html" %}
{% block title %}Mi Perfil{% endblock %}
{% block content %}
<h1>👨‍⚕️ Mi Perfil Profesional</h1>
<div class="card"><div class="card-body"><form method="POST">
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Nombre</label><input type="text" class="form-control" name="nombre" value="{{ current_user.nombre }}" required></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Apellido</label><input type="text" class="form-control" name="apellido" value="{{ current_user.apellido }}" required></div></div>
</div>
<div class="form-group"><label class="form-label">Email</label><input type="email" class="form-control" name="email" value="{{ current_user.email }}" required></div>
<div class="form-group"><label class="form-label">Teléfono</label><input type="text" class="form-control" name="telefono" value="{{ current_user.telefono or '' }}"></div>
<div class="row">
<div class="col-md-6"><div class="form-group"><label class="form-label">Especialidad</label><input type="text" class="form-control" name="especialidad" value="{{ current_user.especialidad or '' }}"></div></div>
<div class="col-md-6"><div class="form-group"><label class="form-label">Licencia</label><input type="text" class="form-control" name="licencia_profesional" value="{{ current_user.licencia_profesional or '' }}"></div></div>
</div>
<button type="submit" class="btn btn-success">Actualizar Perfil</button>
</form></div></div>
{% endblock %}
EOF

echo "✅ Todos los templates fueron creados exitosamente!"
