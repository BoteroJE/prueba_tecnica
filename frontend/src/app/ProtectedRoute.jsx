import {
  Navigate,
  Outlet,
  useLocation,
} from "react-router";

import { LoadingScreen } from "../shared/components/LoadingScreen";
import { useAuth } from "./AuthProvider";

export function ProtectedRoute() {
  const {
    isAuthenticated,
    isLoading,
  } = useAuth();

  const location = useLocation();

  if (isLoading) {
    return (
      <LoadingScreen message="Validando sesión..." />
    );
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
        state={{
          from: location,
        }}
      />
    );
  }

  return <Outlet />;
}