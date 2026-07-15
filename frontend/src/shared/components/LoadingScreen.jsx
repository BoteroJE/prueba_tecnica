export function LoadingScreen({
  message = "Cargando aplicación...",
}) {
  return (
    <div
      className="loading-screen"
      role="status"
      aria-live="polite"
    >
      <div className="loading-spinner" />

      <p>{message}</p>
    </div>
  );
}