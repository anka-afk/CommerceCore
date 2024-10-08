<template>
  <BaseTemplate>
    <!-- 购物车内容 -->
    <section class="cart-section">
      <h2>您的购物车</h2>
      <div v-if="cartItems.length === 0">您的购物车是空的。</div>
      <div v-else class="cart-items-container">
        <div
          class="cart-item-card"
          v-for="item in cartItems"
          :key="item.product.product_id"
        >
          <div class="cart-item-content">
            <!-- 修改图片的 src 绑定，并添加点击事件 -->
            <img
              :src="`${mediaUrl}${item.product.image}`"
              alt="商品图片"
              class="cart-item-image"
              @click="goToProductDetail(item.product.product_id)"
            />
            <div class="cart-item-details">
              <h4 class="cart-item-name">{{ item.product.product_name }}</h4>
              <p>单价: {{ item.product.price }} 元</p>
              <p>
                数量:
                <button @click="decreaseQuantity(item)">-</button>
                <span>{{ item.quantity }}</span>
                <button @click="increaseQuantity(item)">+</button>
              </p>
              <p>
                总计: {{ (item.product.price * item.quantity).toFixed(2) }} 元
              </p>
              <button class="btn btn-danger" @click="removeFromCart(item)">
                移除
              </button>
            </div>
          </div>
        </div>
        <div class="cart-summary">
          <p>总金额: {{ totalAmount.toFixed(2) }} 元</p>
          <button class="btn btn-primary" @click="checkout">结算</button>
        </div>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      mediaUrl: "http://localhost:8000", // 将其设置为你的后端基础 URL，省略 /media/
    };
  },
  computed: {
    // 从 Vuex 获取购物车内容和总金额
    ...mapGetters(["cartItems", "totalAmount"]),
  },
  mounted() {
    this.fetchCartItems(); // 获取购物车数据
  },
  methods: {
    // 通过 Vuex actions 来操作购物车
    ...mapActions([
      "fetchCartItems",
      "addItemToCart",
      "removeItemFromCart",
      "clearCartItems",
    ]),

    increaseQuantity(item) {
      this.addItemToCart({ ...item, quantity: 1 }); // 增加商品数量
    },

    decreaseQuantity(item) {
      if (item.quantity > 1) {
        this.addItemToCart({ ...item, quantity: -1 }); // 减少商品数量
      }
    },

    removeFromCart(item) {
      this.removeItemFromCart(item.product.product_id); // 移除商品
    },

    checkout() {
      this.$router.push({ name: "OrderConfirmation" }); // 跳转到订单确认页面
    },

    goToProductDetail(productId) {
      this.$router.push({ name: "ProductDetail", params: { id: productId } }); // 跳转到商品详情页
    },
  },
};
</script>

<style scoped>
/* 购物车样式 */
.cart-items-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cart-section {
  @extend .glass-effect;
  padding: 2rem;
  max-width: 1200px;
  margin: 2rem auto;
}

.cart-item-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(5px);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 600px;
}

.cart-item-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.cart-item {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.7);
  padding: 10px;
  border-radius: 10px;
}

.cart-item-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 10px;
  margin-right: 1rem;
  cursor: pointer; /* 增加手型指针，提示图片可点击 */
}

.cart-item-details {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.cart-item-name {
  font-size: 1.2rem;
  font-weight: bold;
}

.cart-item-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.cart-item-actions button {
  padding: 5px 10px;
  border: 1px solid #ccc;
  background-color: #fff;
  cursor: pointer;
  transition: background 0.3s;
}

.cart-item-actions button:hover {
  background-color: #f0f0f0;
}

.cart-item-price {
  margin-top: 10px;
  font-weight: bold;
}

.cart-summary {
  margin-top: 2rem;
  text-align: right;
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
