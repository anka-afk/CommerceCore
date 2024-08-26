<template>
  <BaseTemplate v-if="product">
    <section class="product-detail-section">
      <button class="btn-back" @click="goBack">返回上一页</button>

      <div class="product-container">
        <img :src="product.image" alt="Product Image" class="product-image" />
        <div class="product-info">
          <h2>{{ product.product_name }}</h2>
          <p>价格: ¥{{ product.price }}</p>
          <p>单位: {{ product.unit }}</p>
          <p>库存: {{ product.stock_quantity }}</p>
          <p>点击量: {{ product.click }}</p>
          <p v-if="product.category">
            类别: {{ product.category.category_name }}
          </p>
          <p>上架时间: {{ formatDate(product.listing_date) }}</p>
          <p>销量: {{ product.sales }}</p>
          <p v-if="product.suggest" class="recommended-label">推荐</p>
          <p>评分: {{ product.score }} ({{ product.rating_count }} 人评分)</p>
          <button class="btn-favorite" @click="addToFavorites">收藏</button>
        </div>
      </div>

      <div class="product-details">
        <h3>商品详情</h3>
        <div class="details-container">{{ product.details }}</div>
      </div>

      <div class="comments-section">
        <h3>用户评论</h3>
        <div v-if="product.comments && product.comments.length > 0">
          <div
            v-for="comment in product.comments"
            :key="comment.id"
            class="comment-card"
          >
            <div class="comment-header">
              <strong>{{ comment.user }}</strong>
              <span class="comment-rating">评分: {{ comment.rating }}星</span>
            </div>
            <p>{{ comment.text }}</p>
            <p class="comment-date">
              评论时间: {{ formatDate(comment.created_at) }}
            </p>
          </div>
        </div>
        <div v-else>
          <p>还没有评论，快来留下您的第一条评论吧！</p>
        </div>
      </div>
    </section>
  </BaseTemplate>
  <div v-else>加载中...</div>
</template>

<script>
import axios from "axios";
import BaseTemplate from "./BaseTemplate.vue";

export default {
  components: { BaseTemplate },
  data() {
    return {
      product: null, // 初始化为 null
      user: null, // 用于存储用户信息
    };
  },
  mounted() {
    this.fetchUserInfo(); // 在挂载时获取用户信息
    this.fetchProductDetails(); // 获取产品详情
  },
  methods: {
    fetchProductDetails() {
      const productId = this.$route.params.id; // 从路由获取产品ID
      axios
        .get(`http://localhost:8000/api/products/${productId}/`)
        .then((response) => {
          this.product = response.data;
          this.recordBrowsingHistory(); // 记录浏览历史
        })
        .catch((error) => {
          console.error("Failed to fetch product details:", error);
        });
    },

    fetchUserInfo() {
      axios
        .get("http://localhost:8000/api/user/profile/")
        .then((response) => {
          this.user = response.data; // 存储用户信息
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    },

    recordBrowsingHistory() {
      if (this.user && this.product) {
        axios
          .post("http://localhost:8000/api/browsing-history/record/", {
            product: this.product.product_id, // 传递产品ID
          })
          .then(() => {
            console.log("Browsing history recorded successfully.");
          })
          .catch((error) => {
            console.error("Failed to record browsing history:", error);
          });
      }
    },

    goBack() {
      this.$router.go(-1);
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    addToFavorites() {
      axios
        .post("http://localhost:8000/api/favorite-items/add_item/", {
          product_id: this.product.product_id, // 确保字段名称与后端一致
        })
        .then(() => {
          alert("商品已添加到收藏夹");
        })
        .catch((error) => {
          console.error("Failed to add product to favorites:", error);
          alert("添加到收藏夹失败");
        });
    },
  },
};
</script>

<style scoped>
/* 样式部分保持不变 */
.product-detail-section {
  padding: 2rem;
}

.product-container {
  display: flex;
  gap: 2rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 10px;
}

.product-image {
  width: 300px;
  height: 300px;
  object-fit: cover;
  border-radius: 10px;
}

.product-info {
  flex-grow: 1;
}

.product-details {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 10px;
}

.details-container {
  max-height: 200px;
  overflow-y: auto;
}

.comments-section {
  margin-top: 2rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 10px;
}

.comment-card {
  margin-bottom: 1.5rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
}

.comment-date {
  color: gray;
  font-size: 0.9rem;
}

.btn-back {
  display: inline-block;
  margin-bottom: 1.5rem;
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-back:hover {
  background: #0056b3;
}

.btn-favorite {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-favorite:hover {
  background: #e68900;
}
</style>
