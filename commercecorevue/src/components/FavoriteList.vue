<template>
  <BaseTemplate>
    <section class="favorite-section">
      <h2>我的收藏夹</h2>
      <div v-if="favorites && favorites.length > 0" class="favorite-container">
        <div class="favorite-item" v-for="item in favorites" :key="item.id">
          <!-- 绑定点击事件到图片 -->
          <img
            :src="item.product.image"
            alt="Product Image"
            class="favorite-item-image"
            @click="goToProductDetail(item.product.product_id)"
          />
          <h3>{{ item.product.product_name }}</h3>
          <p>{{ item.product.description }}</p>
          <p>收藏时间: {{ formatDate(item.created_at) }}</p>
          <div class="button-group">
            <button
              class="btn btn-success"
              @click="addToCart(item.product.product_id)"
            >
              添加到购物车
            </button>
            <button
              class="btn btn-danger"
              @click="removeFromFavorites(item.id)"
            >
              移除
            </button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>您的收藏夹为空。</p>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import BaseTemplate from "./BaseTemplate.vue";

export default {
  data() {
    return {
      favorites: [], // 初始化为空数组
      mediaUrl: "http://localhost:8000", // 将其设置为你的后端基础 URL，省略 /media/
    };
  },
  mounted() {
    this.fetchFavorites();
  },
  methods: {
    fetchFavorites() {
      axios
        .get("http://127.0.0.1:8000/api/favorite-items/")
        .then((response) => {
          this.favorites = response.data || []; // 确保返回的数据正确
        })
        .catch((error) => {
          console.error("Failed to fetch favorites:", error);
        });
    },
    removeFromFavorites(itemId) {
      axios
        .delete(`http://127.0.0.1:8000/api/favorite-items/${itemId}/`)
        .then(() => {
          this.fetchFavorites(); // 移除后重新加载收藏夹
        })
        .catch((error) => {
          console.error("Failed to remove favorite item:", error);
        });
    },
    addToCart(productId) {
      axios
        .post("http://127.0.0.1:8000/api/cart/add_item/", {
          product_id: productId,
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
    goToProductDetail(productId) {
      // 使用 Vue Router 导航到商品详情页
      this.$router.push({ name: "ProductDetail", params: { id: productId } });
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
.favorite-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.2); /* 增加毛玻璃效果 */
  backdrop-filter: blur(10px);
  border-radius: 10px;
  max-width: 1000px;
  margin: 20px auto;
}

.favorite-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.favorite-item {
  background: rgba(255, 255, 255, 0.9); /* 增加毛玻璃效果 */
  backdrop-filter: blur(5px);
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 200px;
  text-align: center;
  cursor: pointer; /* 增加手型指针，提示图片可点击 */
}

.favorite-item-image {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
}

.favorite-item h3 {
  font-size: 1.25rem;
  margin: 10px 0;
}

.favorite-item p {
  font-size: 0.9rem;
  color: #555;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.favorite-item .btn-success {
  background-color: #28a745;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.favorite-item .btn-success:hover {
  background-color: #218838;
}

.favorite-item .btn-danger {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.favorite-item .btn-danger:hover {
  background-color: #c82333;
}
</style>
