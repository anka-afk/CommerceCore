<template>
  <div class="container mt-5">
    <h1 class="mb-4">我的购物车</h1>
    <div v-if="cartItems.length > 0">
      <div v-for="item in cartItems" :key="item.id" class="cart-item">
        <h4>{{ item.product_name }}</h4>
        <p>数量: {{ item.quantity }}</p>
        <p>价格: ${{ item.price }}</p>
        <button @click="removeFromCart(item.product)">从购物车中移除</button>
      </div>
      <p>总计: ${{ totalPrice }}</p>
    </div>
    <div v-else>
      <p>你的购物车是空的</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      cartItems: [],
      error: "",
    };
  },
  computed: {
    totalPrice() {
      return this.cartItems.reduce(
        (total, item) => total + item.price * item.quantity,
        0
      );
    },
  },
  created() {
    this.fetchCartItems();
  },
  methods: {
    async fetchCartItems() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:8000/api/cart/", {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.cartItems = response.data;
      } catch (error) {
        this.error = "无法加载购物车，请重试";
      }
    },
    async removeFromCart(product) {
      try {
        const token = localStorage.getItem("token");
        await axios.post(
          "http://127.0.0.1:8000/api/cart/remove_item/",
          {
            product_id: product.id,
          },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        this.fetchCartItems();
      } catch (error) {
        this.error = "无法移除商品，请重试";
      }
    },
  },
};
</script>

<style scoped>
.cart-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
</style>
