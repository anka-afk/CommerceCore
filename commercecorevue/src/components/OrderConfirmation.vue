<template>
  <BaseTemplate>
    <section class="order-confirmation-section">
      <h2>确认订单</h2>

      <!-- 商品列表部分 -->
      <div class="order-summary glass-card">
        <div v-for="item in cartItems" :key="item.id" class="order-item">
          <img
            :src="`${mediaUrl}${item.product.image}`"
            alt="Product Image"
            class="order-item-image"
            @error="handleImageError($event)"
          />
          <div class="order-item-details">
            <h4>{{ item.product.product_name }}</h4>
            <p>{{ item.quantity }} × {{ item.product.price }} 元</p>
            <p v-if="item.product.discount > 0">
              折扣: -{{ item.product.discount }} 元
            </p>
            <p>
              总价:
              {{
                (
                  (item.product.price - (item.product.discount || 0)) *
                  item.quantity
                ).toFixed(2)
              }}
              元
            </p>
          </div>
        </div>
      </div>

      <!-- 选项部分（支付方式和地址选择） -->
      <div class="options-section glass-card">
        <div class="payment-method-section">
          <h3>选择支付方式</h3>
          <select v-model="selectedPaymentMethod">
            <option value="alipay">支付宝</option>
            <option value="wechat">微信支付</option>
            <option value="credit_card">信用卡</option>
          </select>
        </div>

        <div class="address-section">
          <h3>配送地址</h3>
          <div class="address-input-group">
            <input
              v-model="enteredAddress"
              placeholder="请输入配送地址"
              class="address-input"
            />
            <button
              class="btn btn-secondary use-default-address"
              @click="useDefaultAddress"
            >
              使用默认地址
            </button>
          </div>
        </div>

        <!-- 总金额显示部分 -->
        <div class="total-amount">
          <h3>总金额: {{ totalAmount.toFixed(2) }} 元</h3>
        </div>
      </div>

      <!-- 确认支付按钮 -->
      <div class="confirm-button-section glass-card">
        <button class="btn btn-primary" @click="openPaymentPage">
          确认支付
        </button>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      selectedPaymentMethod: "alipay",
      enteredAddress: "", // 用于保存用户输入的地址
      userProfile: {}, // 用户的Profile信息
      mediaUrl: "http://localhost:8000", // 后端基础URL
    };
  },
  computed: {
    ...mapGetters(["cartItems", "totalAmount"]),
  },
  mounted() {
    console.log("Order ID:", this.$route.params.orderId); // 调试输出
    this.fetchUserProfile();
  },
  methods: {
    ...mapActions(["clearCartItems"]),

    fetchUserProfile() {
      axios
        .get("http://localhost:8000/api/user/profile/")
        .then((response) => {
          this.userProfile = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    },

    useDefaultAddress() {
      if (this.userProfile.address && this.userProfile.address !== "未填写") {
        this.enteredAddress = this.userProfile.address;
      } else {
        alert("没有找到默认地址，请手动输入");
      }
    },

    handleImageError(event) {
      event.target.src = "./assets/default.png"; // 使用默认图片路径替换损坏的图片
    },

    openPaymentPage() {
      if (!this.enteredAddress) {
        alert("请填写配送地址");
        return;
      }

      const orderData = {
        user: this.userProfile.id,
        total_amount: this.totalAmount.toFixed(2),
        payment_method: this.selectedPaymentMethod,
        address: this.enteredAddress,
        items: this.cartItems.map((item) => ({
          product_id: item.product.product_id,
          product_name: item.product.product_name,
          quantity: item.quantity,
          unit_price: item.product.price,
          discount: item.product.discount || 0,
        })),
      };

      axios
        .post("http://localhost:8000/api/orders/create/", orderData)
        .then((response) => {
          const orderId = response.data.number; // 使用正确的字段
          if (!orderId) {
            console.error("Order ID is missing");
            return;
          }
          alert("订单提交成功");
          this.clearCartItems();
          this.$router.push({
            name: "PaymentPage",
            params: { orderId: orderId },
          });
        })
        .catch((error) => {
          console.error("Failed to create order:", error);
        });
    },
  },
};
</script>

<style scoped>
/* 样式代码 */
.order-confirmation-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
}

.glass-card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.order-summary {
  flex: 1;
}

.order-item {
  display: flex;
  margin-bottom: 1rem;
}

.order-item-image {
  width: 80px;
  height: 80px;
  margin-right: 1rem;
}

.order-item-details {
  flex: 1;
}

.options-section {
  flex: 1;
}

.payment-method-section,
.address-section,
.total-amount {
  margin-bottom: 1.5rem;
}

.address-input-group {
  display: flex;
  align-items: center;
}

.address-input {
  flex: 1;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-right: 1rem;
}

.use-default-address {
  padding: 0.5rem 1rem;
}

.confirm-button-section {
  text-align: center;
}
</style>
