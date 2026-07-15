const TOKEN_STORAGE_KEY = "clinic_access_token";
const USER_STORAGE_KEY = "clinic_authenticated_user";

export function getAccessToken() {
  return sessionStorage.getItem(TOKEN_STORAGE_KEY);
}

export function getStoredUser() {
  const storedUser = sessionStorage.getItem(
    USER_STORAGE_KEY,
  );

  if (!storedUser) {
    return null;
  }

  try {
    return JSON.parse(storedUser);
  } catch {
    sessionStorage.removeItem(USER_STORAGE_KEY);
    return null;
  }
}

export function saveSession(accessToken, user) {
  if (!accessToken || !user) {
    throw new Error(
      "No es posible guardar una sesión incompleta.",
    );
  }

  sessionStorage.setItem(
    TOKEN_STORAGE_KEY,
    accessToken,
  );

  sessionStorage.setItem(
    USER_STORAGE_KEY,
    JSON.stringify(user),
  );
}

export function clearSession() {
  sessionStorage.removeItem(TOKEN_STORAGE_KEY);
  sessionStorage.removeItem(USER_STORAGE_KEY);
}