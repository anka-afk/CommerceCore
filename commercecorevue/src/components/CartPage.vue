<template>
  <div class="container mt-5">
    <h1 class="mb-4 text-center">我的购物车</h1>
    <div v-if="cartItems.length > 0">
      <div
        v-for="item in cartItems"
        :key="item.id"
        class="card cart-item h-100 shadow-sm mb-4"
      >
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">{{ item.product.product_name }}</h5>
          <div class="quantity-control mb-3">
            <button
              @click="updateQuantity(item, item.quantity - 1)"
              :disabled="item.quantity <= 1"
              class="btn btn-outline-secondary"
            >
              -
            </button>
            <input
              type="number"
              v-model.number="item.quantity"
              @change="updateQuantity(item, item.quantity)"
              class="form-control mx-2 text-center"
              style="width: 60px"
            />
            <button
              @click="updateQuantity(item, item.quantity + 1)"
              class="btn btn-outline-secondary"
            >
              +
            </button>
          </div>
          <p class="card-text">单价: ¥{{ item.product.price }}</p>
          <p class="card-text">
            小计: ¥{{ item.product.price * item.quantity }}
          </p>
          <button
            @click="removeFromCart(item.product.product_id)"
            class="btn btn-outline-danger mt-auto"
          >
            从购物车中移除
          </button>
        </div>
      </div>
      <div class="text-right">
        <p class="font-weight-bold">总计: ¥{{ totalPrice }}</p>
      </div>
    </div>
    <div v-else>
      <p class="text-center">你的购物车是空的</p>
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
        (total, item) => total + item.product.price * item.quantity,
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
        this.cartItems = response.data.items;
      } catch (error) {
        this.error = "无法加载购物车，请重试";
      }
    },
    async updateQuantity(item, quantity) {
      if (quantity < 1) {
        quantity = 1;
      }

      try {
        const token = localStorage.getItem("token");
        await axios.post(
          "http://127.0.0.1:8000/api/cart/update_quantity/",
          {
            product_id: item.product.product_id,
            quantity: quantity,
          },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        this.fetchCartItems();
      } catch (error) {
        this.error = "无法更新数量，请重试";
      }
    },
    async removeFromCart(product_id) {
      try {
        const token = localStorage.getItem("token");
        await axios.post(
          "http://127.0.0.1:8000/api/cart/remove_item/",
          {
            product_id: product_id,
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
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
}

.cart-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

.quantity-control {
  display: flex;
  align-items: center;
}

.quantity-control button {
  width: 30px;
  height: 30px;
  text-align: center;
  margin: 0 5px;
  font-size: 16px;
  line-height: 1;
}

.quantity-control input {
  text-align: center;
}

.card-title {
  font-weight: bold;
  color: #343a40;
}

.card-text {
  margin-bottom: 1rem;
}

.btn-outline-danger {
  border-radius: 50px;
  width: 100%;
}

.text-right {
  text-align: right;
}

.font-weight-bold {
  font-weight: bold;
}
</style>
