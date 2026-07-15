import { httpClient } from "../../shared/api/httpClient";

export const patientsApi = {
  list(params = {}, options = {}) {
    return httpClient.get("/patients", {
      ...options,
      params,
    });
  },

  getById(patientId, options = {}) {
    return httpClient.get(
      `/patients/${patientId}`,
      options,
    );
  },

  create(patientData) {
    return httpClient.post("/patients", {
      body: patientData,
    });
  },

  update(patientId, patientData) {
    return httpClient.patch(
      `/patients/${patientId}`,
      {
        body: patientData,
      },
    );
  },

  remove(patientId) {
    return httpClient.delete(
      `/patients/${patientId}`,
    );
  },
};