<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-navbar">
      <a class="navbar-brand" href="#">
        <img src="../assets/logo.png" alt="隙间小铺" class="navbar-logo" />
        <span class="brand-name">隙间小铺</span>
      </a>
    </nav>

    <!-- 登录表单 -->
    <section class="login-section">
      <div class="login-card">
        <!-- 网站Logo -->
        <img src="../assets/logo.png" alt="隙间小铺" class="login-logo" />

        <!-- 登录标题 -->
        <h2 class="login-title">登录</h2>

        <form @submit.prevent="login">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              v-model="username"
              required
              placeholder="请输入用户名"
            />
          </div>
          <div class="form-group">
            <label for="password">密码</label>
            <input
              type="password"
              id="password"
              v-model="password"
              required
              placeholder="请输入密码"
            />
          </div>
          <!-- 登录按钮 -->
          <button type="submit" class="btn btn-primary login-button">
            登录
          </button>
        </form>

        <!-- 注册账号和忘记密码按钮 -->
        <div class="additional-actions">
          <button class="btn btn-secondary small-button" @click="goToRegister">
            注册账号
          </button>
          <button
            class="btn btn-secondary small-button"
            @click="forgotPassword"
          >
            忘记密码
          </button>
        </div>

        <!-- 错误提示 -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <span>&copy; 2024 anka. 版权所有.</span>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/login/", {
          username: this.username,
          password: this.password,
        });

        const accessToken = response.data.access;
        const refreshToken = response.data.refresh;

        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);

        // 设置 axios 默认的 Authorization 头部
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${accessToken}`;

        this.$router.push("/home");
      } catch (error) {
        this.errorMessage = "登录失败，请检查用户名和密码是否正确。";
      }
    },

    goToRegister() {
      this.$router.push("/register");
    },
    forgotPassword() {
      this.$router.push("/forget-password");
    },
  },
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
}

.glass-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 60px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.brand-name {
  font-size: 1.5rem;
  color: #007bff;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.login-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

.login-logo {
  max-width: 100px;
  margin-bottom: 1rem;
}

.login-title {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: bold;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  font-size: 1.25rem;
}

.additional-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}

.small-button {
  width: 48%;
  padding: 0.5rem;
  font-size: 0.875rem;
}

.error-message {
  color: red;
  margin-top: 1rem;
}
</style>
<style scoped>
/* 设置背景图片覆盖整个网页，并固定不动 */
.app-container {
  min-height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
}

/* 导航栏毛玻璃效果 */
.glass-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 60px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.navbar-logo {
  height: 40px;
  margin-right: 0.5rem;
}

.brand-name {
  font-size: 1.5rem;
  font-family: "Microsoft Yahei UI light", cursive;
  color: #007bff;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  transition: color 0.3s ease, transform 0.3s ease;
}

.brand-name:hover {
  color: #0056b3;
  transform: scale(1.05);
}

/* 页脚 */
.footer {
  background: rgba(52, 58, 64, 0.8);
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

.container {
  max-width: 1140px;
  margin: 0 auto;
}
</style>
