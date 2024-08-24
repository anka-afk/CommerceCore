<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-navbar">
      <a class="navbar-brand" href="#">
        <img src="../assets/logo.png" alt="隙间小铺" class="navbar-logo" />
        <span class="brand-name">隙间小铺</span>
      </a>
    </nav>

    <!-- 找回密码表单 -->
    <section class="login-section">
      <div class="login-card">
        <!-- 网站Logo -->
        <img src="../assets/logo.png" alt="隙间小铺" class="login-logo" />

        <!-- 找回密码标题 -->
        <h2 class="login-title">找回密码</h2>

        <form @submit.prevent="resetPassword">
          <div class="form-group">
            <label for="email">电子邮箱</label>
            <input
              type="email"
              id="email"
              v-model="email"
              required
              placeholder="请输入注册时的电子邮箱"
            />
          </div>

          <!-- 找回密码按钮 -->
          <button type="submit" class="btn btn-primary login-button">
            找回密码
          </button>
        </form>

        <!-- 返回登录页面 -->
        <div class="additional-actions">
          <router-link to="/login" class="small-text">返回登录页面</router-link>
        </div>
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
      email: "",
    };
  },
  methods: {
    async resetPassword() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/password-reset/",
          {
            email: this.email,
          }
        );

        if (response.status === 200) {
          alert("找回密码邮件已发送，请检查您的邮箱。");
        } else {
          console.error("找回密码失败:", response.data);
        }
      } catch (error) {
        console.error(
          "找回密码失败:",
          error.response ? error.response.data : error.message
        );
      }
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
}

.small-text {
  font-size: 0.875rem;
  color: #007bff;
  text-decoration: none;
}

.small-text:hover {
  text-decoration: underline;
}

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
