import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  DOCUMENT_TYPE_OPTIONS,
  GENDER_OPTIONS,
  PRIORITY_OPTIONS,
  STATUS_OPTIONS,
} from "../patientOptions";

const EMPTY_FORM = {
  document_type: "CC",
  document_number: "",
  full_name: "",
  birth_date: "",
  gender: "Femenino",
  phone: "",
  email: "",
  city: "",
  eps_id: "",
  priority: "Media",
  status: "Pendiente",
};

function getPatientFormValues(patient) {
  if (!patient) {
    return {
      ...EMPTY_FORM,
    };
  }

  return {
    document_type:
      patient.document_type ?? "CC",

    document_number:
      patient.document_number ?? "",

    full_name:
      patient.full_name ?? "",

    birth_date:
      patient.birth_date ?? "",

    gender:
      patient.gender ?? "Femenino",

    phone:
      patient.phone ?? "",

    email:
      patient.email ?? "",

    city:
      patient.city ?? "",

    eps_id:
      patient.eps?.id
        ? String(patient.eps.id)
        : "",

    priority:
      patient.priority ?? "Media",

    status:
      patient.status ?? "Pendiente",
  };
}

function validatePatientForm(formValues) {
  const errors = {};

  if (!formValues.document_type) {
    errors.document_type =
      "Selecciona el tipo de documento.";
  }

  const documentNumber =
    formValues.document_number.trim();

  if (!documentNumber) {
    errors.document_number =
      "Ingresa el número de documento.";
  } else if (
    documentNumber.length < 4
    || documentNumber.length > 20
  ) {
    errors.document_number =
      "El documento debe tener entre 4 y 20 caracteres.";
  }

  const fullName = formValues.full_name.trim();

  if (!fullName) {
    errors.full_name =
      "Ingresa el nombre completo.";
  } else if (fullName.length < 3) {
    errors.full_name =
      "El nombre debe tener al menos 3 caracteres.";
  }

  if (!formValues.birth_date) {
    errors.birth_date =
      "Selecciona la fecha de nacimiento.";
  } else {
    const selectedDate = new Date(
      `${formValues.birth_date}T00:00:00`,
    );

    const today = new Date();

    today.setHours(0, 0, 0, 0);

    if (selectedDate > today) {
      errors.birth_date =
        "La fecha de nacimiento no puede ser futura.";
    }
  }

  if (!formValues.gender) {
    errors.gender =
      "Selecciona el género.";
  }

  const phoneDigits = formValues.phone.replace(
    /\D/g,
    "",
  );

  if (!formValues.phone.trim()) {
    errors.phone =
      "Ingresa el teléfono.";
  } else if (
    phoneDigits.length < 7
    || phoneDigits.length > 15
  ) {
    errors.phone =
      "El teléfono debe contener entre 7 y 15 dígitos.";
  }

  if (!formValues.eps_id) {
    errors.eps_id =
      "Selecciona una EPS.";
  }

  if (!formValues.priority) {
    errors.priority =
      "Selecciona una prioridad.";
  }

  if (!formValues.status) {
    errors.status =
      "Selecciona un estado.";
  }

  return errors;
}

export function PatientFormModal({
  isOpen,
  patient,
  epsOptions,
  isSaving,
  onClose,
  onSubmit,
}) {
  const [formValues, setFormValues] = useState(
    EMPTY_FORM,
  );

  const [errors, setErrors] = useState({});
  const [serverError, setServerError] =
    useState("");

  const isEditing = Boolean(patient);

  const title = isEditing
    ? "Editar paciente"
    : "Registrar paciente";

  const maximumBirthDate = useMemo(
    () => new Date().toISOString().split("T")[0],
    [],
  );

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    setFormValues(
      getPatientFormValues(patient),
    );

    setErrors({});
    setServerError("");
  }, [isOpen, patient]);

  useEffect(() => {
    if (!isOpen) {
      return undefined;
    }

    function handleKeyDown(event) {
      if (
        event.key === "Escape"
        && !isSaving
      ) {
        onClose();
      }
    }

    window.addEventListener(
      "keydown",
      handleKeyDown,
    );

    return () => {
      window.removeEventListener(
        "keydown",
        handleKeyDown,
      );
    };
  }, [isOpen, isSaving, onClose]);

  if (!isOpen) {
    return null;
  }

  function handleChange(event) {
    const {
      name,
      value,
    } = event.target;

    setFormValues((currentValues) => ({
      ...currentValues,
      [name]: value,
    }));

    setErrors((currentErrors) => ({
      ...currentErrors,
      [name]: undefined,
    }));

    setServerError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    const validationErrors =
      validatePatientForm(formValues);

    if (
      Object.keys(validationErrors).length > 0
    ) {
      setErrors(validationErrors);
      return;
    }

    const payload = {
      document_type:
        formValues.document_type,

      document_number:
        formValues.document_number.trim(),

      full_name:
        formValues.full_name.trim(),

      birth_date:
        formValues.birth_date,

      gender:
        formValues.gender,

      phone:
        formValues.phone.trim(),

      email:
        formValues.email.trim() || null,

      city:
        formValues.city.trim() || null,

      eps_id:
        Number(formValues.eps_id),

      priority:
        formValues.priority,

      status:
        formValues.status,
    };

    try {
      setServerError("");

      await onSubmit(payload);
    } catch (error) {
      setServerError(
        error.message
          || "No fue posible guardar el paciente.",
      );
    }
  }

  return (
    <div
      className="modal-backdrop"
      onMouseDown={(event) => {
        if (
          event.target === event.currentTarget
          && !isSaving
        ) {
          onClose();
        }
      }}
    >
      <section
        className="modal-card patient-form-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="patient-form-title"
      >
        <header className="modal-header">
          <div>
            <span className="eyebrow">
              Gestión de pacientes
            </span>

            <h2 id="patient-form-title">
              {title}
            </h2>

            <p>
              Completa la información básica del
              paciente y su estado de atención.
            </p>
          </div>

          <button
            type="button"
            className="modal-close-button"
            onClick={onClose}
            disabled={isSaving}
            aria-label="Cerrar formulario"
          >
            ×
          </button>
        </header>

        <form
          className="patient-form"
          onSubmit={handleSubmit}
          noValidate
        >
          {serverError && (
            <div
              className="form-error form-error-full"
              role="alert"
            >
              {serverError}
            </div>
          )}

          <div className="patient-form-grid">
            <div className="form-field">
              <label htmlFor="document_type">
                Tipo de documento
              </label>

              <select
                id="document_type"
                name="document_type"
                value={formValues.document_type}
                onChange={handleChange}
                disabled={isSaving}
              >
                {DOCUMENT_TYPE_OPTIONS.map(
                  (option) => (
                    <option
                      key={option}
                      value={option}
                    >
                      {option}
                    </option>
                  ),
                )}
              </select>

              {errors.document_type && (
                <span className="field-error">
                  {errors.document_type}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="document_number">
                Número de documento
              </label>

              <input
                id="document_number"
                name="document_number"
                type="text"
                value={formValues.document_number}
                onChange={handleChange}
                disabled={isSaving}
                maxLength={20}
                placeholder="Ej. 1234567890"
              />

              {errors.document_number && (
                <span className="field-error">
                  {errors.document_number}
                </span>
              )}
            </div>

            <div className="form-field form-field-full">
              <label htmlFor="full_name">
                Nombre completo
              </label>

              <input
                id="full_name"
                name="full_name"
                type="text"
                value={formValues.full_name}
                onChange={handleChange}
                disabled={isSaving}
                maxLength={150}
                placeholder="Nombre y apellidos"
              />

              {errors.full_name && (
                <span className="field-error">
                  {errors.full_name}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="birth_date">
                Fecha de nacimiento
              </label>

              <input
                id="birth_date"
                name="birth_date"
                type="date"
                value={formValues.birth_date}
                onChange={handleChange}
                disabled={isSaving}
                max={maximumBirthDate}
              />

              {errors.birth_date && (
                <span className="field-error">
                  {errors.birth_date}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="gender">
                Género
              </label>

              <select
                id="gender"
                name="gender"
                value={formValues.gender}
                onChange={handleChange}
                disabled={isSaving}
              >
                {GENDER_OPTIONS.map((option) => (
                  <option
                    key={option}
                    value={option}
                  >
                    {option}
                  </option>
                ))}
              </select>

              {errors.gender && (
                <span className="field-error">
                  {errors.gender}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="phone">
                Teléfono
              </label>

              <input
                id="phone"
                name="phone"
                type="tel"
                value={formValues.phone}
                onChange={handleChange}
                disabled={isSaving}
                maxLength={20}
                placeholder="Ej. 3005551122"
              />

              {errors.phone && (
                <span className="field-error">
                  {errors.phone}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="email">
                Correo
              </label>

              <input
                id="email"
                name="email"
                type="email"
                value={formValues.email}
                onChange={handleChange}
                disabled={isSaving}
                maxLength={150}
                placeholder="correo@ejemplo.com"
              />
            </div>

            <div className="form-field">
              <label htmlFor="city">
                Ciudad
              </label>

              <input
                id="city"
                name="city"
                type="text"
                value={formValues.city}
                onChange={handleChange}
                disabled={isSaving}
                maxLength={80}
                placeholder="Ej. Cali"
              />
            </div>

            <div className="form-field">
              <label htmlFor="eps_id">
                EPS
              </label>

              <select
                id="eps_id"
                name="eps_id"
                value={formValues.eps_id}
                onChange={handleChange}
                disabled={isSaving}
              >
                <option value="">
                  Selecciona una EPS
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

              {errors.eps_id && (
                <span className="field-error">
                  {errors.eps_id}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="priority">
                Prioridad
              </label>

              <select
                id="priority"
                name="priority"
                value={formValues.priority}
                onChange={handleChange}
                disabled={isSaving}
              >
                {PRIORITY_OPTIONS.map((option) => (
                  <option
                    key={option}
                    value={option}
                  >
                    {option}
                  </option>
                ))}
              </select>

              {errors.priority && (
                <span className="field-error">
                  {errors.priority}
                </span>
              )}
            </div>

            <div className="form-field">
              <label htmlFor="status">
                Estado
              </label>

              <select
                id="status"
                name="status"
                value={formValues.status}
                onChange={handleChange}
                disabled={isSaving}
              >
                {STATUS_OPTIONS.map((option) => (
                  <option
                    key={option}
                    value={option}
                  >
                    {option}
                  </option>
                ))}
              </select>

              {errors.status && (
                <span className="field-error">
                  {errors.status}
                </span>
              )}
            </div>
          </div>

          <footer className="modal-actions">
            <button
              type="button"
              className="button button-secondary"
              onClick={onClose}
              disabled={isSaving}
            >
              Cancelar
            </button>

            <button
              type="submit"
              className="button button-primary"
              disabled={isSaving}
            >
              {isSaving
                ? "Guardando..."
                : isEditing
                  ? "Guardar cambios"
                  : "Registrar paciente"}
            </button>
          </footer>
        </form>
      </section>
    </div>
  );
}