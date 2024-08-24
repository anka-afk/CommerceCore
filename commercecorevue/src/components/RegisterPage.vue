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
        return;
      }

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/api/register/",
          {
            username: this.username,
            password: this.password,
            confirm_password: this.confirmPassword,
            phone_number: this.phone, // 确保字段名称与后端一致
            email: this.email,
          }
        );

        if (response.status === 201) {
          // 注册成功，跳转到登录页面
          this.$router.push("/login");
        } else {
          console.error("注册失败:", response.data);
        }
      } catch (error) {
        console.error(
          "注册失败:",
          error.response ? error.response.data : error.message
        );
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

.navbar-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
}

.nav-links {
  display: flex;
  justify-content: center;
  flex: 1;
  gap: 15px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  color: #333;
  font-size: 0.9rem;
  text-decoration: none;
  transition: background 0.3s, color 0.3s;
  border-radius: 20px;
}

.nav-link:hover,
.nav-link.active {
  background: #e0f7e9;
  color: #28a745;
}

.nav-icon {
  width: 20px;
  height: 20px;
  margin-right: 0.4rem;
}

.btn-contact {
  background: transparent;
  border: 1px solid #007bff;
  padding: 0.5rem 1rem;
  color: #007bff;
  margin-right: 1rem;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}

.btn-contact:hover {
  background: #007bff;
  color: white;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #28a745;
  transition: border 0.3s, transform 0.3s;
}

.user-avatar:hover {
  border-color: #1e7e34;
  transform: scale(1.1);
}

/* 中间块 */
.center-block {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  margin-top: 2rem;
}

.center-content {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  color: #333;
}

.center-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.center-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

/* 产品展示 */
.product-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: transparent;
}

/* 容器居中，设置最大宽度 */
.product-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1600px;
  flex-wrap: flex;
  gap: 20px;
}

/* 商品卡片容器 */
.product-card-container {
  flex: 0 1 300px;
}

/* 商品卡片样式 */
.product-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 10px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 420px;
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transition: transform 0.3s ease-in-out;
}

.card-img-top:hover {
  transform: scale(1.05);
}

.card-title {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

/* 推荐标签的样式 */
.recommended-label {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 0.25rem;
  margin-top: 0.5rem;
}

/* 星星评分样式 */
.product-score {
  margin-bottom: 1rem;
}

.star {
  color: #ffd700;
  font-size: 1.25rem;
}

/* 滑动控制按钮 */
.slider-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.slider-arrow {
  background-color: #007bff;
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  margin: 0 1rem;
}

.slider-arrow:hover {
  background-color: #0056b3;
}

/* 滑动条样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}

.dot {
  width: 10px;
  height: 10px;
  background-color: #ddd;
  border-radius: 50%;
  margin: 0 5px;
  cursor: pointer;
}

.dot.active {
  background-color: #007bff;
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

/* 模态框 */
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
  text-align: center;
  overflow-y: auto;
  max-height: 80vh;
  backdrop-filter: blur(10px);
}

/* 模态框内容图片 */
.modal-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 15px;
}

.modal-details {
  text-align: left;
}

.details-container {
  max-height: 150px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 15px;
}

/* 动画效果 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
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
</style>
