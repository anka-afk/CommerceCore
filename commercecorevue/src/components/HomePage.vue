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

    <!-- 中间块 -->
    <section class="center-block">
      <div class="center-content">
        <h1>欢迎来到隙间小铺</h1>
        <p>支付代价...</p>
        <button class="btn btn-primary btn-lg">立即购物</button>
      </div>
    </section>

    <!-- 产品展示 -->
    <section class="product-section">
      <transition-group name="slide-fade" tag="div" class="product-container">
        <div
          class="product-card-container"
          v-for="product in paginatedProducts[currentPage]"
          :key="product.id"
        >
          <div class="card product-card h-100 shadow-sm">
            <img
              :src="product.image"
              class="card-img-top"
              :alt="product.name"
              @error="handleImageError($event)"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ product.product_name }}</h5>
              <p class="card-text">{{ product.description }}</p>
              <div class="product-score mb-2">
                <span
                  v-for="n in Math.floor(product.score)"
                  :key="n"
                  class="star filled"
                  >★</span
                >
                <span
                  v-for="n in 5 - Math.floor(product.score)"
                  :key="n"
                  class="star"
                  >☆</span
                >
              </div>
              <span v-if="product.suggest" class="recommended-label">推荐</span>
              <button class="btn btn-primary mt-auto">添加到购物车</button>
            </div>
          </div>
        </div>
      </transition-group>
    </section>

    <!-- 滑动控制箭头 -->
    <div class="slider-controls">
      <button class="slider-arrow" @click="prevPage">&lt;</button>
      <div class="pagination">
        <span
          v-for="(page, index) in paginatedProducts.length"
          :key="index"
          class="dot"
          :class="{ active: index === currentPage }"
          @click="goToPage(index)"
        ></span>
      </div>
      <button class="slider-arrow" @click="nextPage">&gt;</button>
    </div>
    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <span>&copy; 2024 anka. 版权所有.</span>
      </div>
    </footer>

    <!-- 联系我们 模态框 -->
    <div
      class="modal fade"
      id="contactModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="contactModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="contactModalLabel">联系我们</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>您可以通过以下方式联系我们：</p>
            <ul>
              <li>电子邮件: support@example.com</li>
              <li>电话: 123-456-7890</li>
            </ul>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";

export default {
  data() {
    return {
      products: [],
      paginatedProducts: [],
      currentPage: 0,
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      axios
        .get("http://127.0.0.1:8000/api/products/")
        .then((response) => {
          this.products = response.data;
          this.prepareProducts();
          nextTick(() => {
            this.startAutoSlide();
          });
        })
        .catch((error) => {
          console.error("Failed to fetch products:", error);
        });
    },
    prepareProducts() {
      const recommendedProducts = this.products.filter((p) => p.recommended);
      const nonRecommendedProducts = this.products.filter(
        (p) => !p.recommended
      );
      const shuffledProducts = [
        ...recommendedProducts,
        ...nonRecommendedProducts.sort(() => 0.5 - Math.random()),
      ];

      this.paginatedProducts = [];
      while (shuffledProducts.length) {
        this.paginatedProducts.push(shuffledProducts.splice(0, 3));
      }
    },
    startAutoSlide() {
      setInterval(() => {
        this.currentPage =
          (this.currentPage + 1) % this.paginatedProducts.length;
      }, 20000); // 每20秒自动滑动一页
    },
    handleImageError(event) {
      event.target.src = "./assets/default.png"; // 使用默认图片路径替换损坏的图片
    },
    prevPage() {
      this.currentPage =
        (this.currentPage - 1 + this.paginatedProducts.length) %
        this.paginatedProducts.length;
    },
    nextPage() {
      this.currentPage = (this.currentPage + 1) % this.paginatedProducts.length;
    },
    goToPage(index) {
      this.currentPage = index;
    },
    openContactModal() {
      this.$refs.contactModal.show();
    },
    goToAccount() {
      this.$router.push("/account");
    },
  },
};
</script>

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
