# Configuración de SQL Server

Este documento explica cómo configurar la aplicación para usar SQL Server en lugar de SQLite.

## Requisitos Previos

1. **SQL Server instalado** (2016 o superior)
2. **Driver ODBC para SQL Server**
   - Windows: Instalar [ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - Linux: Instalar según [instrucciones de Microsoft](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)
3. **Paquetes Python necesarios**:
   ```bash
   pip install pyodbc
   ```

## Configuración

### Opción 1: Variables de Entorno (Recomendado)

Crea o edita el archivo `.env` en la raíz del proyecto:

```env
# Configuración SQL Server
SQLSERVER_DRIVER=ODBC Driver 17 for SQL Server
SQLSERVER_SERVER=localhost
SQLSERVER_PORT=1433
SQLSERVER_DATABASE=veterinaria
SQLSERVER_USERNAME=sa
SQLSERVER_PASSWORD=TuPasswordSeguro123!

# O para autenticación Windows (comentar las líneas de usuario/password arriba)
# SQLSERVER_TRUSTED=true
```

### Opción 2: Variable DATABASE_URL directa

```env
DATABASE_URL=mssql+pyodbc://user:pass@localhost:1433/veterinaria?driver=ODBC+Driver+17+for+SQL+Server
```

## Ejecutar con SQL Server

### Método 1: Variable de entorno FLASK_CONFIG

```bash
# Windows PowerShell
$env:FLASK_CONFIG = "sqlserver"
python run.py

# Windows CMD
set FLASK_CONFIG=sqlserver
python run.py

# Linux/Mac
export FLASK_CONFIG=sqlserver
python run.py
```

### Método 2: Modificar run.py temporalmente

Edita `run.py` y cambia:
```python
config_name = os.getenv('FLASK_CONFIG', 'sqlserver')  # Cambiar 'default' por 'sqlserver'
```

## Crear la Base de Datos

### Usando SQL Server Management Studio (SSMS)

```sql
CREATE DATABASE veterinaria;
GO

USE veterinaria;
GO

-- La aplicación creará las tablas automáticamente al iniciar
```

### Usando sqlcmd (línea de comandos)

```bash
sqlcmd -S localhost -U sa -P "TuPassword"
> CREATE DATABASE veterinaria;
> GO
> EXIT
```

## Inicialización

Cuando ejecutes `python run.py` por primera vez con SQL Server:

1. La aplicación detectará que las tablas no existen
2. Creará automáticamente todas las tablas necesarias
3. Insertará datos iniciales (admin, servicios, configuraciones)

## Verificar Conexión

La aplicación mostrará en la consola:

```
========================================
Sistema Veterinario v2.0.0
========================================
Configuración: sqlserver
Base de datos: mssql+pyodbc://...
...
```

## Solución de Problemas

### Error: "pyodbc.InterfaceError: ('IM002'..."

**Solución**: El driver ODBC no está instalado o no se encuentra.

Verifica drivers instalados:
```bash
# Windows PowerShell
Get-OdbcDriver

# Linux
odbcinst -q -d
```

### Error: "Login failed for user..."

**Solución**: Verifica las credenciales en `.env`

- Usuario y contraseña correctos
- El usuario tiene permisos para crear bases de datos
- Si usas autenticación Windows, establece `SQLSERVER_TRUSTED=true`

### Error: "TCP Provider: No connection could be made..."

**Solución**: Verifica que SQL Server acepte conexiones remotas:

1. SQL Server Configuration Manager
2. SQL Server Network Configuration → Protocols
3. Habilitar TCP/IP
4. Reiniciar servicio SQL Server

### Error: Driver no encontrado

**Solución**: Cambia el driver en `.env`:

Verifica qué drivers están disponibles:
```python
import pyodbc
print(pyodbc.drivers())
```

Luego usa uno de los drivers listados:
```env
SQLSERVER_DRIVER=SQL Server Native Client 11.0
# o
SQLSERVER_DRIVER=ODBC Driver 18 for SQL Server
```

## Migración de SQLite a SQL Server

Si ya tienes datos en SQLite y quieres migrarlos:

1. **Exportar datos** desde SQLite (script personalizado o herramientas)
2. **Importar a SQL Server** usando BULK INSERT o herramientas
3. **Verificar integridad** de datos

## Rendimiento

Para mejor rendimiento en producción:

```env
# Configurar pool de conexiones
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
```

Agregar a `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 3600
}
```

## Backup y Restauración

### Backup

```sql
BACKUP DATABASE veterinaria
TO DISK = 'C:\Backups\veterinaria.bak'
WITH FORMAT, MEDIANAME = 'veterinaria_backup';
```

### Restauración

```sql
RESTORE DATABASE veterinaria
FROM DISK = 'C:\Backups\veterinaria.bak'
WITH REPLACE;
```

## Soporte

Para más información sobre SQL Server con SQLAlchemy:
- [SQLAlchemy SQL Server Dialects](https://docs.sqlalchemy.org/en/14/dialects/mssql.html)
- [pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)
