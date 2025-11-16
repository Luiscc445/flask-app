"""
Módulo de controladores de la aplicación
"""
from app.controllers.auth_controller import auth_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.tutor_controller import tutor_bp
from app.controllers.veterinario_controller import veterinario_bp

__all__ = ['auth_bp', 'admin_bp', 'tutor_bp', 'veterinario_bp']
