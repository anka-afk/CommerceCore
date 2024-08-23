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
          :src="avatarUrl"
          class="user-avatar"
          @click="goToAccount"
          alt="User Avatar"
        />
      </div>
    </nav>

    <!-- 搜索和筛选 -->
    <div class="search-filter-container">
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
        v-model="searchTerm"
        placeholder="搜索商品..."
        @input="fetchProducts"
      />
    </div>

    <!-- 产品展示 -->
    <section class="product-section">
      <div v-if="filteredProducts.length === 0">没有找到符合条件的商品。</div>
      <transition-group name="slide-fade" tag="div" class="product-container">
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
              @click="showProductDetails(product)"
              @error="handleImageError($event)"
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ product.product_name }}</h5>
              <p class="card-text">{{ product.description }}</p>
              <div class="product-score mb-2">
                <span v-for="n in product.score" :key="n" class="star filled"
                  >★</span
                >
                <span v-for="n in 5 - product.score" :key="n" class="star"
                  >☆</span
                >
              </div>
              <span v-if="product.suggest" class="recommended-label">推荐</span>
              <p class="price">{{ product.price }} 元</p>
              <button
                class="btn btn-primary mt-auto"
                @click="addToCart(product)"
              >
                添加到购物车
              </button>
              <button
                class="btn btn-secondary mt-2"
                @click="showProductDetails(product)"
              >
                > 查看详情
              </button>
            </div>
          </div>
        </div>
      </transition-group>
    </section>

    <!-- 弹出窗口 -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h3>{{ selectedProduct.product_name }}</h3>
        <img
          :src="selectedProduct.image"
          alt="Product Image"
          class="modal-image"
        />
        <div class="modal-details">
          <p><strong>商品描述:</strong> {{ selectedProduct.description }}</p>
          <p><strong>商品详情:</strong></p>
          <div class="details-container">{{ selectedProduct.details }}</div>
          <p><strong>价格:</strong> {{ selectedProduct.price }} 元</p>
          <p><strong>库存数量:</strong> {{ selectedProduct.stock_quantity }}</p>
          <p><strong>单位:</strong> {{ selectedProduct.unit }}</p>
          <p><strong>销量:</strong> {{ selectedProduct.sales }}</p>
          <p>
            <strong>评分:</strong> {{ selectedProduct.score }} / 5 ({{
              selectedProduct.rating_count
            }}
            人评分)
          </p>
          <p>
            <strong>类别:</strong> {{ selectedProduct.category.category_name }}
          </p>
          <p>
            <strong>上架时间:</strong>
            {{ formatDate(selectedProduct.listing_date) }}
          </p>
          <span v-if="selectedProduct.suggest" class="recommended-label"
            >推荐</span
          >
        </div>
        <button class="btn btn-secondary" @click="closeModal">关闭</button>
      </div>
    </div>

    <!-- 滑动控制箭头 -->
    <div class="slider-controls">
      <button
        class="slider-arrow"
        @click="prevPage"
        :disabled="currentPage === 1"
      >
        &lt; 上一页
      </button>
      <div class="pagination">
        第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
      </div>
      <button
        class="slider-arrow"
        @click="nextPage"
        :disabled="currentPage === totalPages"
      >
        下一页 &gt;
      </button>
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
      products: [],
      categories: [],
      searchTerm: "",
      selectedCategory: "",
      currentPage: 1,
      itemsPerPage: 9,
      mediaUrl: "http://localhost:8000",
      userProfile: null,
      avatarUrl: null,
      showModal: false, // 控制模态框显示
      selectedProduct: null, // 当前选中的商品
    };
  },
  computed: {
    filteredProducts() {
      let filtered = this.products;
      if (this.selectedCategory) {
        filtered = filtered.filter(
          (product) => product.category === parseInt(this.selectedCategory)
        );
      }
      if (this.searchTerm) {
        filtered = filtered.filter((product) =>
          product.product_name.includes(this.searchTerm)
        );
      }
      return filtered;
    },
    totalPages() {
      return Math.ceil(this.filteredProducts.length / this.itemsPerPage);
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredProducts.slice(start, end);
    },
  },
  mounted() {
    this.fetchCategories();
    this.fetchProducts();
    this.fetchUserProfile(); // 添加获取用户信息的方法
  },
  methods: {
    fetchProducts() {
      axios
        .get("http://127.0.0.1:8000/api/products/")
        .then((response) => {
          this.products = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch products:", error);
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
    fetchCategories() {
      // 调用后端获取分类数据的API
      axios
        .get("http://127.0.0.1:8000/api/categories/") // 需要确保后端API存在这个endpoint
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch categories:", error);
        });
    },
    handleImageError(event) {
      event.target.src = "./assets/default.png"; // 使用默认图片路径替换损坏的图片
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    addToCart(product) {
      axios
        .post("http://127.0.0.1:8000/api/cart/add_item/", {
          product_id: product.product_id,
          quantity: 1, // 默认添加一件商品到购物车
        })
        .then(() => {
          alert("商品已添加到购物车");
        })
        .catch((error) => {
          console.error("Failed to add item to cart:", error);
          alert("添加到购物车失败");
        });
    },
    showProductDetails(product) {
      this.selectedProduct = product;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedProduct = null;
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    goToAccount() {
      this.$router.push("/account");
    },
  },
};
</script>

<style scoped>
/* 搜索和筛选容器样式 */
.search-filter-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.search-filter-container select,
.search-filter-container input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* 添加产品价格样式 */
.price {
  font-size: 1.2rem;
  color: #28a745;
  margin-bottom: 1rem;
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

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* 深色背景遮罩 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: rgba(255, 255, 255, 0.9); /* 半透明白色背景 */
  backdrop-filter: blur(20px); /* 毛玻璃效果 */
  border-radius: 15px; /* 圆角 */
  padding: 30px; /* 内边距 */
  max-width: 90%; /* 最大宽度为90% */
  max-height: 90%; /* 最大高度为90% */
  width: auto; /* 宽度根据内容调整 */
  height: auto; /* 高度根据内容调整 */
  text-align: center;
  box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.3); /* 阴影效果 */
  overflow-y: auto; /* 垂直方向滚动条 */
  overflow-x: hidden; /* 禁止水平方向滚动条 */
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

.modal-content.show {
  transform: translateY(0); /* 显示时恢复位置 */
}

.modal-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 20px;
  border-radius: 10px; /* 圆角图片 */
}

.modal-details {
  text-align: left;
  color: #333; /* 深色文字 */
}

.details-container {
  max-height: 200px; /* 最大高度200px */
  overflow-y: auto; /* 保持垂直滚动条 */
  padding: 15px;
  border: 1px solid rgba(0, 0, 0, 0.1); /* 边框 */
  border-radius: 10px;
  margin-bottom: 20px;
  background: rgba(255, 255, 255, 0.5); /* 半透明背景 */
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

.modal-content button {
  margin-top: 15px;
  padding: 10px 20px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s ease;
}

.modal-content button:hover {
  background: #218838; /* 按钮悬停效果 */
}

/* 动画效果 */
.modal-overlay-enter-active,
.modal-overlay-leave-active {
  opacity: 1;
  transition: opacity 0.3s ease;
}

.modal-overlay-enter,
.modal-overlay-leave-to {
  opacity: 0;
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
  flex-wrap: wrap; /* 允许换行，使产品在多行展示 */
  justify-content: center; /* 子元素水平居中 */
  align-items: flex-start; /* 子元素顶部对齐 */
  max-width: 1200px; /* 根据需要调整最大宽度 */
  gap: 20px; /* 增加卡片之间的间距 */
  margin: 0 auto; /* 居中对齐 */
}

/* 商品卡片容器 */
.product-card-container {
  flex: 0 1 calc(33.333% - 20px); /* 每行展示3个卡片，减去间距 */
  box-sizing: border-box; /* 确保 padding 和 border 不影响宽度计算 */
  margin-bottom: 20px; /* 控制每行卡片之间的垂直间距 */
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
  justify-content: space-between; /* 保证按钮始终在底部 */
  min-height: 460px; /* 确保所有卡片最小高度一致 */
}

.card-body {
  flex-grow: 1; /* 使卡片主体部分填充剩余空间 */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 使卡片内容分布均匀 */
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
  margin-top: auto; /* 确保页脚始终位于页面底部 */
}

.container {
  max-width: 1140px;
  margin: 0 auto;
}

/* 模态框样式 */
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
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.modal-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 15px;
}

.modal-content button {
  margin-top: 10px;
  display: block;
  width: 100%;
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

@media (max-width: 1200px) {
  .product-card-container {
    flex: 0 1 calc(50% - 20px); /* 在中等屏幕上每行展示2个卡片 */
  }
}

@media (max-width: 768px) {
  .product-card-container {
    flex: 0 1 calc(100% - 20px); /* 在小屏幕上每行展示1个卡片 */
  }
}
</style>
