import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import axios from "axios";
import BaseTemplate from "@/components/BaseTemplate.vue";

const token = localStorage.getItem("access_token");
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

const app = createApp(App);
app.component("BaseTemplate", BaseTemplate);

// 定期刷新令牌的间隔时间（例如每4分钟刷新一次）
const refreshInterval = 4 * 60 * 1000;

app.mixin({
  mounted() {
    this.refreshTokenInterval = setInterval(() => {
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        axios
          .post("http://127.0.0.1:8000/api/token/refresh/", {
            refresh: refreshToken,
          })
          .then((response) => {
            const newAccessToken = response.data.access;
            localStorage.setItem("access_token", newAccessToken);
            axios.defaults.headers.common[
              "Authorization"
            ] = `Bearer ${newAccessToken}`;
          })
          .catch((error) => {
            console.error("Failed to refresh access token:", error);
            // 如果刷新令牌失败，则注销用户并重定向到登录页面
            clearInterval(this.refreshTokenInterval);
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            router.push({ name: "LoginPage" });
          });
      }
    }, refreshInterval);
  },
  beforeUnmount() {
    clearInterval(this.refreshTokenInterval);
  },
});

app.use(router).mount("#app");

axios.interceptors.request.use(
  (config) => {
    let accessToken = localStorage.getItem("access_token");
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/token/refresh/",
          { refresh: refreshToken }
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
        // 处理刷新失败，重定向到登录页面
        router.push({ name: "LoginPage" });
      }
    }
    return Promise.reject(error);
  }
);
