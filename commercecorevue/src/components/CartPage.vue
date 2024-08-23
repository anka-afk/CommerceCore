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
          src="user-avatar.jpg"
          class="user-avatar"
          @click="goToAccount"
          alt="User Avatar"
        />
      </div>
    </nav>

    <!-- 购物车内容 -->
    <section class="cart-section">
      <h2>购物车</h2>
      <div v-if="cartItems.length > 0" class="cart-container">
        <table class="cart-table">
          <thead>
            <tr>
              <th>商品</th>
              <th>单价</th>
              <th>数量</th>
              <th>小计</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in cartItems" :key="item.id">
              <td class="product-details">
                <img
                  :src="item.product.image"
                  alt="商品图片"
                  class="product-img"
                />
                <span>{{ item.product.product_name }}</span>
              </td>
              <td>{{ item.product.price }} 元</td>
              <td>
                <input
                  type="number"
                  v-model.number="item.quantity"
                  @change="updateQuantity(item)"
                  min="1"
                  class="quantity-input"
                />
              </td>
              <td>{{ item.product.price * item.quantity }} 元</td>
              <td>
                <button class="btn btn-danger" @click="removeItem(item)">
                  移除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="cart-summary">
          <p>总计: {{ cartTotal }} 元</p>
          <button class="btn btn-primary" @click="checkout">结算</button>
        </div>
      </div>
      <div v-else class="empty-cart">
        <p>您的购物车是空的。</p>
        <router-link to="/products" class="btn btn-primary">去购物</router-link>
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
export default {
  data() {
    return {
      cartItems: [], // 购物车商品列表
    };
  },
  computed: {
    cartTotal() {
      return this.cartItems.reduce(
        (total, item) => total + item.product.price * item.quantity,
        0
      );
    },
  },
  methods: {
    fetchCartItems() {
      // 这里可以调用API获取购物车商品列表
      // 模拟数据
      this.cartItems = [
        {
          id: 1,
          product: {
            product_name: "商品1",
            price: 100,
            image: "../assets/product1.png",
          },
          quantity: 2,
        },
        {
          id: 2,
          product: {
            product_name: "商品2",
            price: 200,
            image: "../assets/product2.png",
          },
          quantity: 1,
        },
      ];
    },
    updateQuantity(item) {
      // 更新商品数量的逻辑
      if (item.quantity < 1) {
        item.quantity = 1;
      }
      // 可以在这里发送API请求更新购物车数量
    },
    removeItem(item) {
      // 从购物车中移除商品的逻辑
      this.cartItems = this.cartItems.filter((i) => i.id !== item.id);
      // 可以在这里发送API请求移除商品
    },
    checkout() {
      // 结算的逻辑
      alert("结算成功！");
      // 可以在这里发送API请求进行结算处理
    },
  },
  mounted() {
    this.fetchCartItems(); // 获取购物车商品列表
  },
};
</script>

<style scoped>
/* 购物车内容 */
.cart-section {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  margin: 2rem auto;
  max-width: 1000px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.cart-container {
  overflow-x: auto;
}

.cart-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.cart-table th,
.cart-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.product-details {
  display: flex;
  align-items: center;
}

.product-img {
  width: 50px;
  height: 50px;
  margin-right: 1rem;
}

.quantity-input {
  width: 60px;
  padding: 0.3rem;
  text-align: center;
}

.cart-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.25rem;
}

.cart-summary p {
  margin: 0;
}

.empty-cart {
  text-align: center;
  font-size: 1.5rem;
  color: #777;
}

.empty-cart p {
  margin-bottom: 2rem;
}

.empty-cart .btn {
  font-size: 1rem;
}
</style>

<style scoped>
/* 设置背景图片覆盖整个网页，并固定不动 */
.app-container {
  min-height: 100vh; /* 确保背景覆盖整个页面，包括滚动后部分 */
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
  font-size: 1.5rem; /* 增加字体大小 */
  font-family: "Microsoft Yahei UI light", cursive; /* 示例字体，你可以替换成你喜欢的字体 */
  color: #007bff; /* 文字颜色 */
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* 添加轻微阴影 */
  transition: color 0.3s ease, transform 0.3s ease;
}

.brand-name:hover {
  color: #0056b3; /* 悬停时改变颜色 */
  transform: scale(1.05); /* 悬停时轻微放大 */
}

.navbar-brand {
  font-size: 1.5rem;
  color: #007bff;
}

.navbar-menu {
  display: flex;
  justify-content: space-between;
  align-items: center; /* 确保菜单内元素垂直居中 */
  flex: 1; /* 占满剩余空间 */
}
.nav-links {
  display: flex;
  justify-content: center;
  flex: 1; /* 居中对齐并占据可用空间 */
  gap: 15px; /* 控制链接之间的间距 */
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
.nav-link:hover {
  background: #e0f7e9;
  color: #28a745;
}
.nav-link i {
  margin-right: 0.4rem; /* 缩小图标和文字之间的间距 */
  font-size: 1.1rem; /* 减小图标尺寸 */
}
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
  justify-content: center; /* 水平方向居中 */
  align-items: center; /* 垂直方向居中 */
  padding: 2rem;
  background: transparent; /* 确保背景透明 */
}

/* 容器居中，设置最大宽度 */
.product-container {
  display: flex;
  justify-content: center; /* 子元素水平居中 */
  align-items: center; /* 子元素垂直居中 */
  max-width: 1600px; /* 设置最大宽度以防止过度拉伸 */
  flex-wrap: flex; /* 当内容过多时不换行 */
  gap: 20px; /* 增加卡片之间的间距 */
}

/* 商品卡片容器 */
.product-card-container {
  flex: 0 1 300px; /* 控制卡片宽度并允许换行 */
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
  color: #ffd700; /* 金色 */
  font-size: 1.25rem;
}

/* 滑动控制按钮 */
.slider-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px; /* 增加间距 */
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
}

.container {
  max-width: 1140px;
  margin: 0 auto;
}

/* 模态框 */
.modal-content {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}

/* 动画效果 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter,
.slide-fade-leave-to /* .slide-fade-leave-active for <2.1.8 */ {
  transform: translateX(20px);
  opacity: 0;
}
</style>
