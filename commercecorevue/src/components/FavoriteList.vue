<template>
  <BaseTemplate>
    <section class="favorite-section">
      <h2>我的收藏夹</h2>
      <div v-if="favorites && favorites.length > 0" class="favorite-container">
        <div class="favorite-item" v-for="item in favorites" :key="item.id">
          <img :src="item.product.image" alt="Product Image" />
          <h3>{{ item.product.product_name }}</h3>
          <p>{{ item.product.description }}</p>
          <p>收藏时间: {{ formatDate(item.created_at) }}</p>
          <button class="btn btn-danger" @click="removeFromFavorites(item.id)">
            移除
          </button>
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
      mediaUrl: "http://localhost:8000",
    };
  },
  mounted() {
    this.fetchFavorites();
  },
  methods: {
    fetchFavorites() {
      axios
        .get("http://127.0.0.1:8000/api/favorites/")
        .then((response) => {
          this.favorites = response.data.items || []; // 确保 items 存在
        })
        .catch((error) => {
          console.error("Failed to fetch favorites:", error);
        });
    },
    removeFromFavorites(itemId) {
      axios
        .delete(`http://127.0.0.1:8000/api/favorite-items/${itemId}/`)
        .then(() => {
          this.fetchFavorites();
        })
        .catch((error) => {
          console.error("Failed to remove favorite item:", error);
        });
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
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  max-width: 800px;
  margin: 20px auto;
}

.favorite-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.favorite-item {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 200px;
  text-align: center;
}

.favorite-item img {
  max-width: 100%;
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
