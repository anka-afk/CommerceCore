<template>
  <div class="app-container">
    <!-- 导航栏 -->
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
          :src="avatarUrl || 'default-avatar.jpg'"
          class="user-avatar"
          @click="goToAccount"
          alt="User Avatar"
        />
      </div>
    </nav>

    <!-- 购物车内容 -->
    <section class="cart-section">
      <h2>您的购物车</h2>
      <div v-if="cartItems.length === 0">您的购物车是空的。</div>
      <div v-else class="cart-items-container">
        <div
          class="cart-item-card"
          v-for="item in cartItems"
          :key="item.product.product_id"
        >
          <div class="cart-item-content">
            <!-- 修改图片的 src 绑定 -->
            <img
              :src="`${mediaUrl}${item.product.image}`"
              alt="商品图片"
              class="cart-item-image"
            />
            <div class="cart-item-details">
              <h4 class="cart-item-name">{{ item.product.product_name }}</h4>
              <p>单价: {{ item.product.price }} 元</p>
              <p>
                数量:
                <button @click="decreaseQuantity(item)">-</button>
                <span>{{ item.quantity }}</span>
                <button @click="increaseQuantity(item)">+</button>
              </p>
              <p>
                总计: {{ (item.product.price * item.quantity).toFixed(2) }} 元
              </p>
              <button class="btn btn-danger" @click="removeFromCart(item)">
                移除
              </button>
            </div>
          </div>
        </div>
        <div class="cart-summary">
          <p>总金额: {{ totalAmount.toFixed(2) }} 元</p>
          <button class="btn btn-primary" @click="checkout">结算</button>
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
      cartItems: [],
      mediaUrl: "http://localhost:8000", // 将其设置为你的后端基础 URL，省略 /media/
      userProfile: null, // 用户信息对象
      avatarUrl: null, // 头像URL
    };
  },
  computed: {
    totalAmount() {
      return this.cartItems.reduce(
        (total, item) => total + item.product.price * item.quantity,
        0
      );
    },
  },
  mounted() {
    this.fetchCartItems();
    this.fetchUserProfile(); // 添加获取用户信息的方法
  },
  methods: {
    fetchCartItems() {
      axios
        .get("http://127.0.0.1:8000/api/cart/")
        .then((response) => {
          this.cartItems = response.data.items;
        })
        .catch((error) => {
          console.error("Failed to fetch cart items:", error);
        });
    },
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
    increaseQuantity(item) {
      axios
        .post("http://127.0.0.1:8000/api/cart/update_quantity/", {
          product_id: item.product.product_id,
          quantity: item.quantity + 1,
        })
        .then(() => {
          item.quantity++;
        })
        .catch((error) => {
          console.error("Failed to update quantity:", error);
        });
    },
    decreaseQuantity(item) {
      if (item.quantity > 1) {
        axios
          .post("http://127.0.0.1:8000/api/cart/update_quantity/", {
            product_id: item.product.product_id,
            quantity: item.quantity - 1,
          })
          .then(() => {
            item.quantity--;
          })
          .catch((error) => {
            console.error("Failed to update quantity:", error);
          });
      }
    },
    removeFromCart(item) {
      axios
        .post("http://127.0.0.1:8000/api/cart/remove_item/", {
          product_id: item.product.product_id,
        })
        .then(() => {
          this.cartItems = this.cartItems.filter(
            (cartItem) =>
              cartItem.product.product_id !== item.product.product_id
          );
        })
        .catch((error) => {
          console.error("Failed to remove item from cart:", error);
        });
    },
    checkout() {
      alert("结算功能暂未实现"); // 结算逻辑根据需要实现
    },
    goToAccount() {
      this.$router.push("/account");
    },
  },
};
</script>
<style scoped>
/* 通用容器样式 */
.container {
  max-width: 1140px;
  margin: 0 auto;
}

/* 设置背景图片覆盖整个网页，并固定不动 */
.app-container {
  min-height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
}

/* 毛玻璃效果的通用样式 */
.glass-effect {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
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
  @extend .glass-effect;
  padding: 2rem;
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

/* 购物车样式 */
.cart-items-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cart-section {
  @extend .glass-effect;
  padding: 2rem;
  max-width: 1200px;
  margin: 2rem auto;
}

.cart-item-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(5px);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 600px;
}

.cart-item-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.cart-item {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.7);
  padding: 10px;
  border-radius: 10px;
}

.cart-item-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
  margin-right: 1rem;
}

.cart-item-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cart-item-name {
  font-size: 1.2rem;
  font-weight: bold;
}

.cart-item-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.cart-item-actions button {
  padding: 5px 10px;
  border: 1px solid #ccc;
  background-color: #fff;
  cursor: pointer;
  transition: background 0.3s;
}

.cart-item-actions button:hover {
  background-color: #f0f0f0;
}

.cart-item-price {
  margin-top: 10px;
  font-weight: bold;
}

.cart-summary {
  margin-top: 2rem;
  text-align: right;
  font-size: 1.5rem;
  font-weight: bold;
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

.product-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1600px;
  flex-wrap: flex;
  gap: 20px;
}

.product-card-container {
  flex: 0 1 300px;
}

.product-card {
  @extend .glass-effect;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
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
  @extend .glass-effect;
  padding: 20px;
  max-width: 600px;
  width: 100%;
  text-align: center;
  overflow-y: auto;
  max-height: 80vh;
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
