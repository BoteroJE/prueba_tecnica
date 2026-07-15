import {
  clearSession,
  getAccessToken,
} from "../auth/tokenStorage";

const rawApiUrl = import.meta.env.VITE_API_URL;

if (!rawApiUrl) {
  throw new Error(
    "No se encontró la variable VITE_API_URL.",
  );
}

const API_URL = rawApiUrl.replace(/\/+$/, "");

export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);

    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

function buildUrl(path, params) {
  const normalizedPath = path.startsWith("/")
    ? path
    : `/${path}`;

  const url = new URL(`${API_URL}${normalizedPath}`);

  if (!params) {
    return url.toString();
  }

  Object.entries(params).forEach(([key, value]) => {
    if (
      value === undefined
      || value === null
      || value === ""
    ) {
      return;
    }

    url.searchParams.set(key, String(value));
  });

  return url.toString();
}

function getErrorMessage(data, status) {
  if (typeof data === "string" && data.trim()) {
    return data;
  }

  if (typeof data?.detail === "string") {
    return data.detail;
  }

  if (Array.isArray(data?.detail)) {
    return data.detail
      .map((error) => error.msg)
      .filter(Boolean)
      .join(" ");
  }

  if (typeof data?.message === "string") {
    return data.message;
  }

  if (status === 401) {
    return "La sesión no es válida o ha expirado.";
  }

  if (status === 404) {
    return "El recurso solicitado no existe.";
  }

  if (status === 422) {
    return "Los datos enviados no son válidos.";
  }

  if (status >= 500) {
    return "Ocurrió un error interno en el servidor.";
  }

  return "No fue posible completar la solicitud.";
}

async function parseResponse(response) {
  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get(
    "content-type",
  );

  if (contentType?.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

async function request(
  path,
  {
    method = "GET",
    body = undefined,
    params = undefined,
    headers = {},
    auth = true,
    signal = undefined,
  } = {},
) {
  const requestHeaders = new Headers(headers);

  if (auth) {
    const accessToken = getAccessToken();

    if (accessToken) {
      requestHeaders.set(
        "Authorization",
        `Bearer ${accessToken}`,
      );
    }
  }

  let requestBody = body;

  if (
    body !== undefined
    && body !== null
    && !(body instanceof FormData)
    && !(body instanceof URLSearchParams)
    && typeof body !== "string"
  ) {
    requestHeaders.set(
      "Content-Type",
      "application/json",
    );

    requestBody = JSON.stringify(body);
  }

  if (body instanceof URLSearchParams) {
    requestHeaders.set(
      "Content-Type",
      "application/x-www-form-urlencoded",
    );
  }

  let response;

  try {
    response = await fetch(
      buildUrl(path, params),
      {
        method,
        headers: requestHeaders,
        body: requestBody,
        signal,
      },
    );
  } catch (error) {
    if (error.name === "AbortError") {
      throw error;
    }

    throw new ApiError(
      "No fue posible conectarse con el servidor.",
      0,
    );
  }

  const responseData = await parseResponse(
    response,
  );

  if (!response.ok) {
    if (response.status === 401 && auth) {
      clearSession();

      window.dispatchEvent(
        new Event("auth:unauthorized"),
      );
    }

    throw new ApiError(
      getErrorMessage(
        responseData,
        response.status,
      ),
      response.status,
      responseData,
    );
  }

  return responseData;
}

export const httpClient = {
  get(path, options = {}) {
    return request(path, {
      ...options,
      method: "GET",
    });
  },

  post(path, options = {}) {
    return request(path, {
      ...options,
      method: "POST",
    });
  },

  patch(path, options = {}) {
    return request(path, {
      ...options,
      method: "PATCH",
    });
  },

  delete(path, options = {}) {
    return request(path, {
      ...options,
      method: "DELETE",
    });
  },
};