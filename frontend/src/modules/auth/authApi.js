import { httpClient } from "../../shared/api/httpClient";

export const authApi = {
  login(username, password) {
    const formData = new URLSearchParams();

    formData.set("username", username);
    formData.set("password", password);

    return httpClient.post("/auth/login", {
      body: formData,
      auth: false,
    });
  },

  getCurrentUser() {
    return httpClient.get("/auth/me");
  },
};