import {
  Navigate,
  Outlet,
} from "react-router";

import { LoadingScreen } from "../shared/components/LoadingScreen";
import { useAuth } from "./AuthProvider";

export function GuestRoute() {
  const {
    isAuthenticated,
    isLoading,
  } = useAuth();

  if (isLoading) {
    return (
      <LoadingScreen message="Validando sesión..." />
    );
  }

  if (isAuthenticated) {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    );
  }

  return <Outlet />;
}