# Clinic Patient Tracker — Frontend

Interfaz web para la gestión de pacientes en espera de atención.

El frontend permite iniciar sesión, consultar indicadores operativos, buscar y filtrar pacientes, registrar nuevos pacientes, editar su información, cambiar su prioridad o estado y eliminar registros con confirmación previa.

La aplicación consume una API REST desarrollada con FastAPI.

---

## 1. Tecnologías utilizadas

* React.
* Vite.
* React Router.
* JavaScript.
* Fetch API.
* Context API.
* CSS tradicional.
* Session Storage para conservar temporalmente la sesión.

No se utilizan Redux, Axios ni librerías externas de componentes visuales, con el fin de mantener una solución sencilla y apropiada para el alcance de la prueba técnica.

---

## 2. Funcionalidades

### Autenticación

* Inicio de sesión con usuario y contraseña.
* Consumo del endpoint `POST /auth/login`.
* Almacenamiento temporal del JWT.
* Recuperación de sesión al recargar la página.
* Consulta del usuario autenticado.
* Cierre de sesión.
* Redirección automática al login cuando el token expira.
* Protección de rutas privadas.

### Dashboard

* Total de pacientes registrados.
* Pacientes pendientes.
* Pacientes en atención.
* Pacientes atendidos.
* Pacientes con prioridad alta.
* Actualización manual de indicadores.
* Manejo de estados de carga y error.

### Gestión de pacientes

* Listado paginado.
* Búsqueda por nombre o documento.
* Filtro por estado.
* Filtro por prioridad.
* Filtro por EPS.
* Registro de pacientes.
* Edición de pacientes.
* Cambio de estado.
* Cambio de prioridad.
* Eliminación con confirmación.
* Mensajes de éxito y error.
* Validaciones básicas en formularios.

---

## 3. Requisitos previos

Antes de ejecutar el frontend se requiere:

* Node.js 20.19 o superior.
* npm.
* Backend de FastAPI en ejecución.
* Base de datos inicializada con los datos sintéticos.

Verificar las versiones instaladas:

```bash
node --version
npm --version
```

---

## 4. Estructura del frontend

```text
frontend/
├── src/
│   ├── app/
│   │   ├── AuthProvider.jsx
│   │   ├── GuestRoute.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── router.jsx
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── authApi.js
│   │   │   └── pages/
│   │   │       └── LoginPage.jsx
│   │   │
│   │   ├── dashboard/
│   │   │   ├── dashboardApi.js
│   │   │   ├── components/
│   │   │   │   └── MetricCard.jsx
│   │   │   └── pages/
│   │   │       └── DashboardPage.jsx
│   │   │
│   │   └── patients/
│   │       ├── components/
│   │       │   ├── DeletePatientDialog.jsx
│   │       │   └── PatientFormModal.jsx
│   │       ├── pages/
│   │       │   └── PatientsPage.jsx
│   │       ├── epsApi.js
│   │       ├── patientOptions.js
│   │       └── patientsApi.js
│   │
│   ├── shared/
│   │   ├── api/
│   │   │   └── httpClient.js
│   │   ├── auth/
│   │   │   └── tokenStorage.js
│   │   └── components/
│   │       ├── AppLayout.jsx
│   │       └── LoadingScreen.jsx
│   │
│   ├── styles/
│   │   └── global.css
│   │
│   └── main.jsx
│
├── .env
├── .env.example
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

---

## 5. Arquitectura del frontend

El frontend está organizado por funcionalidades:

```text
auth
dashboard
patients
```

Cada módulo contiene sus páginas, componentes y funciones de acceso a la API.

El flujo general es:

```text
Componente React
      ↓
Archivo API del módulo
      ↓
httpClient
      ↓
API REST FastAPI
```

El cliente HTTP centralizado se encarga de:

* Construir las URL.
* Agregar el JWT.
* Enviar JSON o formularios.
* Interpretar respuestas.
* Procesar errores.
* Detectar respuestas `401`.
* Eliminar una sesión inválida.

---

## 6. Instalación

Desde la raíz del repositorio:

```bash
cd frontend
```

Instalar las dependencias:

```bash
npm install
```

---

## 7. Variables de entorno

Crear el archivo `.env` tomando como referencia `.env.example`.

En PowerShell:

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

Las variables expuestas por Vite deben comenzar con:

```text
VITE_
```

No deben almacenarse contraseñas, claves JWT ni información sensible en el frontend.

Después de modificar `.env`, es necesario reiniciar Vite.

---

## 8. Ejecutar el frontend

Desde `frontend`:

```bash
npm run dev
```

La aplicación estará disponible normalmente en:

```text
http://localhost:5173
```

El backend debe estar ejecutándose en:

```text
http://127.0.0.1:8000
```

---

## 9. Credenciales de demostración

### Administrador

```text
Usuario: admin.demo
Contraseña: Demo2026*
```

### Operador

```text
Usuario: operador.demo
Contraseña: Demo2026*
```

La pantalla de inicio de sesión incluye botones para cargar automáticamente estas credenciales.

---

## 10. Autenticación

El login se realiza mediante:

```http
POST /api/v1/auth/login
```

El backend recibe:

```text
application/x-www-form-urlencoded
```

Campos:

```text
username
password
```

Respuesta esperada:

```json
{
  "access_token": "eyJhbGciOi...",
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

El token se almacena en:

```text
sessionStorage
```

Cada solicitud protegida incluye:

```http
Authorization: Bearer TOKEN
```

La sesión se valida nuevamente al recargar la aplicación mediante:

```http
GET /api/v1/auth/me
```

Si el token expiró o no es válido:

1. El backend devuelve `401`.
2. El cliente HTTP elimina el token.
3. El contexto de autenticación actualiza la sesión.
4. React Router redirige al login.

---

## 11. Rutas del frontend

### Login

```text
/login
```

Ruta pública.

### Dashboard

```text
/dashboard
```

Ruta protegida.

### Pacientes

```text
/patients
```

Ruta protegida.

Si un usuario no autenticado intenta ingresar a una ruta privada, será redirigido a `/login`.

---

## 12. Dashboard

El dashboard consume:

```http
GET /api/v1/dashboard
```

Respuesta esperada:

```json
{
  "total_patients": 1000,
  "pending_patients": 378,
  "in_progress_patients": 182,
  "attended_patients": 440,
  "high_priority_patients": 185
}
```

La interfaz muestra estos valores mediante tarjetas de indicadores.

Los datos no se almacenan en el frontend. Siempre se consultan desde la API.

---

## 13. Listado de pacientes

La página de pacientes consume:

```http
GET /api/v1/patients
```

Parámetros disponibles:

| Parámetro   | Descripción          |
| ----------- | -------------------- |
| `page`      | Número de página     |
| `page_size` | Registros por página |
| `search`    | Nombre o documento   |
| `status`    | Estado               |
| `priority`  | Prioridad            |
| `eps_id`    | Identificador de EPS |

Ejemplo:

```text
/api/v1/patients?page=1&page_size=20&status=Pendiente&priority=Alta
```

El frontend envía únicamente los filtros que tienen un valor seleccionado.

---

## 14. Catálogo de EPS

El selector de EPS consume:

```http
GET /api/v1/eps
```

La respuesta se utiliza tanto en:

* Filtro de pacientes.
* Formulario de creación.
* Formulario de edición.

---

## 15. Registrar un paciente

Endpoint utilizado:

```http
POST /api/v1/patients
```

Ejemplo:

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

Después de una creación exitosa:

* Se cierra el formulario.
* Se muestra un mensaje de confirmación.
* Se actualiza el listado.
* Se actualiza el contador de registros.

---

## 16. Editar un paciente

Endpoint utilizado:

```http
PATCH /api/v1/patients/{patient_id}
```

El formulario permite actualizar:

* Tipo de documento.
* Número de documento.
* Nombre.
* Fecha de nacimiento.
* Género.
* Teléfono.
* Correo.
* Ciudad.
* EPS.
* Prioridad.
* Estado.

Aunque el backend acepta actualizaciones parciales, el formulario actual envía la información completa visible del paciente.

---

## 17. Eliminar un paciente

Endpoint utilizado:

```http
DELETE /api/v1/patients/{patient_id}
```

Antes de ejecutar la solicitud se presenta un cuadro de confirmación que muestra:

* Nombre del paciente.
* Tipo de documento.
* Número de documento.
* Advertencia de eliminación permanente.

Una eliminación exitosa devuelve:

```text
204 No Content
```

Después de eliminar:

* Se cierra el cuadro de confirmación.
* Se muestra un mensaje de éxito.
* Se actualiza el listado.
* Se ajusta la paginación cuando es necesario.

---

## 18. Validaciones del formulario

### Documento

* Obligatorio.
* Entre 4 y 20 caracteres.

### Nombre completo

* Obligatorio.
* Al menos 3 caracteres.

### Fecha de nacimiento

* Obligatoria.
* No puede ser futura.

### Teléfono

* Obligatorio.
* Debe contener entre 7 y 15 dígitos.

### EPS

* Obligatoria.

### Prioridad

Valores permitidos:

```text
Alta
Media
Baja
```

### Estado

Valores permitidos:

```text
Pendiente
En atención
Atendido
```

El backend realiza una segunda validación y conserva la autoridad final sobre los datos.

---

## 19. Manejo de errores

El frontend interpreta respuestas de error de la API.

### `401 Unauthorized`

* El token no es válido o expiró.
* Se elimina la sesión.
* Se redirige al login.

### `404 Not Found`

* El recurso solicitado no existe.

### `409 Conflict`

* Documento duplicado.
* Conflicto de integridad.

### `422 Unprocessable Entity`

* Datos inválidos.
* Formato incorrecto.
* Regla de validación incumplida.

### Error de conexión

Mensaje mostrado:

```text
No fue posible conectarse con el servidor.
```

---

## 20. Compilar para producción

Ejecutar:

```bash
npm run build
```

Los archivos compilados se generan en:

```text
frontend/dist/
```

Revisar localmente la compilación:

```bash
npm run preview
```

---

## 21. Scripts disponibles

```bash
npm run dev
```

Inicia el servidor de desarrollo.

```bash
npm run build
```

Genera la versión de producción.

```bash
npm run preview
```

Sirve localmente la compilación.

```bash
npm run lint
```

Ejecuta las reglas de ESLint incluidas por Vite, siempre que el archivo de configuración permanezca en el proyecto.

---

## 22. Solución de problemas

### El login funciona, pero no aparecen pacientes ni indicadores

Verificar que las páginas estén utilizando:

```javascript
dashboardApi.getMetrics()
patientsApi.list()
```

Revisar en las herramientas del navegador:

```text
F12 → Network
```

Confirmar que existan solicitudes a:

```text
/api/v1/dashboard
/api/v1/patients
/api/v1/eps
```

### Error CORS

Confirmar en el backend:

```env
CORS_ORIGINS=["http://localhost:5173"]
```

Después reiniciar FastAPI.

### Error `401`

Cerrar sesión e ingresar nuevamente.

También puede borrarse manualmente:

```text
sessionStorage
```

desde las herramientas del navegador.

### Error de conexión

Confirmar que FastAPI esté ejecutándose:

```bash
uvicorn app.main:app --reload
```

Y que la variable sea:

```env
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

### Los cambios del `.env` no se reflejan

Reiniciar Vite:

```bash
npm run dev
```

### El frontend abre en otro puerto

Si Vite utiliza, por ejemplo:

```text
http://localhost:5174
```

debe agregarse ese origen en el `.env` del backend:

```env
CORS_ORIGINS=["http://localhost:5173","http://localhost:5174"]
```

---

## 23. Consideraciones de seguridad

* El frontend no conoce la clave utilizada para firmar los JWT.
* Las contraseñas no se almacenan en el navegador.
* El token se guarda en `sessionStorage`.
* Los endpoints protegidos requieren `Authorization: Bearer`.
* Los datos utilizados son sintéticos.
* No deben incorporarse datos reales de pacientes.
* La validación del frontend mejora la experiencia, pero no sustituye la validación del backend.

---

## 24. Alcance actual

El frontend cubre:

* Inicio de sesión.
* Rutas protegidas.
* Recuperación de sesión.
* Cierre de sesión.
* Dashboard.
* Listado paginado.
* Búsqueda.
* Filtros.
* Registro.
* Edición.
* Cambio de estado.
* Cambio de prioridad.
* Eliminación con confirmación.
* Mensajes de éxito y error.
* Diseño adaptable para escritorio y dispositivos pequeños.
