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

    <!-- 商店内容 -->
    <section class="shop-section">
      <div class="filters">
        <select v-model="selectedCategory" @change="fetchProducts">
          <option value="">所有分类</option>
          <option
            v-for="category in categories"
            :key="category.id"
            :value="category.id"
          >
            {{ category.category_name }}
          </option>
        </select>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜索商品..."
          @input="fetchProducts"
        />
      </div>

      <div class="shop-container">
        <div
          class="product-card-container"
          v-for="product in paginatedProducts"
          :key="product.product_id"
        >
          <div class="card product-card h-100 shadow-sm">
            <img
              :src="product.image"
              class="card-img-top"
              :alt="product.product_name"
              @error="handleImageError($event)"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ product.product_name }}</h5>
              <p class="card-text">{{ product.description }}</p>
              <p class="product-price">{{ product.price }} 元</p>
              <div class="mt-auto">
                <button class="btn btn-primary" @click="addToCart(product)">
                  加入购物车
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页控制 -->
      <div class="pagination-controls">
        <button
          class="btn-pagination"
          @click="prevPage"
          :disabled="currentPage === 0"
        >
          &lt; 上一页
        </button>
        <span>第 {{ currentPage + 1 }} 页 / 共 {{ totalPages }} 页</span>
        <button
          class="btn-pagination"
          @click="nextPage"
          :disabled="currentPage === totalPages - 1"
        >
          下一页 &gt;
        </button>
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
      products: [], // 商品列表
      categories: [], // 分类列表
      selectedCategory: "", // 选中的分类
      searchQuery: "", // 搜索关键词
      currentPage: 0, // 当前页面
      itemsPerPage: 9, // 每页显示商品数量
    };
  },
  computed: {
    paginatedProducts() {
      const start = this.currentPage * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.products.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.products.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchProducts() {
      const params = {
        category: this.selectedCategory,
        search: this.searchQuery,
      };

      try {
        const response = await axios.get("/api/products/", { params });
        this.products = response.data;
      } catch (error) {
        console.error("Failed to fetch products:", error);
      }
    },
    async fetchCategories() {
      try {
        const response = await axios.get("/api/categories/");
        this.categories = response.data;
      } catch (error) {
        console.error("Failed to fetch categories:", error);
      }
    },
    addToCart(product) {
      // 添加商品到购物车的逻辑
      alert(`已将 ${product.product_name} 加入购物车`);
      // 可以在这里发送API请求添加商品到购物车
    },
    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages - 1) {
        this.currentPage++;
      }
    },
    handleImageError(event) {
      event.target.src = "./assets/default.png"; // 使用默认图片路径替换损坏的图片
    },
  },
  mounted() {
    this.fetchCategories(); // 获取分类列表
    this.fetchProducts(); // 获取商品列表
  },
};
</script>

<style scoped>
/* 商店内容 */
.shop-section {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  margin: 2rem auto;
  max-width: 1200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.shop-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 20px;
}

.product-card-container {
  flex: 0 1 calc(33.333% - 20px); /* 每行显示3个卡片，卡片之间有间距 */
}

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

.product-price {
  font-size: 1.25rem;
  font-weight: bold;
  color: #28a745;
  margin-top: 0.5rem;
}

.btn-primary {
  background-color: #28a745;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  text-align: center;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #218838;
}

/* 分页控制 */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.btn-pagination {
  background-color: #007bff;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.btn-pagination:disabled {
  background-color: #c0c0c0;
  cursor: not-allowed;
}

.btn-pagination:hover:enabled {
  background-color: #0056b3;
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
