<template>
  <BaseTemplate>
    <!-- 中间块 -->
    <section class="center-block">
      <div class="center-content">
        <h1>欢迎来到隙间小铺</h1>
        <p>支付代价...</p>
        <button class="btn btn-primary btn-lg" @click="goToStore">
          前往商店
        </button>
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
          <div
            class="card product-card h-100 shadow-sm"
            @click="showProductDetails(product)"
          >
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
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import { nextTick } from "vue";
import BaseTemplate from "./BaseTemplate.vue";

export default {
  data() {
    return {
      products: [],
      paginatedProducts: [],
      currentPage: 0,
      mediaUrl: "http://localhost:8000", // 将其设置为你的后端基础 URL，省略 /media/
      showModal: false, // 控制模态框显示
      selectedProduct: null, // 当前选中的商品
      showDropdown: false,
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    goToStore() {
      this.$router.push("/products");
    },
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
  },
  components: { BaseTemplate },
};
</script>

<style scoped>
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
</style>
