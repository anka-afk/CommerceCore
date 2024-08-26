<template>
  <BaseTemplate>
    <!-- 搜索和筛选 -->
    <div class="search-filter-container">
      <select
        v-model="selectedCategory"
        @change="fetchProducts"
        class="glass-select"
      >
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
        class="glass-input"
      />
      <select v-model="sortOption" @change="fetchProducts" class="glass-select">
        <option value="click">按点击量排序</option>
        <option value="name">按名称排序</option>
        <option value="price">按价格排序</option>
        <option value="stock">按库存数量排序</option>
        <option value="listing_date">按上架时间排序</option>
        <option value="score">按评分排序</option>
      </select>
      <select v-model="sortOrder" @change="fetchProducts" class="glass-select">
        <option value="asc">升序</option>
        <option value="desc">降序</option>
      </select>
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
              @click="showProductDetails1(product)"
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
                查看详情
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
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import BaseTemplate from "./BaseTemplate.vue";

export default {
  data() {
    return {
      products: [],
      categories: [],
      searchTerm: "",
      selectedCategory: "",
      currentPage: 1,
      itemsPerPage: 16, // 每页显示16个物品
      mediaUrl: "http://localhost:8000",
      showModal: false,
      selectedProduct: null,
      sortOption: "click",
      sortOrder: "asc",
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

      // 根据选择的排序选项和排序方式排序产品
      filtered.sort((a, b) => {
        let result = 0;
        switch (this.sortOption) {
          case "click":
            result = b.click - a.click;
            break;
          case "name":
            result = a.product_name.localeCompare(b.product_name);
            break;
          case "price":
            result = a.price - b.price;
            break;
          case "stock":
            result = b.stock_quantity - a.stock_quantity;
            break;
          case "listing_date":
            result = new Date(b.listing_date) - new Date(a.listing_date);
            break;
          case "score":
            result = b.score - a.score;
            break;
        }
        return this.sortOrder === "asc" ? result : -result;
      });

      return filtered;
    },
    totalPages() {
      return Math.ceil(this.filteredProducts.length / this.itemsPerPage);
    },
    paginatedProducts() {
      const start = Math.max((this.currentPage - 1) * this.itemsPerPage, 0);
      const end = Math.min(
        start + this.itemsPerPage,
        this.filteredProducts.length
      );
      return this.filteredProducts.slice(start, end);
    },
  },
  mounted() {
    this.fetchCategories();
    this.fetchProducts();
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

    fetchCategories() {
      axios
        .get("http://127.0.0.1:8000/api/categories/")
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch categories:", error);
        });
    },
    handleImageError(event) {
      event.target.src = "./assets/default.png";
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
          quantity: 1,
        })
        .then(() => {
          alert("商品已添加到购物车");
        })
        .catch((error) => {
          console.error("Failed to add item to cart:", error);
          alert("添加到购物车失败");
        });
    },
    showProductDetails1(product) {
      if (product && !product.empty) {
        // 确保空元素不会触发模态框
        this.selectedProduct = product;
        this.showModal = true;
      }
    },
    closeModal() {
      this.showModal = false;
      this.selectedProduct = null;
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    showProductDetails(product) {
      this.$router.push({
        name: "ProductDetail",
        params: { id: product.product_id },
      });
    },
  },
  components: { BaseTemplate },
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

/* 胶囊型搜索框和筛选框 */
.glass-input,
.glass-select {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #333;
  font-size: 1rem;
  transition: box-shadow 0.3s ease-in-out;
}

.glass-input::placeholder {
  color: #aaa;
}

.glass-input:focus,
.glass-select:focus {
  outline: none;
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
}

/* 添加产品价格样式 */
.price {
  font-size: 1.2rem;
  color: #28a745;
  margin-bottom: 1rem;
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

/* 容器居中，设置最大宽度 */
.product-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4列布局 */
  grid-gap: 20px;
  max-width: 1200px;
  margin: 0 auto; /* 居中对齐 */
}

.product-card-container {
  height: 100%; /* 使卡片容器高度自适应 */
  display: flex;
  justify-content: center;
  align-items: center;
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

/* 产品展示 */
.product-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: transparent;
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

.product-card-container.empty {
  visibility: hidden; /* 隐藏空元素 */
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
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  margin: 0 1rem;
  font-size: 1.25rem;
}

.slider-arrow:disabled {
  background-color: #ddd; /* 禁用按钮颜色 */
}

.slider-arrow:hover:enabled {
  background-color: #0056b3;
}
/* 滑动条样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 1rem;
}

.pagination span {
  font-size: 1.25rem;
  margin: 0 0.5rem;
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
</style>
