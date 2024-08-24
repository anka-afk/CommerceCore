<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-navbar">
      <a class="navbar-brand" href="#">
        <img src="../assets/logo.png" alt="隙间小铺" class="navbar-logo" />
        <span class="brand-name">隙间小铺</span>
      </a>
    </nav>

    <!-- 注册表单 -->
    <section class="login-section">
      <div class="login-card">
        <!-- 网站Logo -->
        <img src="../assets/logo.png" alt="隙间小铺" class="login-logo" />

        <!-- 注册标题 -->
        <h2 class="login-title">注册</h2>

        <form @submit.prevent="register">
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
          <div class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              required
              placeholder="请再次输入密码"
            />
            <p v-if="passwordMismatch" class="error-message">
              两次输入的密码不一致
            </p>
          </div>
          <div class="form-group">
            <label for="phone">电话号码</label>
            <input
              type="text"
              id="phone"
              v-model="phone"
              required
              placeholder="请输入电话号码"
            />
          </div>
          <div class="form-group">
            <label for="email">电子邮箱</label>
            <input
              type="email"
              id="email"
              v-model="email"
              required
              placeholder="请输入电子邮箱"
            />
          </div>

          <div class="form-group terms-checkbox">
            <label for="terms">
              <input type="checkbox" id="terms" v-model="agreedToTerms" />
              我已阅读并同意
              <a href="#" @click.prevent="showTermsModal">服务条款与隐私政策</a>
            </label>
          </div>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

          <!-- 注册按钮 -->
          <button
            type="submit"
            class="btn btn-primary login-button"
            :disabled="!agreedToTerms"
          >
            注册
          </button>
        </form>

        <!-- 已有账户 -->
        <div class="additional-actions">
          <router-link to="/login" class="small-text"
            >已有账户? 点击登录</router-link
          >
        </div>
      </div>
    </section>

    <!-- 服务条款与隐私政策 模态框 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>服务条款与隐私政策</h3>
        <p><strong>隐私政策</strong></p>
        <p>邮箱为本站服务的唯一凭证，请妥善保管。</p>
        <p>
          用户密码均为密文储存，无法解密，但出于安全起见还是请使用随机密码或使用密码管理器。
        </p>
        <p><strong>使用条款</strong></p>
        <p>在使用服务时，需遵循站点和节点所在国家的法律。</p>
        <p>对于免费用户，本站有权在不通知的情况下删除账户。</p>
        <p>
          任何违反使用条款的用户，我们将会删除违规账户并收回使用本站服务的权利。
        </p>
        <button class="btn btn-success" @click="closeModal">了解</button>
      </div>
    </div>

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
      confirmPassword: "",
      phone: "",
      email: "",
      agreedToTerms: false,
      showModal: false,
      passwordMismatch: false,
      errorMessage: "", // 错误信息
    };
  },
  watch: {
    confirmPassword() {
      this.passwordMismatch = this.password !== this.confirmPassword;
    },
  },
  methods: {
    async register() {
      if (this.passwordMismatch) {
        this.errorMessage = "两次输入的密码不一致";
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/register/",
          {
            username: this.username,
            password: this.password,
            confirm_password: this.confirmPassword,
            phone_number: this.phone,
            email: this.email,
          }
        );

        if (response.status === 201) {
          this.$router.push("/login");
        }
      } catch (error) {
        if (error.response && error.response.data) {
          const errors = error.response.data;
          if (errors.username) {
            this.errorMessage = "用户名已经被注册";
          } else if (errors.email) {
            this.errorMessage = "邮箱已经被注册";
          } else {
            this.errorMessage = "注册失败，请检查输入信息";
          }
        } else {
          this.errorMessage = "注册失败，请稍后重试";
        }
      }
    },

    showTermsModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
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

.error-message {
  color: red;
  margin-top: 0.5rem;
  font-size: 0.875rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
  width: 100%;
  text-align: left;
  overflow-y: auto;
  max-height: 80vh;
  backdrop-filter: blur(10px);
}

.modal-content button {
  display: block;
  margin: 1rem auto 0;
  padding: 0.5rem 1rem;
  background-color: #28a745;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
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

.terms-checkbox label {
  display: flex;
  align-items: center;
  white-space: nowrap; /* 防止换行 */
  font-size: 14px; /* 适当调整文本大小 */
}

.terms-checkbox input[type="checkbox"] {
  margin-right: 0px; /* 调整复选框与文本之间的间距 */
}

.terms-checkbox a {
  color: #007bff; /* 设置链接颜色 */
  text-decoration: none;
  margin-left: 4px; /* 调整链接与前面文本的间距 */
}

.terms-checkbox a:hover {
  text-decoration: underline;
}

.error-message {
  color: red;
  margin-top: 1rem;
}
</style>
