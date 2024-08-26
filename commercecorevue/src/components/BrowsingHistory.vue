<template>
  <BaseTemplate>
    <section class="browsing-history-section">
      <h2>浏览记录</h2>
      <div v-if="browsingHistory.length">
        <div
          v-for="item in browsingHistory"
          :key="item.id"
          class="history-item"
        >
          <!-- 显示商品图片并添加点击事件跳转到商品详情 -->
          <img
            :src="item.product.image"
            alt="Product Image"
            class="product-image"
            @click="goToProductDetail(item.product.product_id)"
          />
          <div class="product-info">
            <h3>{{ item.product.product_name }}</h3>
            <p>价格: ¥{{ item.product.price }}</p>
            <p>浏览时间: {{ formatDate(item.browse_date) }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>暂无浏览记录。</p>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import BaseTemplate from "./BaseTemplate.vue";

export default {
  components: { BaseTemplate },
  data() {
    return {
      browsingHistory: [],
    };
  },
  mounted() {
    this.fetchBrowsingHistory();
  },
  methods: {
    async fetchBrowsingHistory() {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/browsing-history/"
        );
        const history = response.data;

        // 获取所有 product_id 的商品详细信息
        const productPromises = history.map((item) =>
          axios
            .get(`http://localhost:8000/api/products/${item.product}/`)
            .catch((error) => {
              if (error.response && error.response.status === 404) {
                console.error(`Product with ID ${item.product} not found.`);
                return null; // 返回 null 用于标记商品不存在
              }
              throw error;
            })
        );

        const products = await Promise.all(productPromises);

        // 合并商品信息和浏览记录，排除返回 null 的商品
        this.browsingHistory = history
          .map((item, index) => {
            if (products[index]) {
              return {
                ...item,
                product: products[index].data,
              };
            }
            return null;
          })
          .filter((item) => item !== null);
      } catch (error) {
        console.error("Failed to fetch browsing history:", error);
      }
    },
    goToProductDetail(productId) {
      this.$router.push({ name: "ProductDetail", params: { id: productId } }); // 跳转到商品详情页
    },
    formatDate(dateString) {
      const options = {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.browsing-history-section {
  padding: 2rem;
}

.history-item {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  padding: 1rem;
  border-radius: 10px;
}

.product-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
  cursor: pointer; /* 增加手型指针，提示图片可点击 */
}

.product-info {
  flex-grow: 1;
}

.product-info h3 {
  margin: 0;
  font-size: 1.2rem;
}
</style>
