# Clinic Patient Tracker API

Backend de una aplicación sencilla para gestionar pacientes en espera de atención en una clínica.

La API permite:

* Iniciar sesión mediante usuario y contraseña.
* Consultar pacientes con paginación.
* Buscar pacientes por nombre o documento.
* Filtrar pacientes por estado, prioridad y EPS.
* Registrar pacientes.
* Consultar el detalle de un paciente.
* Actualizar información, estado y prioridad.
* Eliminar pacientes.
* Consultar indicadores operativos.
* Importar datos sintéticos desde un archivo ODS.

---

## 1. Tecnologías utilizadas

* Python 3.11 o superior.
* FastAPI.
* SQLAlchemy 2.
* SQLite.
* Pydantic 2.
* PyJWT.
* Argon2 mediante `pwdlib`.
* ODFPy para lectura de archivos ODS.
* Uvicorn.

---

## 2. Arquitectura

El backend está implementado como un **monolito modular**.

Todos los módulos se ejecutan dentro de una única aplicación FastAPI, pero el código está separado por funcionalidad:

```text
app/
├── core/
├── db/
├── importers/
├── modules/
│   ├── auth/
│   ├── dashboard/
│   ├── eps/
│   ├── patients/
│   └── users/
└── shared/
```

Cada módulo puede contener:

```text
router.py       Rutas HTTP
service.py      Reglas de negocio
repository.py   Consultas a la base de datos
schemas.py      Modelos de entrada y respuesta
model.py        Modelo SQLAlchemy
```

El flujo general es:

```text
Cliente
  ↓
Router FastAPI
  ↓
Service
  ↓
Repository
  ↓
SQLite
```

---

## 3. Estructura del backend

```text
backend/
├── app/
│   ├── __init__.py
│   ├── api_router.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exception_handlers.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── init_db.py
│   │   └── seed.py
│   │
│   ├── importers/
│   │   ├── __init__.py
│   │   ├── ods_importer.py
│   │   └── ods_reader.py
│   │
│   ├── modules/
│   │   ├── __init__.py
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   │
│   │   ├── dashboard/
│   │   │   ├── __init__.py
│   │   │   ├── repository.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   │
│   │   ├── eps/
│   │   │   ├── __init__.py
│   │   │   ├── model.py
│   │   │   ├── repository.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   │
│   │   ├── patients/
│   │   │   ├── __init__.py
│   │   │   ├── model.py
│   │   │   ├── repository.py
│   │   │   ├── router.py
│   │   │   ├── schemas.py
│   │   │   └── service.py
│   │   │
│   │   └── users/
│   │       ├── __init__.py
│   │       ├── model.py
│   │       ├── repository.py
│   │       └── schemas.py
│   │
│   └── shared/
│       ├── __init__.py
│       ├── enums.py
│       └── exceptions.py
│
├── data/
│   ├── clinic.db
│   └── raw/
│       └── datos_sinteticos.ods
│
├── scripts/
│   ├── __init__.py
│   └── import_ods.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 4. Requisitos previos

Antes de ejecutar el backend se requiere:

* Python 3.11 o superior.
* `pip`.
* PowerShell, CMD, Bash o una terminal equivalente.
* El archivo de datos sintéticos en formato ODS.

Verificar Python:

```bash
python --version
```

También puede ser necesario utilizar:

```bash
py --version
```

---

## 5. Instalación

### 5.1 Entrar en el backend

```bash
cd clinic-patient-tracker/backend
```

### 5.2 Crear el entorno virtual

En Windows:

```powershell
python -m venv .venv
```

En Linux o macOS:

```bash
python3 -m venv .venv
```

### 5.3 Activar el entorno virtual

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

CMD:

```cmd
.venv\Scripts\activate
```

Linux o macOS:

```bash
source .venv/bin/activate
```

Cuando el entorno esté activo, la terminal mostrará algo similar a:

```text
(.venv)
```

### 5.4 Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 6. Configuración de variables de entorno

Crear el archivo `.env` tomando como base `.env.example`.

En PowerShell:

```powershell
Copy-Item .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Contenido esperado:

```env
APP_NAME=Clinic Patient Tracker API
APP_VERSION=0.1.0
APP_ENVIRONMENT=development
DEBUG=true

API_V1_PREFIX=/api/v1

DATABASE_URL=sqlite:///./data/clinic.db

JWT_SECRET_KEY=change-this-development-secret-key-before-production-2026
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

CORS_ORIGINS=["http://localhost:5173"]

SEED_FILE=data/raw/datos_sinteticos.ods
```

### Generar una clave JWT

Para generar una clave segura:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiar el resultado en `.env`:

```env
JWT_SECRET_KEY=CLAVE_GENERADA
```

El archivo `.env` no debe subirse al repositorio.

---

## 7. Archivo de datos sintéticos

El archivo suministrado debe copiarse en:

```text
backend/data/raw/datos_sinteticos.ods
```

El nombre original puede ser:

```text
Datos_Sinteticos_Prueba_Full_Stack_Junior_2026(2).ods
```

Se recomienda renombrarlo como:

```text
datos_sinteticos.ods
```

El archivo contiene las hojas:

```text
Pacientes
Catalogos
Diccionario
Usuarios_Login
LEEME
```

La importación utiliza principalmente:

* `Pacientes`.
* `Catalogos`.
* `Usuarios_Login`.

---

## 8. Modelo de datos

### 8.1 Usuarios

Tabla:

```text
users
```

Campos principales:

```text
id
username
full_name
password_hash
role
is_active
created_at
```

Reglas:

* `username` es único.
* La contraseña nunca se almacena en texto plano.
* El hash se genera mediante Argon2.
* Solo los usuarios activos pueden iniciar sesión.

Roles permitidos:

```text
ADMIN
OPERADOR
```

### 8.2 EPS

Tabla:

```text
eps
```

Campos:

```text
id
code
name
is_active
```

Reglas:

* El código de EPS es único.
* El nombre de EPS es único.
* Un paciente debe estar relacionado con una EPS existente.

### 8.3 Pacientes

Tabla:

```text
patients
```

Campos:

```text
id
document_type
document_number
full_name
birth_date
gender
phone
email
city
eps_id
priority
status
created_at
updated_at
```

Reglas principales:

* El documento es obligatorio y único.
* La fecha de nacimiento no puede ser futura.
* La EPS debe existir.
* El estado debe pertenecer al catálogo permitido.
* La prioridad debe pertenecer al catálogo permitido.
* `email` y `city` son opcionales.
* `eps_id` es una llave foránea hacia `eps`.

---

## 9. Catálogos controlados

### Tipos de documento

```text
CC
TI
CE
PA
```

### Géneros

```text
Femenino
Masculino
Otro
Prefiere no informar
```

### Prioridades

```text
Alta
Media
Baja
```

### Estados

```text
Pendiente
En atención
Atendido
```

Los valores deben enviarse exactamente como aparecen, incluyendo espacios y tildes.

---

## 10. Crear las tablas e importar los datos

La aplicación crea las tablas cuando FastAPI inicia. Sin embargo, la carga del ODS debe ejecutarse mediante el script de importación.

Desde `backend`:

```bash
python -m scripts.import_ods
```

Resultado esperado durante la primera ejecución:

```json
{
  "eps": {
    "created": 10,
    "updated": 0
  },
  "users": {
    "created": 2,
    "updated": 0
  },
  "patients": {
    "created": 1000,
    "updated": 0
  }
}
```

La importación es idempotente. Puede ejecutarse nuevamente sin duplicar registros:

```bash
python -m scripts.import_ods
```

Resultado esperado en la segunda ejecución:

```json
{
  "eps": {
    "created": 0,
    "updated": 0
  },
  "users": {
    "created": 0,
    "updated": 0
  },
  "patients": {
    "created": 0,
    "updated": 0
  }
}
```

También puede indicarse manualmente otra ruta:

```bash
python -m scripts.import_ods --file "C:\ruta\archivo.ods"
```

---

## 11. Ejecutar el servidor

Desde la carpeta `backend`:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Documentación Swagger:

```text
http://127.0.0.1:8000/docs
```

Documentación ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Esquema OpenAPI:

```text
http://127.0.0.1:8000/api/v1/openapi.json
```

---

## 12. Credenciales de demostración

### Usuario administrador

```text
Usuario: admin.demo
Contraseña: Demo2026*
Rol: ADMIN
```

### Usuario operador

```text
Usuario: operador.demo
Contraseña: Demo2026*
Rol: OPERADOR
```

Estas credenciales provienen del archivo de datos sintéticos.

Las contraseñas se importan a SQLite como hashes Argon2.

---

## 13. Autenticación

La API utiliza tokens JWT.

### Flujo

```text
Usuario y contraseña
        ↓
POST /api/v1/auth/login
        ↓
Token JWT
        ↓
Authorization: Bearer TOKEN
        ↓
Acceso a rutas protegidas
```

La duración predeterminada del token es de 60 minutos.

Se puede modificar en `.env`:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 14. Rutas disponibles

### Sistema

```http
GET /api/v1/health
```

### Autenticación

```http
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

### EPS

```http
GET /api/v1/eps
```

### Pacientes

```http
GET    /api/v1/patients
GET    /api/v1/patients/{patient_id}
POST   /api/v1/patients
PATCH  /api/v1/patients/{patient_id}
DELETE /api/v1/patients/{patient_id}
```

### Dashboard

```http
GET /api/v1/dashboard
```

Excepto el endpoint de login y los endpoints generales del sistema, las rutas requieren autenticación.

---

## 15. Inicio de sesión

Endpoint:

```http
POST /api/v1/auth/login
```

El login utiliza `application/x-www-form-urlencoded`.

Campos:

```text
username
password
```

Ejemplo con PowerShell:

```powershell
$login = Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/auth/login" `
  -ContentType "application/x-www-form-urlencoded" `
  -Body @{
    username = "admin.demo"
    password = "Demo2026*"
  }
```

Respuesta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin.demo",
    "full_name": "Administrador Demo",
    "role": "ADMIN",
    "is_active": true,
    "created_at": "2026-01-01T08:00:00"
  }
}
```

Guardar el token:

```powershell
$token = $login.access_token
```

---

## 16. Consultar el usuario autenticado

Endpoint:

```http
GET /api/v1/auth/me
```

Ejemplo:

```powershell
Invoke-RestMethod `
  -Method Get `
  -Uri "http://127.0.0.1:8000/api/v1/auth/me" `
  -Headers @{
    Authorization = "Bearer $token"
  }
```

Respuesta:

```json
{
  "id": 1,
  "username": "admin.demo",
  "full_name": "Administrador Demo",
  "role": "ADMIN",
  "is_active": true,
  "created_at": "2026-01-01T08:00:00"
}
```

---

## 17. Consultar EPS

Endpoint:

```http
GET /api/v1/eps
```

Ejemplo:

```powershell
Invoke-RestMethod `
  -Method Get `
  -Uri "http://127.0.0.1:8000/api/v1/eps" `
  -Headers @{
    Authorization = "Bearer $token"
  }
```

Respuesta:

```json
[
  {
    "id": 7,
    "code": "EPS007",
    "name": "Compensar EPS",
    "is_active": true
  },
  {
    "id": 5,
    "code": "EPS005",
    "name": "Coosalud",
    "is_active": true
  }
]
```

---

## 18. Consultar pacientes

Endpoint:

```http
GET /api/v1/patients
```

Parámetros disponibles:

| Parámetro   | Descripción          | Valor predeterminado |
| ----------- | -------------------- | -------------------: |
| `page`      | Página solicitada    |                  `1` |
| `page_size` | Registros por página |                 `20` |
| `search`    | Nombre o documento   |                Vacío |
| `status`    | Estado del paciente  |                Vacío |
| `priority`  | Prioridad            |                Vacío |
| `eps_id`    | Identificador de EPS |                Vacío |

Ejemplo:

```text
GET /api/v1/patients?page=1&page_size=20
```

Respuesta:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 1000,
  "total_pages": 50,
  "has_previous": false,
  "has_next": true
}
```

### Buscar por nombre o documento

```text
GET /api/v1/patients?search=María
```

```text
GET /api/v1/patients?search=1000000123
```

### Filtrar por estado

```text
GET /api/v1/patients?status=Pendiente
```

```text
GET /api/v1/patients?status=En%20atenci%C3%B3n
```

```text
GET /api/v1/patients?status=Atendido
```

### Filtrar por prioridad

```text
GET /api/v1/patients?priority=Alta
```

### Filtrar por EPS

```text
GET /api/v1/patients?eps_id=1
```

### Combinar filtros

```text
GET /api/v1/patients?page=1&page_size=20&status=Pendiente&priority=Alta&eps_id=1
```

---

## 19. Consultar un paciente

Endpoint:

```http
GET /api/v1/patients/{patient_id}
```

Ejemplo:

```text
GET /api/v1/patients/1
```

Respuesta:

```json
{
  "id": 1,
  "document_type": "CC",
  "document_number": "1000000001",
  "full_name": "Paciente de ejemplo",
  "birth_date": "1990-05-20",
  "gender": "Femenino",
  "phone": "3001234567",
  "email": "paciente@example.com",
  "city": "Cali",
  "priority": "Alta",
  "status": "Pendiente",
  "created_at": "2026-01-10T08:00:00",
  "updated_at": "2026-01-10T08:00:00",
  "eps": {
    "id": 1,
    "code": "EPS001",
    "name": "SURA EPS",
    "is_active": true
  }
}
```

---

## 20. Crear un paciente

Endpoint:

```http
POST /api/v1/patients
```

Ejemplo de cuerpo:

```json
{
  "document_type": "CC",
  "document_number": "1234567890",
  "full_name": "Laura Marcela Gómez",
  "birth_date": "1995-08-17",
  "gender": "Femenino",
  "phone": "3005551122",
  "email": "laura.gomez@example.com",
  "city": "Cali",
  "eps_id": 1,
  "priority": "Alta",
  "status": "Pendiente"
}
```

Respuesta:

```text
201 Created
```

El documento no puede pertenecer a otro paciente.

---

## 21. Actualizar un paciente

Endpoint:

```http
PATCH /api/v1/patients/{patient_id}
```

Solo deben enviarse los campos que se desean modificar.

### Cambiar estado

```json
{
  "status": "En atención"
}
```

### Cambiar prioridad

```json
{
  "priority": "Alta"
}
```

### Cambiar estado y prioridad

```json
{
  "status": "Atendido",
  "priority": "Media"
}
```

### Actualizar datos de contacto

```json
{
  "phone": "3155556677",
  "email": "nuevo.correo@example.com",
  "city": "Palmira"
}
```

### Eliminar un valor opcional

```json
{
  "email": null
}
```

No puede enviarse un cuerpo vacío.

---

## 22. Eliminar un paciente

Endpoint:

```http
DELETE /api/v1/patients/{patient_id}
```

Respuesta exitosa:

```text
204 No Content
```

La interfaz web debe solicitar confirmación antes de llamar este endpoint.

---

## 23. Dashboard

Endpoint:

```http
GET /api/v1/dashboard
```

Respuesta esperada con los 1.000 registros iniciales:

```json
{
  "total_patients": 1000,
  "pending_patients": 378,
  "in_progress_patients": 182,
  "attended_patients": 440,
  "high_priority_patients": 185
}
```

Los indicadores se calculan directamente desde la tabla `patients`.

No existe una tabla independiente para el dashboard.

---

## 24. Validaciones de pacientes

### Documento

* Obligatorio.
* Único.
* Entre 4 y 20 caracteres.
* Puede contener letras, números, puntos y guiones.

### Nombre completo

* Obligatorio.
* Entre 3 y 150 caracteres.

### Fecha de nacimiento

* Obligatoria.
* Debe ser una fecha válida.
* No puede ser futura.

### Género

Debe pertenecer al catálogo permitido.

### Teléfono

* Obligatorio.
* Debe contener entre 7 y 15 dígitos.
* Puede incluir espacios, guiones, paréntesis y `+`.

### Correo

* Opcional.
* Si se envía, debe tener un formato válido.

### Ciudad

* Opcional.
* Entre 2 y 80 caracteres.

### EPS

* Obligatoria.
* Debe existir.
* Debe encontrarse activa.

### Prioridad

Debe ser:

```text
Alta
Media
Baja
```

### Estado

Debe ser:

```text
Pendiente
En atención
Atendido
```

---

## 25. Códigos de respuesta

| Código | Significado                       |
| -----: | --------------------------------- |
|  `200` | Operación exitosa                 |
|  `201` | Recurso creado                    |
|  `204` | Recurso eliminado                 |
|  `400` | Regla de negocio incumplida       |
|  `401` | Credenciales o token inválidos    |
|  `404` | Recurso no encontrado             |
|  `409` | Conflicto o información duplicada |
|  `422` | Datos de entrada inválidos        |
|  `500` | Error interno no controlado       |

Ejemplo de documento duplicado:

```json
{
  "detail": "Ya existe un paciente con ese número de documento."
}
```

Ejemplo de paciente inexistente:

```json
{
  "detail": "El paciente solicitado no existe."
}
```

---

## 26. Probar la API con Swagger

Abrir:

```text
http://127.0.0.1:8000/docs
```

Presionar el botón **Authorize**.

Ingresar:

```text
Username: admin.demo
Password: Demo2026*
```

Dejar vacíos:

```text
client_id
client_secret
```

Después de autorizarse, Swagger enviará automáticamente el token en las rutas protegidas.

---

## 27. Reiniciar la base de datos

Para comenzar nuevamente desde cero:

1. Detener el servidor.
2. Eliminar:

```text
backend/data/clinic.db
```

En PowerShell:

```powershell
Remove-Item data\clinic.db
```

3. Ejecutar nuevamente la importación:

```bash
python -m scripts.import_ods
```

4. Iniciar FastAPI:

```bash
uvicorn app.main:app --reload
```

No deben eliminarse los archivos `.ods` de `data/raw`.

---

## 28. Integración con el frontend

El frontend React + Vite debe utilizar como URL base:

```text
http://127.0.0.1:8000/api/v1
```

Variable sugerida en el frontend:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Origen permitido en el backend:

```env
CORS_ORIGINS=["http://localhost:5173"]
```

Después del login, el frontend debe guardar temporalmente el token y enviarlo así:

```http
Authorization: Bearer TOKEN
```

---

## 29. Flujo recomendado para ejecutar el proyecto

Primera ejecución:

```bash
cd backend
python -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar:

```bash
pip install -r requirements.txt
```

Crear `.env`:

```powershell
Copy-Item .env.example .env
```

Importar datos:

```bash
python -m scripts.import_ods
```

Ejecutar:

```bash
uvicorn app.main:app --reload
```

Abrir:

```text
http://127.0.0.1:8000/docs
```

Ejecuciones posteriores:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

---

## 30. Consideraciones técnicas

* SQLite es suficiente para el alcance actual y los 1.000 registros suministrados.
* La arquitectura permite sustituir SQLite por PostgreSQL posteriormente.
* La aplicación utiliza sesiones síncronas de SQLAlchemy para mantener una implementación sencilla.
* Los datos clínicos suministrados son sintéticos.
* No deben incorporarse datos reales ni información clínica sensible.
* Las contraseñas se almacenan mediante hash.
* La clave JWT se configura mediante variables de entorno.
* Los endpoints de negocio están protegidos.
* La importación evita duplicar pacientes, usuarios y EPS.
* El dashboard se calcula directamente desde los datos actuales.

---

## 31. Alcance actual

El backend cubre las historias principales de:

* Autenticación.
* Consulta y búsqueda de pacientes.
* Registro de pacientes.
* Actualización de pacientes.
* Cambio de estado.
* Cambio de prioridad.
* Eliminación.
* Catálogo de EPS.
* Indicadores operativos.
* Documentación automática de la API.
* Importación de datos sintéticos.

---

## 32. Próximo paso

El siguiente componente del proyecto es el frontend con React y Vite, que consumirá esta API para implementar:

* Pantalla de inicio de sesión.
* Dashboard.
* Tabla paginada de pacientes.
* Búsqueda y filtros.
* Formulario de creación y edición.
* Confirmación de eliminación.
* Mensajes de éxito y error.
