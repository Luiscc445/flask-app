# Script PowerShell para actualizar el sistema veterinario
# Este script reemplazará todos los archivos viejos con el sistema mejorado

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ACTUALIZACION SISTEMA VETERINARIO v2.0.0" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
$currentPath = Get-Location
Write-Host "Directorio actual: $currentPath" -ForegroundColor Yellow

# Hacer backup de los archivos actuales
$backupFolder = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "`nCreando backup en: $backupFolder" -ForegroundColor Yellow

if (Test-Path "app") {
    New-Item -ItemType Directory -Name $backupFolder -Force | Out-Null
    Copy-Item -Path "app", "*.py", "*.txt", "*.md" -Destination $backupFolder -Recurse -Force
    Write-Host "✓ Backup creado exitosamente" -ForegroundColor Green
}

Write-Host "`n=== INICIANDO ACTUALIZACIÓN ===" -ForegroundColor Cyan

# Eliminar archivos antiguos (excepto el backup)
Write-Host "`nEliminando archivos antiguos..." -ForegroundColor Yellow
if (Test-Path "app") { Remove-Item -Path "app" -Recurse -Force }
if (Test-Path "config.py") { Remove-Item -Path "config.py" -Force }
if (Test-Path "requirements.txt") { Remove-Item -Path "requirements.txt" -Force }
if (Test-Path "run.py") { Remove-Item -Path "run.py" -Force }

# Crear estructura de directorios
Write-Host "`nCreando nueva estructura de directorios..." -ForegroundColor Yellow
$directories = @(
    "app",
    "app\models",
    "app\controllers", 
    "app\templates",
    "app\templates\admin",
    "app\templates\admin\tutores",
    "app\templates\admin\mascotas",
    "app\templates\admin\veterinarios",
    "app\templates\admin\inventario",
    "app\templates\admin\citas",
    "app\templates\auth",
    "app\templates\veterinario",
    "app\templates\tutor",
    "app\templates\errors",
    "app\static",
    "app\static\css",
    "app\static\js",
    "app\static\images",
    "uploads",
    "uploads\profiles",
    "uploads\pets",
    "uploads\documents"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}
Write-Host "✓ Estructura de directorios creada" -ForegroundColor Green

# Descargar el sistema mejorado
Write-Host "`nDescargando sistema mejorado..." -ForegroundColor Yellow
Write-Host "Por favor, extrae el archivo 'sistema_veterinario_mejorado.zip' en este directorio" -ForegroundColor Magenta

# Esperar confirmación del usuario
Write-Host "`nPresiona ENTER cuando hayas extraído los archivos..." -ForegroundColor Yellow
Read-Host

# Verificar que los archivos se hayan extraído
if (Test-Path "veterinaria_mejorado") {
    Write-Host "`nCopiando archivos del sistema mejorado..." -ForegroundColor Yellow
    
    # Copiar todos los archivos del sistema mejorado
    Copy-Item -Path "veterinaria_mejorado\*" -Destination "." -Recurse -Force
    
    # Limpiar directorio temporal
    Remove-Item -Path "veterinaria_mejorado" -Recurse -Force
    
    Write-Host "✓ Archivos copiados exitosamente" -ForegroundColor Green
} else {
    Write-Host "ERROR: No se encontró el directorio 'veterinaria_mejorado'" -ForegroundColor Red
    Write-Host "Asegúrate de extraer el archivo ZIP correctamente" -ForegroundColor Red
    exit 1
}

Write-Host "`n=== INSTALANDO DEPENDENCIAS ===" -ForegroundColor Cyan

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "`nCreando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "`nActivando entorno virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Actualizar pip
Write-Host "`nActualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Instalar dependencias
Write-Host "`nInstalando dependencias del sistema..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n=== CONFIGURANDO BASE DE DATOS ===" -ForegroundColor Cyan

# Crear archivo .env si no existe
if (-not (Test-Path ".env")) {
    Write-Host "`nCreando archivo de configuración .env..." -ForegroundColor Yellow
    @"
# Configuración del Sistema Veterinario
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production-$(Get-Random)
DATABASE_URL=sqlite:///veterinaria.db

# Configuración de correo (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@veterinaria.com
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ Archivo .env creado" -ForegroundColor Green
}

# Inicializar base de datos
Write-Host "`nInicializando base de datos..." -ForegroundColor Yellow
python -c "from app import create_app, db, init_database; app = create_app(); app.app_context().push(); db.create_all(); init_database()"
Write-Host "✓ Base de datos inicializada" -ForegroundColor Green

Write-Host "`n================================================" -ForegroundColor Green
Write-Host "  ✓ ACTUALIZACIÓN COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "CREDENCIALES DE ACCESO:" -ForegroundColor Cyan
Write-Host "  Usuario: admin" -ForegroundColor White
Write-Host "  Contraseña: admin123" -ForegroundColor White
Write-Host ""
Write-Host "PARA EJECUTAR EL SISTEMA:" -ForegroundColor Cyan
Write-Host "  1. Activar entorno virtual: .\venv\Scripts\Activate" -ForegroundColor White
Write-Host "  2. Ejecutar: python run.py" -ForegroundColor White
Write-Host "  3. Abrir navegador en: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "BACKUP GUARDADO EN: $backupFolder" -ForegroundColor Yellow
Write-Host ""
Write-Host "¿Deseas ejecutar el sistema ahora? (S/N): " -ForegroundColor Green -NoNewline
$respuesta = Read-Host

if ($respuesta -eq 'S' -or $respuesta -eq 's') {
    Write-Host "`nIniciando sistema..." -ForegroundColor Green
    python run.py
}
