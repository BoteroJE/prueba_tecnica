import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { DeletePatientDialog } from "../components/DeletePatientDialog";
import { PatientFormModal } from "../components/PatientFormModal";
import { epsApi } from "../epsApi";
import {
  PRIORITY_OPTIONS,
  STATUS_OPTIONS,
} from "../patientOptions";
import { patientsApi } from "../patientsApi";

function formatBirthDate(value) {
  if (!value) {
    return "—";
  }

  const date = new Date(`${value}T00:00:00`);

  return new Intl.DateTimeFormat("es-CO", {
    year: "numeric",
    month: "short",
    day: "2-digit",
  }).format(date);
}

function getStatusClass(status) {
  if (status === "Pendiente") {
    return "badge badge-pending";
  }

  if (status === "En atención") {
    return "badge badge-progress";
  }

  return "badge badge-attended";
}

function getPriorityClass(priority) {
  if (priority === "Alta") {
    return "badge badge-high";
  }

  if (priority === "Media") {
    return "badge badge-medium";
  }

  return "badge badge-low";
}

export function PatientsPage() {
  const [patients, setPatients] = useState([]);
  const [epsOptions, setEpsOptions] = useState([]);

  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);

  const [searchInput, setSearchInput] =
    useState("");

  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("");
  const [priority, setPriority] = useState("");
  const [epsId, setEpsId] = useState("");

  const [pagination, setPagination] = useState({
    total: 0,
    totalPages: 0,
    hasPrevious: false,
    hasNext: false,
  });

  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] =
    useState("");

  const [isFormOpen, setIsFormOpen] =
    useState(false);

  const [selectedPatient, setSelectedPatient] =
    useState(null);

  const [isSaving, setIsSaving] =
    useState(false);

  const [
    patientPendingDeletion,
    setPatientPendingDeletion,
  ] = useState(null);

  const [isDeleting, setIsDeleting] =
    useState(false);

  const [feedback, setFeedback] =
    useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadEps() {
      try {
        const response = await epsApi.list({
          signal: controller.signal,
        });

        setEpsOptions(response);
      } catch (error) {
        if (error.name !== "AbortError") {
          setFeedback({
            type: "error",
            message:
              error.message
              || "No fue posible cargar las EPS.",
          });
        }
      }
    }

    loadEps();

    return () => {
      controller.abort();
    };
  }, []);

  const loadPatients = useCallback(
    async (signal) => {
      setIsLoading(true);
      setErrorMessage("");

      try {
        const response = await patientsApi.list(
          {
            page,
            page_size: pageSize,
            search,
            status,
            priority,
            eps_id: epsId,
          },
          {
            signal,
          },
        );

        setPatients(response.items);

        setPagination({
          total: response.total,
          totalPages: response.total_pages,
          hasPrevious: response.has_previous,
          hasNext: response.has_next,
        });
      } catch (error) {
        if (error.name === "AbortError") {
          return;
        }

        setPatients([]);

        setErrorMessage(
          error.message
            || "No fue posible cargar los pacientes.",
        );
      } finally {
        if (!signal?.aborted) {
          setIsLoading(false);
        }
      }
    },
    [
      page,
      pageSize,
      search,
      status,
      priority,
      epsId,
    ],
  );

  useEffect(() => {
    const controller = new AbortController();

    loadPatients(controller.signal);

    return () => {
      controller.abort();
    };
  }, [loadPatients]);

  function openCreateForm() {
    setSelectedPatient(null);
    setIsFormOpen(true);
    setFeedback(null);
  }

  function openEditForm(patient) {
    setSelectedPatient(patient);
    setIsFormOpen(true);
    setFeedback(null);
  }

  function closeForm() {
    if (isSaving) {
      return;
    }

    setIsFormOpen(false);
    setSelectedPatient(null);
  }

  async function handleSavePatient(payload) {
    setIsSaving(true);

    const isEditing = Boolean(selectedPatient);

    try {
      if (isEditing) {
        await patientsApi.update(
          selectedPatient.id,
          payload,
        );
      } else {
        await patientsApi.create(payload);
      }

      setFeedback({
        type: "success",
        message: isEditing
          ? "El paciente fue actualizado correctamente."
          : "El paciente fue registrado correctamente.",
      });

      setIsFormOpen(false);
      setSelectedPatient(null);

      if (!isEditing && page !== 1) {
        setPage(1);
      } else {
        await loadPatients();
      }
    } finally {
      setIsSaving(false);
    }
  }

  async function handleDeletePatient() {
    if (!patientPendingDeletion) {
      return;
    }

    setIsDeleting(true);

    try {
      await patientsApi.remove(
        patientPendingDeletion.id,
      );

      setFeedback({
        type: "success",
        message:
          "El paciente fue eliminado correctamente.",
      });

      setPatientPendingDeletion(null);

      if (
        patients.length === 1
        && page > 1
      ) {
        setPage(
          (currentPage) => currentPage - 1,
        );
      } else {
        await loadPatients();
      }
    } finally {
      setIsDeleting(false);
    }
  }

  function handleSearch(event) {
    event.preventDefault();

    setPage(1);
    setSearch(searchInput.trim());
  }

  function handleClearFilters() {
    setSearchInput("");
    setSearch("");
    setStatus("");
    setPriority("");
    setEpsId("");
    setPage(1);
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">
            Gestión asistencial
          </span>

          <h1>Pacientes</h1>

          <p>
            Consulta, registra y actualiza los
            pacientes en espera de atención.
          </p>
        </div>

        <div className="page-header-actions">
          <div className="page-header-counter">
            <span>Registros encontrados</span>
            <strong>{pagination.total}</strong>
          </div>

          <button
            type="button"
            className="button button-primary"
            onClick={openCreateForm}
          >
            Nuevo paciente
          </button>
        </div>
      </header>

      {feedback && (
        <div
          className={
            feedback.type === "success"
              ? "feedback-message feedback-success"
              : "feedback-message feedback-error"
          }
          role="status"
        >
          <span>{feedback.message}</span>

          <button
            type="button"
            onClick={() => setFeedback(null)}
            aria-label="Cerrar mensaje"
          >
            ×
          </button>
        </div>
      )}

      <section className="patient-filters">
        <form
          className="patient-search"
          onSubmit={handleSearch}
        >
          <div className="form-field">
            <label htmlFor="patient-search">
              Nombre o documento
            </label>

            <div className="search-control">
              <input
                id="patient-search"
                type="search"
                value={searchInput}
                onChange={(event) => {
                  setSearchInput(event.target.value);
                }}
                placeholder="Buscar paciente..."
              />

              <button
                type="submit"
                className="button button-primary"
              >
                Buscar
              </button>
            </div>
          </div>
        </form>

        <div className="patient-filter-grid">
          <div className="form-field">
            <label htmlFor="status-filter">
              Estado
            </label>

            <select
              id="status-filter"
              value={status}
              onChange={(event) => {
                setStatus(event.target.value);
                setPage(1);
              }}
            >
              <option value="">
                Todos los estados
              </option>

              {STATUS_OPTIONS.map((option) => (
                <option
                  key={option}
                  value={option}
                >
                  {option}
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="priority-filter">
              Prioridad
            </label>

            <select
              id="priority-filter"
              value={priority}
              onChange={(event) => {
                setPriority(event.target.value);
                setPage(1);
              }}
            >
              <option value="">
                Todas las prioridades
              </option>

              {PRIORITY_OPTIONS.map((option) => (
                <option
                  key={option}
                  value={option}
                >
                  {option}
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="eps-filter">
              EPS
            </label>

            <select
              id="eps-filter"
              value={epsId}
              onChange={(event) => {
                setEpsId(event.target.value);
                setPage(1);
              }}
            >
              <option value="">
                Todas las EPS
              </option>

              {epsOptions.map((eps) => (
                <option
                  key={eps.id}
                  value={eps.id}
                >
                  {eps.name}
                </option>
              ))}
            </select>
          </div>

          <button
            type="button"
            className="button button-secondary clear-filters-button"
            onClick={handleClearFilters}
          >
            Limpiar filtros
          </button>
        </div>
      </section>

      {errorMessage && (
        <div className="page-error" role="alert">
          <div>
            <strong>
              No se pudieron cargar los pacientes
            </strong>

            <p>{errorMessage}</p>
          </div>

          <button
            type="button"
            className="button button-secondary"
            onClick={() => loadPatients()}
          >
            Reintentar
          </button>
        </div>
      )}

      <section className="patient-table-card">
        <div className="patient-table-header">
          <div>
            <h2>Listado de pacientes</h2>

            <p>
              Página {page} de{" "}
              {pagination.totalPages || 1}
            </p>
          </div>

          {isLoading && (
            <span className="table-loading-label">
              Actualizando...
            </span>
          )}
        </div>

        <div className="table-responsive">
          <table className="patient-table">
            <thead>
              <tr>
                <th>Paciente</th>
                <th>Documento</th>
                <th>Fecha de nacimiento</th>
                <th>EPS</th>
                <th>Prioridad</th>
                <th>Estado</th>
                <th>Teléfono</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {isLoading
                && patients.length === 0 && (
                  <tr>
                    <td
                      colSpan="8"
                      className="table-message"
                    >
                      Cargando pacientes...
                    </td>
                  </tr>
                )}

              {!isLoading
                && !errorMessage
                && patients.length === 0 && (
                  <tr>
                    <td
                      colSpan="8"
                      className="table-message"
                    >
                      No se encontraron pacientes con
                      los filtros seleccionados.
                    </td>
                  </tr>
                )}

              {patients.map((patient) => (
                <tr key={patient.id}>
                  <td>
                    <div className="patient-name-cell">
                      <strong>
                        {patient.full_name}
                      </strong>

                      <span>
                        {patient.gender}
                      </span>
                    </div>
                  </td>

                  <td>
                    <span className="document-cell">
                      {patient.document_type}
                    </span>{" "}
                    {patient.document_number}
                  </td>

                  <td>
                    {formatBirthDate(
                      patient.birth_date,
                    )}
                  </td>

                  <td>
                    <div className="eps-cell">
                      <strong>
                        {patient.eps.name}
                      </strong>

                      <span>
                        {patient.eps.code}
                      </span>
                    </div>
                  </td>

                  <td>
                    <span
                      className={getPriorityClass(
                        patient.priority,
                      )}
                    >
                      {patient.priority}
                    </span>
                  </td>

                  <td>
                    <span
                      className={getStatusClass(
                        patient.status,
                      )}
                    >
                      {patient.status}
                    </span>
                  </td>

                  <td>{patient.phone}</td>

                  <td>
                    <div className="table-actions">
                      <button
                        type="button"
                        className="table-action-button"
                        onClick={() => {
                          openEditForm(patient);
                        }}
                      >
                        Editar
                      </button>

                      <button
                        type="button"
                        className="table-action-button table-action-danger"
                        onClick={() => {
                          setPatientPendingDeletion(
                            patient,
                          );
                        }}
                      >
                        Eliminar
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <footer className="pagination">
          <span>
            Mostrando {patients.length} de{" "}
            {pagination.total} registros
          </span>

          <div className="pagination-actions">
            <button
              type="button"
              className="button button-secondary"
              disabled={
                !pagination.hasPrevious
                || isLoading
              }
              onClick={() => {
                setPage((currentPage) =>
                  Math.max(1, currentPage - 1),
                );
              }}
            >
              Anterior
            </button>

            <span className="pagination-page">
              {page}
            </span>

            <button
              type="button"
              className="button button-secondary"
              disabled={
                !pagination.hasNext
                || isLoading
              }
              onClick={() => {
                setPage(
                  (currentPage) => currentPage + 1,
                );
              }}
            >
              Siguiente
            </button>
          </div>
        </footer>
      </section>

      <PatientFormModal
        isOpen={isFormOpen}
        patient={selectedPatient}
        epsOptions={epsOptions}
        isSaving={isSaving}
        onClose={closeForm}
        onSubmit={handleSavePatient}
      />

      <DeletePatientDialog
        patient={patientPendingDeletion}
        isDeleting={isDeleting}
        onCancel={() => {
          if (!isDeleting) {
            setPatientPendingDeletion(null);
          }
        }}
        onConfirm={handleDeletePatient}
      />
    </section>
  );
}