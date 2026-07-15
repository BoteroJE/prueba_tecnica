import {
  useEffect,
  useState,
} from "react";

export function DeletePatientDialog({
  patient,
  isDeleting,
  onCancel,
  onConfirm,
}) {
  const [errorMessage, setErrorMessage] =
    useState("");

  useEffect(() => {
    setErrorMessage("");
  }, [patient]);

  useEffect(() => {
    if (!patient) {
      return undefined;
    }

    function handleKeyDown(event) {
      if (
        event.key === "Escape"
        && !isDeleting
      ) {
        onCancel();
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
  }, [
    patient,
    isDeleting,
    onCancel,
  ]);

  if (!patient) {
    return null;
  }

  async function handleConfirm() {
    try {
      setErrorMessage("");
      await onConfirm();
    } catch (error) {
      setErrorMessage(
        error.message
          || "No fue posible eliminar el paciente.",
      );
    }
  }

  return (
    <div
      className="modal-backdrop"
      onMouseDown={(event) => {
        if (
          event.target === event.currentTarget
          && !isDeleting
        ) {
          onCancel();
        }
      }}
    >
      <section
        className="modal-card delete-dialog"
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="delete-patient-title"
      >
        <div className="delete-dialog-icon">
          !
        </div>

        <h2 id="delete-patient-title">
          Eliminar paciente
        </h2>

        <p>
          Esta acción eliminará permanentemente a:
        </p>

        <div className="delete-patient-summary">
          <strong>{patient.full_name}</strong>

          <span>
            {patient.document_type}{" "}
            {patient.document_number}
          </span>
        </div>

        <p className="delete-dialog-warning">
          Esta operación no se puede deshacer.
        </p>

        {errorMessage && (
          <div
            className="form-error"
            role="alert"
          >
            {errorMessage}
          </div>
        )}

        <footer className="modal-actions">
          <button
            type="button"
            className="button button-secondary"
            onClick={onCancel}
            disabled={isDeleting}
          >
            Cancelar
          </button>

          <button
            type="button"
            className="button button-danger"
            onClick={handleConfirm}
            disabled={isDeleting}
          >
            {isDeleting
              ? "Eliminando..."
              : "Eliminar paciente"}
          </button>
        </footer>
      </section>
    </div>
  );
}