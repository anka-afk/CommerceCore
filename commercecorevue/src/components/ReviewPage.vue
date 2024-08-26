<template>
  <BaseTemplate>
    <section class="review-section">
      <h2>商品评价</h2>
      <div v-if="product" class="product-info glass-card">
        <img :src="product.image" alt="商品图片" class="product-image" />
        <div class="product-details">
          <h3>{{ product.product_name }}</h3>
          <p>{{ product.description }}</p>
          <p><strong>价格：</strong>{{ product.price }} 元</p>
          <p><strong>库存：</strong>{{ product.stock_quantity }}</p>
        </div>
      </div>
      <div v-if="product" class="review-form glass-card">
        <h4>为该商品留下评价：</h4>
        <form @submit.prevent="submitReview">
          <div class="form-group">
            <label for="rating">评分 (1-5):</label>
            <input
              type="number"
              id="rating"
              v-model="review.rating"
              min="1"
              max="5"
              required
            />
          </div>
          <div class="form-group">
            <label for="comment">评论:</label>
            <textarea
              id="comment"
              v-model="review.comment"
              rows="5"
              required
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">提交评价</button>
        </form>
      </div>
      <div v-else>
        <p>加载商品信息时出错，请稍后再试。</p>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      product: null, // 用于存储商品信息
      review: {
        rating: 0,
        comment: "",
      },
      userProfile: null, // 修改为 null 初始值
    };
  },
  mounted() {
    this.fetchUserProfile();
    this.fetchProductDetails();
  },
  methods: {
    fetchUserProfile() {
      axios
        .get("http://localhost:8000/api/user/profile/")
        .then((response) => {
          this.userProfile = response.data.profile; // 假设返回的数据中包含用户profile信息
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    },
    fetchProductDetails() {
      const productId = this.$route.params.productId;
      if (productId) {
        axios
          .get(`http://localhost:8000/api/products/${productId}/`)
          .then((response) => {
            this.product = response.data;
          })
          .catch((error) => {
            console.error("Failed to fetch product details:", error);
          });
      } else {
        console.error("Product ID is missing from the route params.");
      }
    },
    submitReview() {
      if (!this.product) {
        console.error("Product information is missing.");
        return;
      }

      const productId = this.product.product_id;

      axios
        .post("http://localhost:8000/api/comments/", {
          product: productId,
          text: this.review.comment,
          rating: this.review.rating,
        })
        .then(() => {
          alert("评价提交成功！");
          this.$router.push("/orders");
        })
        .catch((error) => {
          console.error("Failed to submit review:", error);
        });
    },
  },
};
</script>

<style scoped>
.review-section {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.product-info {
  display: flex;
  gap: 1rem;
}

.product-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.product-details {
  flex: 1;
}

.review-form {
  padding: 1.5rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
