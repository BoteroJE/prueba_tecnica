# Clinic Patient Tracker

Aplicación full stack para administrar pacientes en espera de atención en una clínica.

El sistema permite identificar pacientes prioritarios, consultar información básica, actualizar el estado de atención y visualizar indicadores operativos.

El proyecto fue desarrollado como un **monolito modular**, con frontend y backend separados dentro de un mismo repositorio. **Por favor, se debe leer y analizar cada README (Frontend y backend) para la correcta instalacion y uso**

---

## 1. Funcionalidades principales

* Inicio de sesión con usuario y contraseña.
* Autenticación mediante JWT.
* Dashboard de indicadores.
* Consulta de pacientes.
* Búsqueda por nombre o documento.
* Filtros por estado, prioridad y EPS.
* Registro de pacientes.
* Edición de pacientes.
* Cambio de estado de atención.
* Cambio de prioridad.
* Eliminación con confirmación.
* Paginación.
* Catálogo de EPS.
* Importación de 1.000 pacientes sintéticos desde un archivo ODS.
* Documentación automática de la API.

---

## 2. Historias de usuario cubiertas

### Inicio de sesión

Como usuario del sistema, puedo iniciar sesión para acceder al módulo de seguimiento.

### Consulta y búsqueda

Como personal asistencial, puedo consultar y buscar pacientes para encontrar rápidamente un registro.

### Registro y actualización

Como personal asistencial, puedo registrar y actualizar pacientes para mantener la lista vigente.

### Estado y prioridad

Como personal asistencial, puedo cambiar el estado y la prioridad de un paciente para reflejar su situación actual.

### Indicadores

Como responsable del servicio, puedo consultar indicadores simples sobre el volumen y estado general de la atención.

---

## 3. Tecnologías

### Backend

* Python.
* FastAPI.
* SQLAlchemy 2.
* SQLite.
* Pydantic 2.
* PyJWT.
* Argon2 mediante `pwdlib`.
* ODFPy.
* Uvicorn.

### Frontend

* React.
* Vite.
* React Router.
* JavaScript.
* Fetch API.
* Context API.
* CSS.

---

## 4. Estructura general

```text
clinic-patient-tracker/
├── backend/
│   ├── app/
│   ├── data/
│   ├── scripts/
│   ├── tests/
│   ├── .env.example
│   ├── README.md
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── .env.example
│   ├── README.md
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 5. Arquitectura

El repositorio contiene dos aplicaciones:

```text
Frontend React + Vite
        ↓
API REST con JWT
        ↓
Backend FastAPI
        ↓
SQLAlchemy
        ↓
SQLite
```

El backend está organizado como un monolito modular:

```text
auth
users
eps
patients
dashboard
```

El frontend también está organizado por funcionalidades:

```text
auth
dashboard
patients
```

No se utilizan microservicios. Todo el backend se ejecuta dentro de una única aplicación FastAPI.

---

## 6. Modelo de datos

### Usuarios

Información utilizada para autenticación:

```text
id
username
full_name
password_hash
role
is_active
created_at
```

### EPS

Catálogo de entidades prestadoras de salud:

```text
id
code
name
is_active
```

### Pacientes

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

El documento del paciente es único.

La EPS se maneja mediante una llave foránea para evitar duplicar el nombre y código en cada paciente.

---

## 7. Datos sintéticos

El proyecto utiliza el archivo:

```text
backend/data/raw/datos_sinteticos.ods
```

El archivo suministrado contiene:

* 1.000 pacientes sintéticos.
* 10 EPS.
* Catálogos controlados.
* Diccionario de datos.
* 2 usuarios de demostración.

Los datos son ficticios y no deben reemplazarse por información real de pacientes.

---

## 8. Requisitos previos

### Backend

* Python 3.11 o superior.
* pip.

### Frontend

* Node.js 20.19 o superior.
* npm.

Verificar:

```bash
python --version
node --version
npm --version
```

---

# Ejecución del proyecto

## 9. Configurar el backend

Entrar a la carpeta:

```bash
cd backend
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activar en CMD:

```cmd
.venv\Scripts\activate
```

Activar en Linux o macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear `.env`:

```powershell
Copy-Item .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Contenido mínimo:

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

Generar una clave JWT:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiarla en:

```env
JWT_SECRET_KEY=CLAVE_GENERADA
```

---

## 10. Importar los datos

Confirmar que el ODS se encuentre en:

```text
backend/data/raw/datos_sinteticos.ods
```

Ejecutar:

```bash
python -m scripts.import_ods
```

Primera ejecución esperada:

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

La importación es idempotente. Puede ejecutarse nuevamente sin duplicar registros.

---

## 11. Ejecutar el backend

Desde `backend`:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## 12. Configurar el frontend

En una terminal diferente, desde la raíz:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Crear `.env`:

```powershell
Copy-Item .env.example .env
```

En Linux o macOS:

```bash
cp .env.example .env
```

Contenido:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

---

## 13. Ejecutar el frontend

```bash
npm run dev
```

Abrir:

```text
http://localhost:5173
```

El backend y el frontend deben mantenerse ejecutándose al mismo tiempo.

---

## 14. Credenciales de demostración

### Administrador

```text
Usuario: admin.demo
Contraseña: Demo2026*
Rol: ADMIN
```

### Operador

```text
Usuario: operador.demo
Contraseña: Demo2026*
Rol: OPERADOR
```

---

## 15. Flujo de ejecución completo

### Terminal 1 — Backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m scripts.import_ods
uvicorn app.main:app --reload
```

### Terminal 2 — Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Navegador

```text
http://localhost:5173
```

---

## 16. Endpoints de la API

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

---

## 17. Parámetros del listado de pacientes

```http
GET /api/v1/patients
```

| Parámetro   | Descripción          | Predeterminado |
| ----------- | -------------------- | -------------: |
| `page`      | Página solicitada    |            `1` |
| `page_size` | Registros por página |           `20` |
| `search`    | Nombre o documento   |          Vacío |
| `status`    | Estado               |          Vacío |
| `priority`  | Prioridad            |          Vacío |
| `eps_id`    | EPS                  |          Vacío |

Ejemplo:

```text
/api/v1/patients?page=1&page_size=20&status=Pendiente&priority=Alta
```

---

## 18. Dashboard

El dashboard muestra:

```text
Pacientes registrados
Pacientes pendientes
Pacientes en atención
Pacientes atendidos
Pacientes con prioridad alta
```

Los indicadores se calculan directamente desde la tabla de pacientes.

No existe una tabla separada para almacenar estadísticas.

---

## 19. Catálogos controlados

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

Los valores deben conservar espacios y tildes.

---

## 20. Validaciones principales

### Pacientes

* Documento obligatorio.
* Documento único.
* Fecha de nacimiento no futura.
* Nombre obligatorio.
* Teléfono válido.
* EPS existente.
* Prioridad controlada.
* Estado controlado.
* Correo válido cuando se proporciona.

### Usuarios

* Nombre de usuario único.
* Contraseña almacenada como hash.
* Solo usuarios activos pueden iniciar sesión.

---

## 21. Seguridad

* Las contraseñas se almacenan mediante Argon2.
* La API utiliza JWT.
* La clave JWT se configura desde `.env`.
* Los endpoints de pacientes, EPS y dashboard están protegidos.
* El frontend no contiene la clave JWT.
* El token se envía mediante `Authorization: Bearer`.
* El token se almacena temporalmente en `sessionStorage`.
* Los datos suministrados son sintéticos.

---

## 22. Códigos de respuesta relevantes

| Código | Significado                    |
| -----: | ------------------------------ |
|  `200` | Operación exitosa              |
|  `201` | Registro creado                |
|  `204` | Registro eliminado             |
|  `400` | Regla de negocio incumplida    |
|  `401` | Credenciales o token inválidos |
|  `404` | Recurso no encontrado          |
|  `409` | Conflicto o duplicidad         |
|  `422` | Datos de entrada inválidos     |
|  `500` | Error interno                  |

---

## 23. Reiniciar la base de datos

Detener FastAPI.

Eliminar:

```text
backend/data/clinic.db
```

En PowerShell:

```powershell
Remove-Item backend\data\clinic.db
```

Volver al backend:

```bash
cd backend
```

Ejecutar:

```bash
python -m scripts.import_ods
uvicorn app.main:app --reload
```

---

## 24. Compilar el frontend

Desde `frontend`:

```bash
npm run build
```

La compilación se genera en:

```text
frontend/dist/
```

Revisar localmente:

```bash
npm run preview
```

---

## 25. Solución de problemas

### El frontend no puede conectarse al backend

Confirmar que FastAPI esté activo:

```text
http://127.0.0.1:8000/docs
```

Confirmar en `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

### Error CORS

Confirmar en `backend/.env`:

```env
CORS_ORIGINS=["http://localhost:5173"]
```

Reiniciar FastAPI.

### El login funciona, pero no aparecen datos

Abrir:

```text
F12 → Network
```

Verificar solicitudes a:

```text
/api/v1/dashboard
/api/v1/patients
/api/v1/eps
```

### Respuesta `401`

El token pudo expirar.

Cerrar sesión e ingresar nuevamente.

### La base de datos está vacía

Ejecutar:

```bash
python -m scripts.import_ods
```

### El ODS no se encuentra

Confirmar la ubicación:

```text
backend/data/raw/datos_sinteticos.ods
```

Y la variable:

```env
SEED_FILE=data/raw/datos_sinteticos.ods
```

---

## 26. Decisiones técnicas

### Monolito modular

Se escogió una arquitectura modular, pero sin separar el sistema en microservicios, debido al alcance reducido de la prueba.

### SQLite

SQLite es suficiente para:

* 1.000 registros.
* Ejecución local.
* Instalación sencilla.
* Entrega técnica rápida.

La capa de SQLAlchemy permitiría migrar posteriormente a PostgreSQL.

### Autenticación JWT

JWT permite mantener el backend sin estado de sesión y simplifica la integración con React.

### Session Storage

Se utilizó `sessionStorage` para evitar conservar indefinidamente la sesión en el navegador.

### Sin Redux

El estado compartido es reducido y se limita principalmente a la autenticación. Context API es suficiente.

### Sin Axios

La Fetch API cubre las solicitudes necesarias y evita agregar otra dependencia.

### Sin librería de componentes

El diseño se implementó con CSS para reducir dependencias y demostrar construcción directa de la interfaz.

---

## 27. Alcance entregado

### Backend

* API REST.
* Autenticación.
* JWT.
* Modelos de usuarios, EPS y pacientes.
* Importación del ODS.
* CRUD de pacientes.
* Búsqueda.
* Filtros.
* Paginación.
* Dashboard.
* Documentación Swagger y ReDoc.

### Frontend

* Login.
* Rutas protegidas.
* Dashboard.
* Listado de pacientes.
* Búsqueda y filtros.
* Formularios de creación y edición.
* Cambio de prioridad y estado.
* Eliminación con confirmación.
* Mensajes de éxito y error.
* Diseño adaptable.

---

## 28. Protección de datos

Todos los datos incluidos en el archivo suministrado son ficticios.

No deben incorporarse:

* Datos reales de pacientes.
* Historias clínicas.
* Diagnósticos.
* Información médica sensible.
* Credenciales reales.

La aplicación se desarrolló exclusivamente con fines demostrativos y de evaluación técnica.
