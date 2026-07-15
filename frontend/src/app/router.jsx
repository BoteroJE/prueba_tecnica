import {
  createBrowserRouter,
  Navigate,
} from "react-router";

import { LoginPage } from "../modules/auth/pages/LoginPage";
import { DashboardPage } from "../modules/dashboard/pages/DashboardPage";
import { PatientsPage } from "../modules/patients/pages/PatientsPage";
import { AppLayout } from "../shared/components/AppLayout";
import { GuestRoute } from "./GuestRoute";
import { ProtectedRoute } from "./ProtectedRoute";

export const router = createBrowserRouter([
  {
    element: <GuestRoute />,
    children: [
      {
        path: "/login",
        element: <LoginPage />,
      },
    ],
  },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          {
            index: true,
            element: (
              <Navigate
                to="/dashboard"
                replace
              />
            ),
          },
          {
            path: "/dashboard",
            element: <DashboardPage />,
          },
          {
            path: "/patients",
            element: <PatientsPage />,
          },
        ],
      },
    ],
  },
  {
    path: "*",
    element: (
      <Navigate
        to="/"
        replace
      />
    ),
  },
]);