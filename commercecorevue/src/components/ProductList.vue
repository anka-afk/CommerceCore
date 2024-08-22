<template>
  <div class="container mt-5">
    <h1 class="mb-4 text-center">我们的产品</h1>
    <div class="row">
      <div class="col-md-4 mb-4" v-for="product in products" :key="product.id">
        <div class="card h-100 shadow-sm">
          <img
            :src="product.image"
            class="card-img-top"
            :alt="product.product_name"
          />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ product.product_name }}</h5>
            <p class="card-text text-muted">¥{{ product.price }}</p>
            <p class="card-text">{{ product.description }}</p>
            <!-- 推荐产品标签 -->
            <span v-if="product.suggest" class="badge bg-success mb-2"
              >推荐</span
            >
            <!-- 添加产品评分（模拟） -->
            <div class="mb-2">
              <span class="text-warning"
                >&#9733;&#9733;&#9733;&#9734;&#9734;</span
              >
              <span class="text-muted">(10)</span>
            </div>
            <!-- 添加一个自定义的“加入购物车”按钮 -->
            <button class="btn btn-outline-primary mt-auto">加入购物车</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      products: [],
      error: "",
    };
  },
  created() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/products/",
          {
            headers: {
              Authorization: `Token ${token}`, // 这里携带了Token
            },
          }
        );
        this.products = response.data;
      } catch (error) {
        console.error("Failed to fetch products:", error);
        this.error = "无法加载产品列表，请重试";
      }
    },
  },
};
</script>

<style scoped>
/* 提升整体布局的外观 */
.card {
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.card-title {
  font-weight: bold;
  color: #343a40;
}

.card-text {
  margin-bottom: 1rem;
}

.btn-outline-primary {
  border-radius: 50px;
}

.badge {
  font-size: 0.8rem;
}
</style>
