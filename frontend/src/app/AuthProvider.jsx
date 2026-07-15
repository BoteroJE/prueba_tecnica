import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import { authApi } from "../modules/auth/authApi";
import {
  clearSession,
  getAccessToken,
  getStoredUser,
  saveSession,
} from "../shared/auth/tokenStorage";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(
    () => getAccessToken(),
  );

  const [user, setUser] = useState(
    () => getStoredUser(),
  );

  const [isLoading, setIsLoading] = useState(
    true,
  );

  const logout = useCallback(() => {
    clearSession();
    setAccessToken(null);
    setUser(null);
  }, []);

  const login = useCallback(
    async (username, password) => {
      const response = await authApi.login(
        username,
        password,
      );

      saveSession(
        response.access_token,
        response.user,
      );

      setAccessToken(response.access_token);
      setUser(response.user);

      return response.user;
    },
    [],
  );

  useEffect(() => {
    let isCancelled = false;

    async function restoreSession() {
      const storedToken = getAccessToken();

      if (!storedToken) {
        if (!isCancelled) {
          setIsLoading(false);
        }

        return;
      }

      try {
        const currentUser =
          await authApi.getCurrentUser();

        if (isCancelled) {
          return;
        }

        saveSession(
          storedToken,
          currentUser,
        );

        setAccessToken(storedToken);
        setUser(currentUser);
      } catch {
        if (!isCancelled) {
          logout();
        }
      } finally {
        if (!isCancelled) {
          setIsLoading(false);
        }
      }
    }

    restoreSession();

    return () => {
      isCancelled = true;
    };
  }, [logout]);

  useEffect(() => {
    function handleUnauthorized() {
      logout();
    }

    window.addEventListener(
      "auth:unauthorized",
      handleUnauthorized,
    );

    return () => {
      window.removeEventListener(
        "auth:unauthorized",
        handleUnauthorized,
      );
    };
  }, [logout]);

  const contextValue = useMemo(
    () => ({
      user,
      accessToken,
      isLoading,
      isAuthenticated: Boolean(
        accessToken && user,
      ),
      login,
      logout,
    }),
    [
      user,
      accessToken,
      isLoading,
      login,
      logout,
    ],
  );

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth debe utilizarse dentro de AuthProvider.",
    );
  }

  return context;
}