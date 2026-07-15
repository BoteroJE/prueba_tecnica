import {
  useState,
} from "react";

import {
  useLocation,
  useNavigate,
} from "react-router";

import { useAuth } from "../../../app/AuthProvider";

const DEMO_CREDENTIALS = {
  admin: {
    username: "admin.demo",
    password: "Demo2026*",
  },
  operator: {
    username: "operador.demo",
    password: "Demo2026*",
  },
};

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const { login } = useAuth();

  const [username, setUsername] = useState(
    "",
  );

  const [password, setPassword] = useState(
    "",
  );

  const [errorMessage, setErrorMessage] =
    useState("");

  const [isSubmitting, setIsSubmitting] =
    useState(false);

  function loadDemoCredentials(type) {
    const credentials =
      DEMO_CREDENTIALS[type];

    setUsername(credentials.username);
    setPassword(credentials.password);
    setErrorMessage("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const normalizedUsername =
      username.trim();

    if (!normalizedUsername || !password) {
      setErrorMessage(
        "Ingresa el usuario y la contraseña.",
      );

      return;
    }

    setIsSubmitting(true);
    setErrorMessage("");

    try {
      await login(
        normalizedUsername,
        password,
      );

      const previousLocation =
        location.state?.from;

      const destination = previousLocation
        ? `${previousLocation.pathname}${
            previousLocation.search ?? ""
          }`
        : "/dashboard";

      navigate(destination, {
        replace: true,
      });
    } catch (error) {
      setErrorMessage(
        error.message
          || "No fue posible iniciar sesión.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-information">
        <div className="login-brand">
          <div className="login-brand-icon">
            +
          </div>

          <div>
            <span className="login-brand-name">
              Clinic Tracker
            </span>

            <span className="login-brand-description">
              Seguimiento de pacientes
            </span>
          </div>
        </div>

        <div className="login-information-content">
          <span className="eyebrow">
            Gestión asistencial
          </span>

          <h1>
            Administra la espera de atención
            de forma clara y sencilla.
          </h1>

          <p>
            Consulta pacientes, identifica
            prioridades, actualiza estados y
            revisa los indicadores operativos
            del servicio.
          </p>

          <div className="login-feature-list">
            <div className="login-feature">
              <span>01</span>
              <p>Búsqueda rápida por paciente.</p>
            </div>

            <div className="login-feature">
              <span>02</span>
              <p>
                Priorización y seguimiento del
                estado de atención.
              </p>
            </div>

            <div className="login-feature">
              <span>03</span>
              <p>
                Indicadores actualizados desde la
                base de datos.
              </p>
            </div>
          </div>
        </div>

        <p className="login-data-notice">
          Aplicación demostrativa con datos
          completamente sintéticos.
        </p>
      </section>

      <section className="login-form-section">
        <div className="login-card">
          <header className="login-card-header">
            <span className="eyebrow">
              Acceso al sistema
            </span>

            <h2>Iniciar sesión</h2>

            <p>
              Ingresa las credenciales asignadas
              para acceder al módulo de seguimiento.
            </p>
          </header>

          <form
            className="login-form"
            onSubmit={handleSubmit}
            noValidate
          >
            <div className="form-field">
              <label htmlFor="username">
                Usuario
              </label>

              <input
                id="username"
                name="username"
                type="text"
                value={username}
                onChange={(event) => {
                  setUsername(event.target.value);
                }}
                autoComplete="username"
                placeholder="Ej. admin.demo"
                disabled={isSubmitting}
                required
              />
            </div>

            <div className="form-field">
              <label htmlFor="password">
                Contraseña
              </label>

              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={(event) => {
                  setPassword(event.target.value);
                }}
                autoComplete="current-password"
                placeholder="Ingresa tu contraseña"
                disabled={isSubmitting}
                required
              />
            </div>

            {errorMessage && (
              <div
                className="form-error"
                role="alert"
              >
                {errorMessage}
              </div>
            )}

            <button
              className="button button-primary button-full"
              type="submit"
              disabled={isSubmitting}
            >
              {isSubmitting
                ? "Ingresando..."
                : "Ingresar"}
            </button>
          </form>

          <div className="demo-credentials">
            <p>Credenciales de demostración</p>

            <div className="demo-credential-buttons">
              <button
                type="button"
                className="button button-secondary"
                onClick={() => {
                  loadDemoCredentials("admin");
                }}
                disabled={isSubmitting}
              >
                Usar administrador
              </button>

              <button
                type="button"
                className="button button-secondary"
                onClick={() => {
                  loadDemoCredentials("operator");
                }}
                disabled={isSubmitting}
              >
                Usar operador
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}