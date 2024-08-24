<template>
  <BaseTemplate>
    <!-- 结算页面 -->
    <section class="checkout-section">
      <div class="checkout-container">
        <h2>结算页面</h2>
        <div class="cart-items">
          <div class="cart-item" v-for="item in cartItems" :key="item.id">
            <img
              :src="getImageUrl(item.product.image)"
              alt="Product Image"
              class="cart-item-image"
            />
            <div class="cart-item-details">
              <h4>{{ item.product.product_name }}</h4>
              <p>数量: {{ item.quantity }}</p>
              <p>单价: ¥{{ item.product.price }}</p>
              <p>总价: ¥{{ item.product.price * item.quantity }}</p>
            </div>
          </div>
        </div>
        <div class="total-amount">
          <h3>总金额: ¥{{ totalAmount }}</h3>
        </div>
        <button class="btn btn-success" @click="proceedToPayment">支付</button>
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
      cartItems: [], // 购物车中的商品列表
      mediaUrl: "http://localhost:8000", // 后端服务器基础URL
    };
  },
  computed: {
    totalAmount() {
      // 计算购物车中的商品总金额
      return this.cartItems.reduce((total, item) => {
        return total + item.product.price * item.quantity;
      }, 0);
    },
  },
  mounted() {
    this.fetchCartItems(); // 获取购物车商品
  },
  methods: {
    fetchCartItems() {
      axios
        .get("http://localhost:8000/api/cart/")
        .then((response) => {
          this.cartItems = response.data.items; // 假设返回的数据中包含购物车商品列表
        })
        .catch((error) => {
          console.error("Failed to fetch cart items:", error);
        });
    },

    getImageUrl(imagePath) {
      // 构建完整的图片URL
      return `${this.mediaUrl}${imagePath}`;
    },

    proceedToPayment() {
      // 在这里处理支付逻辑，例如重定向到支付页面
      alert("支付功能待实现");
    },
  },
  components: { BaseTemplate },
};
</script>

<style scoped>
/* 结算页面样式 */
.checkout-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.checkout-container {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 10px;
  max-width: 800px;
  width: 100%;
}

.cart-items {
  margin-bottom: 2rem;
}

.cart-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.cart-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 10px;
  margin-right: 1rem;
}

.cart-item-details {
  flex-grow: 1;
}

.total-amount {
  text-align: right;
  margin-bottom: 2rem;
}
</style>
