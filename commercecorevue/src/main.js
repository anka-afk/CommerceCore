import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import BaseTemplate from "@/components/BaseTemplate.vue";
import ModalTemplate from "@/components/ModalTemplate.vue";
import "./assets/global.css";
import store from "./store"; // 引入 Vuex Store

// 获取初始的 access_token 并设置 axios 请求头
const token = localStorage.getItem("access_token");
if (token) {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

const app = createApp(App);
app.component("BaseTemplate", BaseTemplate);
app.component("ModalTemplate", ModalTemplate);
app.use(store); // 使用 Vuex Store

app.use(router).mount("#app");

// 请求拦截器：在每次请求前确保发送最新的 access_token
axios.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("access_token");
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：处理令牌过期和自动刷新
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");

      if (refreshToken) {
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
          console.log("Failed to refresh token:", err);
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          router.push({ name: "LoginPage" });
          return Promise.reject(err);
        }
      } else {
        router.push({ name: "LoginPage" });
      }
    }

    // 如果还是 401 错误，清除令牌并跳转到登录页面
    if (
      error.response &&
      error.response.status === 401 &&
      originalRequest._retry
    ) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      router.push({ name: "LoginPage" });
    }

    return Promise.reject(error);
  }
);
