import {
  NavLink,
  Outlet,
  useNavigate,
} from "react-router";

import { useAuth } from "../../app/AuthProvider";

function getInitials(fullName) {
  if (!fullName) {
    return "US";
  }

  return fullName
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

export function AppLayout() {
  const navigate = useNavigate();

  const {
    user,
    logout,
  } = useAuth();

  function handleLogout() {
    logout();

    navigate("/login", {
      replace: true,
    });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">
            +
          </div>

          <div>
            <strong>Clinic Tracker</strong>
            <span>Gestión asistencial</span>
          </div>
        </div>

        <nav
          className="sidebar-navigation"
          aria-label="Navegación principal"
        >
          <span className="sidebar-section-title">
            Seguimiento
          </span>

          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              isActive
                ? "sidebar-link active"
                : "sidebar-link"
            }
          >
            <span className="sidebar-link-icon">
              D
            </span>

            Dashboard
          </NavLink>

          <NavLink
            to="/patients"
            className={({ isActive }) =>
              isActive
                ? "sidebar-link active"
                : "sidebar-link"
            }
          >
            <span className="sidebar-link-icon">
              P
            </span>

            Pacientes
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <div className="sidebar-user">
            <div className="user-avatar">
              {getInitials(user?.full_name)}
            </div>

            <div className="sidebar-user-information">
              <strong>{user?.full_name}</strong>
              <span>{user?.role}</span>
            </div>
          </div>

          <button
            type="button"
            className="button button-logout"
            onClick={handleLogout}
          >
            Cerrar sesión
          </button>
        </div>
      </aside>

      <div className="app-main">
        <header className="topbar">
          <div>
            <span className="topbar-label">
              Sistema de seguimiento
            </span>

            <strong>
              Clínica · Atención de pacientes
            </strong>
          </div>

          <div className="topbar-user">
            <span>
              Sesión iniciada como
            </span>

            <strong>
              {user?.username}
            </strong>
          </div>
        </header>

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}