import { httpClient } from "../../shared/api/httpClient";

export const epsApi = {
  list(options = {}) {
    return httpClient.get("/eps", options);
  },
};