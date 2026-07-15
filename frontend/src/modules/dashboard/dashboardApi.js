import { httpClient } from "../../shared/api/httpClient";

export const dashboardApi = {
  getMetrics(options = {}) {
    return httpClient.get("/dashboard", options);
  },
};