<template>
  <div class="app-container">
    <nav class="navbar glass-navbar">
      <a class="navbar-brand" href="#">
        <img src="../assets/logo.png" alt="隙间小铺" class="navbar-logo" />
        <span class="brand-name">隙间小铺</span>
      </a>
      <div class="navbar-menu">
        <div class="nav-links">
          <router-link class="nav-link" to="/home" exact-active-class="active">
            <img src="../assets/Home.png" class="nav-icon" /> 首页
          </router-link>
          <router-link
            class="nav-link"
            to="/products"
            exact-active-class="active"
          >
            <img src="../assets/store.png" class="nav-icon" /> 商店
          </router-link>
          <router-link class="nav-link" to="/cart" exact-active-class="active">
            <img src="../assets/cart.png" class="nav-icon" /> 购物车
          </router-link>
          <router-link
            class="nav-link"
            to="/favorites"
            exact-active-class="active"
          >
            <img src="../assets/favorite.png" class="nav-icon" /> 收藏
          </router-link>
          <router-link class="nav-link" to="/help" exact-active-class="active">
            <img src="../assets/help.png" class="nav-icon" /> 帮助
          </router-link>
          <router-link
            class="nav-link"
            to="/settings"
            exact-active-class="active"
          >
            <img src="../assets/settings.png" class="nav-icon" /> 设置
          </router-link>
          <router-link
            class="nav-link"
            to="/notifications"
            exact-active-class="active"
          >
            <img src="../assets/notifications.png" class="nav-icon" /> 公告
          </router-link>
        </div>
        <img
          :src="avatarUrl"
          class="user-avatar"
          @click="goToAccount"
          alt="User Avatar"
        />
      </div>
    </nav>

    <section class="favorite-section">
      <h2>我的收藏夹</h2>
      <div v-if="favorites && favorites.length > 0" class="favorite-container">
        <div class="favorite-item" v-for="item in favorites" :key="item.id">
          <img :src="item.product.image" alt="Product Image" />
          <h3>{{ item.product.product_name }}</h3>
          <p>{{ item.product.description }}</p>
          <p>收藏时间: {{ formatDate(item.created_at) }}</p>
          <button class="btn btn-danger" @click="removeFromFavorites(item.id)">
            移除
          </button>
        </div>
      </div>
      <div v-else>
        <p>您的收藏夹为空。</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      favorites: [], // 初始化为空数组
      mediaUrl: "http://localhost:8000",
      userProfile: null,
      avatarUrl: null,
    };
  },
  mounted() {
    this.fetchFavorites();
    this.fetchUserProfile(); // 添加获取用户信息的方法
  },
  methods: {
    fetchUserProfile() {
      axios
        .get("http://localhost:8000/api/user/profile/")
        .then((response) => {
          this.userProfile = response.data.profile; // 假设返回的数据中包含用户profile信息
          this.avatarUrl = `${this.mediaUrl}${this.userProfile.avatar}`;
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    },
    goToAccount() {
      this.$router.push("/account");
    },
    fetchFavorites() {
      axios
        .get("http://127.0.0.1:8000/api/favorites/")
        .then((response) => {
          this.favorites = response.data.items || []; // 确保 items 存在
        })
        .catch((error) => {
          console.error("Failed to fetch favorites:", error);
        });
    },
    removeFromFavorites(itemId) {
      axios
        .delete(`http://127.0.0.1:8000/api/favorite-items/${itemId}/`)
        .then(() => {
          this.fetchFavorites();
        })
        .catch((error) => {
          console.error("Failed to remove favorite item:", error);
        });
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
/* 样式与其他组件保持一致 */
.favorite-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  max-width: 800px;
  margin: 20px auto;
}

.favorite-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.favorite-item {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 200px;
  text-align: center;
}

.favorite-item img {
  max-width: 100%;
  border-radius: 10px;
}

.favorite-item h3 {
  font-size: 1.25rem;
  margin: 10px 0;
}

.favorite-item p {
  font-size: 0.9rem;
  color: #555;
}

.favorite-item .btn-danger {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.favorite-item .btn-danger:hover {
  background-color: #c82333;
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
</style>
