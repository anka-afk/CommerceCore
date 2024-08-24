import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";

// 在应用启动时配置axios
const token = localStorage.getItem("token");
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

createApp(App).use(router).mount("#app");

axios.interceptors.request.use(
  async (config) => {
    let accessToken = localStorage.getItem("access_token");

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/token/refresh/",
          {
            refresh: refreshToken,
          }
        );

        const newAccessToken = response.data.access;
        localStorage.setItem("access_token", newAccessToken);
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${newAccessToken}`;

        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return axios(originalRequest);
      } catch (err) {
        console.log("Refresh token failed", err);
        // Handle token refresh failure (e.g., redirect to login)
      }
    }

    return Promise.reject(error);
  }
);
