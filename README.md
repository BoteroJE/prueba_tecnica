# Clinic Patient Tracker

Aplicación web full stack para gestionar pacientes en espera de atención en una clínica.

El sistema permite autenticar usuarios, consultar pacientes, buscar y filtrar registros, crear y actualizar pacientes, modificar su estado o prioridad, eliminar registros y visualizar indicadores operativos.

El proyecto utiliza datos completamente sintéticos y fue desarrollado como solución para una prueba técnica de Desarrollador Full Stack Junior.

---

## 1. Funcionalidades principales

### Autenticación

* Inicio de sesión con usuario y contraseña.
* Validación contra usuarios almacenados en SQLite.
* Contraseñas almacenadas mediante hash Argon2.
* Autenticación con JWT.
* Protección de rutas del backend.
* Protección de rutas del frontend.
* Recuperación de sesión al recargar la página.
* Cierre de sesión.
* Redirección automática cuando el token expira.

### Dashboard

* Total de pacientes registrados.
* Pacientes pendientes.
* Pacientes en atención.
* Pacientes atendidos.
* Pacientes con prioridad alta.
* Actualización manual de indicadores.
* Indicadores calculados directamente desde la base de datos.

### Gestión de pacientes

* Listado paginado.
* Consulta individual.
* Búsqueda por nombre o documento.
* Filtro por estado.
* Filtro por prioridad.
* Filtro por EPS.
* Registro de pacientes.
* Edición de pacientes.
* Cambio de estado.
* Cambio de prioridad.
* Eliminación con confirmación.
* Validación de formularios.
* Mensajes de éxito y error.

### Datos iniciales

* Importación de 1.000 pacientes sintéticos.
* Importación de 10 EPS.
* Importación de 2 usuarios de demostración.
* Importación idempotente para evitar duplicados.

---

## 2. Tecnologías utilizadas

### Backend

* Python 3.11 o superior.
* FastAPI.
* SQLAlchemy 2.
* SQLite.
* Pydantic 2.
* Pydantic Settings.
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
* Session Storage.
* CSS tradicional.

---

## 3. Arquitectura

El proyecto está organizado como un monorepo con frontend y backend separados:

```text
clinic-patient-tracker/
├── backend/
├── frontend/
└── README.md
```

El backend está desarrollado como un **monolito modular**. Todos los módulos se ejecutan dentro de una única aplicación FastAPI, pero el código está separado por funcionalidad:

```text
auth
users
eps
patients
dashboard
```

El frontend también está organizado por funcionalidad:

```text
auth
dashboard
patients
```

Flujo general:

```text
React + Vite
      ↓
API REST con JWT
      ↓
FastAPI
      ↓
SQLAlchemy
      ↓
SQLite
```

---

## 4. Estructura general

```text
clinic-patient-tracker/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── db/
│   │   ├── importers/
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── eps/
│   │   │   ├── patients/
│   │   │   └── users/
│   │   ├── shared/
│   │   ├── api_router.py
│   │   └── main.py
│   ├── data/
│   │   ├── raw/
│   │   │   └── datos_sinteticos.ods
│   │   └── clinic.db
│   ├── scripts/
│   ├── .env.example
│   ├── README.md
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   └── patients/
│   │   ├── shared/
│   │   ├── styles/
│   │   └── main.jsx
│   ├── .env.example
│   ├── README.md
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Requisitos

## 5. Requisitos del sistema

### Backend

* Python 3.11 o superior.
* `pip`.
* Soporte para entornos virtuales de Python.

### Frontend

* Node.js 20.19 o superior.
* npm.

### Verificación

```bash
python --version
node --version
npm --version
```

En algunos sistemas Windows puede ser necesario utilizar:

```bash
py --version
```

---

## 6. Archivo de datos sintéticos

El archivo ODS debe estar ubicado en:

```text
backend/data/raw/datos_sinteticos.ods
```

El archivo suministrado originalmente puede llamarse:

```text
Datos_Sinteticos_Prueba_Full_Stack_Junior_2026(2).ods
```

Se recomienda renombrarlo a:

```text
datos_sinteticos.ods
```

El archivo contiene:

* 1.000 pacientes sintéticos.
* 10 EPS.
* Tipos de documento.
* Géneros.
* Prioridades.
* Estados.
* Diccionario de datos.
* Usuarios de demostración.

---

# Instalación

## 7. Clonar o descargar el proyecto

Ubicarse en la carpeta del repositorio:

```bash
cd clinic-patient-tracker
```

---

## 8. Instalación del backend

Entrar al backend:

```bash
cd backend
```

### Crear el entorno virtual

Windows:

```bash
python -m venv .venv
```

Linux o macOS:

```bash
python3 -m venv .venv
```

### Activar el entorno virtual

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

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Crear el archivo de configuración

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux o macOS:

```bash
cp .env.example .env
```

Contenido esperado de `backend/.env`:

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

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copiar el resultado en:

```env
JWT_SECRET_KEY=CLAVE_GENERADA
```

La clave JWT no debe publicarse en el repositorio.

---

## 9. Importar los datos iniciales

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

La importación es idempotente. Al ejecutarla nuevamente no debe duplicar información:

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

---

## 10. Instalación del frontend

Abrir otra terminal y ubicarse en:

```bash
cd clinic-patient-tracker/frontend
```

Instalar dependencias:

```bash
npm install
```

Crear el archivo `.env`:

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux o macOS:

```bash
cp .env.example .env
```

Contenido esperado de `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

---

# Ejecución

## 11. Ejecutar el backend

Desde `backend`, con el entorno virtual activo:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

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

Verificación de salud:

```text
http://127.0.0.1:8000/api/v1/health
```

---

## 12. Ejecutar el frontend

Desde `frontend`:

```bash
npm run dev
```

La interfaz estará disponible normalmente en:

```text
http://localhost:5173
```

El frontend y el backend deben permanecer ejecutándose al mismo tiempo.

---

## 13. Ejecución rápida en dos terminales

### Terminal 1: backend

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m scripts.import_ods
uvicorn app.main:app --reload
```

### Terminal 2: frontend

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

# Credenciales de demostración

## 14. Usuario administrador

```text
Usuario: admin.demo
Contraseña: Demo2026*
Rol: ADMIN
```

## 15. Usuario operador

```text
Usuario: operador.demo
Contraseña: Demo2026*
Rol: OPERADOR
```

Las contraseñas se almacenan en SQLite mediante hash Argon2, no como texto plano.

Actualmente ambos usuarios pueden acceder a las funcionalidades del sistema.

---

# API REST

## 16. Endpoints disponibles

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

Excepto el login y el endpoint de salud, las rutas requieren un token JWT.

---

## 17. Parámetros del listado de pacientes

```http
GET /api/v1/patients
```

| Parámetro   | Descripción          | Valor predeterminado |
| ----------- | -------------------- | -------------------: |
| `page`      | Número de página     |                  `1` |
| `page_size` | Registros por página |                 `20` |
| `search`    | Nombre o documento   |                Vacío |
| `status`    | Estado               |                Vacío |
| `priority`  | Prioridad            |                Vacío |
| `eps_id`    | Identificador de EPS |                Vacío |

Ejemplo:

```text
/api/v1/patients?page=1&page_size=20&status=Pendiente&priority=Alta
```

---

## 18. Catálogos controlados

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

Los valores deben conservar exactamente los espacios y las tildes.

---

# Decisiones técnicas

## 19. Monolito modular

Se eligió un monolito modular porque el proyecto tiene un alcance pequeño y un número limitado de historias de usuario.

Esta decisión permite:

* Mantener una sola aplicación backend.
* Evitar la complejidad de microservicios.
* Separar responsabilidades por funcionalidad.
* Facilitar el mantenimiento.
* Permitir una futura extracción de módulos si el sistema crece.

---

## 20. Separación entre frontend y backend

El frontend y el backend están separados dentro del mismo repositorio.

Esto permite:

* Desarrollar cada aplicación de forma independiente.
* Mantener contratos claros mediante la API REST.
* Cambiar el frontend sin modificar la lógica del backend.
* Sustituir el backend o consumirlo desde otros clientes en el futuro.

---

## 21. SQLite

Se eligió SQLite por las siguientes razones:

* Instalación sencilla.
* No requiere un servidor de base de datos.
* Es suficiente para 1.000 registros sintéticos.
* Facilita la ejecución local de la prueba.
* Permite entregar una solución reproducible rápidamente.

SQLAlchemy permite sustituir SQLite por PostgreSQL u otro motor en una evolución posterior.

---

## 22. SQLAlchemy síncrono

Se utilizaron sesiones síncronas de SQLAlchemy.

Para el volumen actual y el alcance de la prueba, una configuración asíncrona agregaría complejidad sin aportar una mejora significativa.

---

## 23. JWT

Se eligió JWT para la autenticación porque:

* Evita mantener sesiones en memoria en el backend.
* Es sencillo de integrar con React.
* Permite proteger los endpoints mediante el encabezado `Authorization`.
* Incluye una fecha de expiración.

---

## 24. Argon2

Las contraseñas se protegen mediante Argon2 porque es un algoritmo adecuado para hashing de contraseñas.

La contraseña original nunca se almacena en la base de datos.

---

## 25. Session Storage

El token JWT se guarda en `sessionStorage`.

Esta decisión permite:

* Conservar la sesión al recargar la página.
* Eliminar la sesión al cerrar la pestaña.
* Evitar una persistencia indefinida en el navegador.

Para un sistema productivo de mayor nivel de seguridad podría evaluarse el uso de cookies `HttpOnly`.

---

## 26. Context API

Se utiliza Context API únicamente para administrar el estado global de autenticación.

No se incorporó Redux porque el estado compartido es reducido y no justifica una dependencia adicional.

---

## 27. Fetch API

Se utiliza la API nativa `fetch`.

No se incorporó Axios porque las operaciones requeridas pueden resolverse mediante un cliente HTTP pequeño y centralizado.

---

## 28. CSS sin librería visual

La interfaz fue implementada con CSS tradicional.

Esto reduce dependencias y permite controlar directamente:

* Diseño.
* Comportamiento responsive.
* Formularios.
* Tablas.
* Modales.
* Estados visuales.

---

## 29. Importación idempotente

El importador puede ejecutarse varias veces sin duplicar:

* EPS.
* Usuarios.
* Pacientes.

Los pacientes se identifican principalmente por su documento, los usuarios por su nombre de usuario y las EPS por su código.

---

## 30. Dashboard calculado en tiempo real

Los indicadores no se almacenan en una tabla independiente.

Se calculan directamente desde los registros actuales de pacientes para evitar inconsistencias entre los datos y las estadísticas.

---

# Limitaciones conocidas

## 31. SQLite y concurrencia

SQLite es apropiado para ejecución local y cargas pequeñas, pero presenta limitaciones cuando existen muchas escrituras concurrentes.

Para un despliegue productivo con múltiples usuarios simultáneos se recomienda PostgreSQL.

---

## 32. Sin migraciones de base de datos

El proyecto crea las tablas mediante `Base.metadata.create_all()`.

Actualmente no se utiliza Alembic.

Esto significa que los cambios futuros en el esquema no se aplicarán automáticamente sobre bases de datos existentes. En una versión productiva se deben implementar migraciones.

---

## 33. Sin control granular de permisos

Existen los roles:

```text
ADMIN
OPERADOR
```

Sin embargo, actualmente ambos roles tienen acceso a las mismas funcionalidades.

No se han implementado permisos específicos como:

* Solo administradores pueden eliminar.
* Operadores solo pueden consultar o actualizar.
* Gestión de usuarios.
* Asignación dinámica de roles.

---

## 34. Sin administración de usuarios

Los usuarios se importan desde el archivo ODS.

La aplicación no incluye interfaces ni endpoints para:

* Crear usuarios.
* Editar usuarios.
* Eliminar usuarios.
* Cambiar contraseñas.
* Recuperar contraseñas.

---

## 35. Eliminación física

La eliminación de pacientes es permanente.

No se implementó:

* Eliminación lógica.
* Papelera.
* Recuperación de registros.
* Historial de eliminaciones.

---

## 36. Sin auditoría

El sistema no registra:

* Qué usuario creó un paciente.
* Qué usuario modificó el estado.
* Fecha y valor anterior de cada cambio.
* Qué usuario eliminó un registro.
* Historial de accesos.

En un sistema clínico real esta funcionalidad sería importante.

---

## 37. Sin historial de estados

Solo se conserva el estado actual del paciente.

No existe una tabla que registre transiciones como:

```text
Pendiente → En atención → Atendido
```

Tampoco se registra cuánto tiempo permaneció el paciente en cada estado.

---

## 38. Seguridad del token en el navegador

El token se almacena en `sessionStorage`, lo que simplifica la prueba, pero puede ser accesible desde JavaScript si existiera una vulnerabilidad XSS.

Para un entorno productivo se recomienda evaluar cookies seguras con:

```text
HttpOnly
Secure
SameSite
```

---

## 39. Sin renovación de token

El sistema genera un único token de acceso con duración limitada.

No se implementaron:

* Refresh tokens.
* Renovación silenciosa.
* Revocación de tokens.
* Lista de tokens invalidados.

Cuando el token expira, el usuario debe iniciar sesión nuevamente.

---

## 40. Validaciones limitadas al alcance

Las validaciones cubren las reglas principales de la prueba, pero no incluyen verificaciones avanzadas como:

* Validez real del documento colombiano.
* Validación real del número telefónico.
* Confirmación del correo.
* Homologación de ciudades.
* Verificación externa de EPS.
* Detección avanzada de pacientes duplicados.

---

## 41. Búsqueda sencilla

La búsqueda se realiza por coincidencia parcial en:

* Nombre.
* Documento.

No se implementó:

* Búsqueda difusa.
* Corrección de errores tipográficos.
* Búsqueda sin sensibilidad a tildes en todos los motores.
* Motor de búsqueda especializado.
* Ordenamiento configurable desde el frontend.

---

## 42. Paginación por desplazamiento

La API utiliza paginación mediante `offset` y `limit`.

Es adecuada para 1.000 registros, pero puede perder eficiencia con millones de filas. Para conjuntos de datos grandes se recomienda paginación basada en cursor.

---

## 43. Sin actualización automática del dashboard

El dashboard se actualiza:

* Al ingresar a la página.
* Al presionar el botón de actualización.
* Al recargar la interfaz.

No se implementaron:

* WebSockets.
* Server-Sent Events.
* Actualización periódica automática.
* Sincronización en tiempo real entre usuarios.

---

## 44. Sin despliegue productivo incluido

El proyecto está preparado principalmente para ejecución local.

No incluye configuración específica para:

* Docker.
* Nginx.
* HTTPS.
* Dominio.
* CI/CD.
* Hosting.
* Variables de entorno administradas.
* Monitoreo.
* Copias de seguridad.

---

## 45. Archivo ODS requerido para la carga inicial

La carga inicial depende del archivo:

```text
backend/data/raw/datos_sinteticos.ods
```

Si el archivo no existe, el importador no podrá crear los datos de demostración.

La aplicación puede continuar funcionando con una base ya creada, pero no podrá regenerar los datos iniciales sin el ODS.

---

## 46. Datos únicamente sintéticos

La aplicación fue diseñada para datos ficticios.

No debe utilizarse en producción con información real de pacientes sin implementar previamente:

* Cifrado.
* Auditoría.
* Políticas de acceso.
* Gestión de consentimiento.
* Copias de seguridad.
* Seguridad de infraestructura.
* Cumplimiento de la normativa aplicable a datos personales y clínicos.

---

# Comandos útiles

## 47. Reiniciar la base de datos

Detener FastAPI.

Desde la raíz del repositorio, eliminar:

```powershell
Remove-Item backend\data\clinic.db
```

Entrar al backend:

```bash
cd backend
```

Importar nuevamente:

```bash
python -m scripts.import_ods
```

Iniciar FastAPI:

```bash
uvicorn app.main:app --reload
```

---

## 48. Compilar el frontend

Desde `frontend`:

```bash
npm run build
```

La compilación se generará en:

```text
frontend/dist/
```

Para revisar la compilación:

```bash
npm run preview
```

---

## 49. Solución de problemas frecuentes

### El frontend no se conecta

Verificar que FastAPI esté disponible en:

```text
http://127.0.0.1:8000/docs
```

Verificar `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

### Error CORS

Verificar `backend/.env`:

```env
CORS_ORIGINS=["http://localhost:5173"]
```

Reiniciar FastAPI después de modificar el archivo.

### El login funciona, pero no aparecen datos

Abrir:

```text
F12 → Network
```

Comprobar las solicitudes:

```text
/api/v1/dashboard
/api/v1/patients
/api/v1/eps
```

### La base de datos está vacía

Ejecutar:

```bash
python -m scripts.import_ods
```

### El token expiró

Cerrar sesión e iniciar nuevamente con las credenciales de demostración.

### Vite utiliza otro puerto

Agregar el nuevo origen en `backend/.env`.

Ejemplo:

```env
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

Después reiniciar FastAPI.

---

# Protección de datos

## 50. Consideración final

Todos los registros entregados para la prueba son sintéticos.

No deben incorporarse:

* Datos reales de pacientes.
* Historias clínicas.
* Diagnósticos.
* Información médica sensible.
* Credenciales reales.
* Documentos reales de identificación.

La solución tiene fines exclusivamente demostrativos y de evaluación técnica.
