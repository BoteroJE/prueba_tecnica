import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { MetricCard } from "../components/MetricCard";
import { dashboardApi } from "../dashboardApi";

export function DashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const loadDashboard = useCallback(async (signal) => {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await dashboardApi.getMetrics({
        signal,
      });

      setMetrics(response);
    } catch (error) {
      if (error.name === "AbortError") {
        return;
      }

      setErrorMessage(
        error.message
          || "No fue posible cargar el dashboard.",
      );
    } finally {
      if (!signal?.aborted) {
        setIsLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();

    loadDashboard(controller.signal);

    return () => {
      controller.abort();
    };
  }, [loadDashboard]);

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">
            Resumen operativo
          </span>

          <h1>Dashboard</h1>

          <p>
            Consulta el volumen y el estado general
            de la atención.
          </p>
        </div>

        <button
          type="button"
          className="button button-secondary"
          onClick={() => loadDashboard()}
          disabled={isLoading}
        >
          {isLoading
            ? "Actualizando..."
            : "Actualizar"}
        </button>
      </header>

      {errorMessage && (
        <div className="page-error" role="alert">
          <div>
            <strong>
              No se pudieron cargar los indicadores
            </strong>

            <p>{errorMessage}</p>
          </div>

          <button
            type="button"
            className="button button-secondary"
            onClick={() => loadDashboard()}
          >
            Reintentar
          </button>
        </div>
      )}

      {isLoading && !metrics && (
        <div className="content-loading">
          <div className="loading-spinner" />

          <p>Cargando indicadores...</p>
        </div>
      )}

      {metrics && (
        <>
          <div className="metrics-grid">
            <MetricCard
              label="Pacientes registrados"
              value={metrics.total_patients}
              description="Total de pacientes incluidos en el sistema."
              variant="total"
            />

            <MetricCard
              label="Pendientes"
              value={metrics.pending_patients}
              description="Pacientes que todavía esperan atención."
              variant="pending"
            />

            <MetricCard
              label="En atención"
              value={metrics.in_progress_patients}
              description="Pacientes atendidos actualmente."
              variant="progress"
            />

            <MetricCard
              label="Atendidos"
              value={metrics.attended_patients}
              description="Pacientes cuya atención ya finalizó."
              variant="attended"
            />

            <MetricCard
              label="Prioridad alta"
              value={metrics.high_priority_patients}
              description="Pacientes que requieren atención prioritaria."
              variant="high"
            />
          </div>

          <section className="dashboard-summary">
            <header>
              <h2>Distribución por estado</h2>

              <p>
                Los valores se calculan directamente
                desde la base de datos.
              </p>
            </header>

            <div className="status-summary-list">
              <div className="status-summary-row">
                <div>
                  <span className="status-dot status-pending" />
                  Pendientes
                </div>

                <strong>
                  {metrics.pending_patients}
                </strong>
              </div>

              <div className="status-summary-row">
                <div>
                  <span className="status-dot status-progress" />
                  En atención
                </div>

                <strong>
                  {metrics.in_progress_patients}
                </strong>
              </div>

              <div className="status-summary-row">
                <div>
                  <span className="status-dot status-attended" />
                  Atendidos
                </div>

                <strong>
                  {metrics.attended_patients}
                </strong>
              </div>
            </div>
          </section>
        </>
      )}
    </section>
  );
}