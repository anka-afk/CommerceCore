<template>
  <BaseTemplate>
    <div class="payment-modal-container">
      <div class="payment-modal glass-card">
        <h2>请扫码支付</h2>
        <img src="@/assets/qr_code.png" alt="二维码" class="qr-code" />

        <div class="order-info">
          <p><strong>订单号：</strong>{{ order.number || "未知订单号" }}</p>
          <p><strong>订单时间：</strong>{{ formattedOrderDate }}</p>
          <p><strong>总金额：</strong>{{ orderTotalAmount }} 元</p>
          <p>
            <strong>订单状态：</strong>
            <span @click="toggleOrderStatus" class="order-status">
              {{ orderStatusText }}
            </span>
          </p>
        </div>

        <div class="countdown">
          <p>请在 {{ countdown }} 秒内完成支付</p>
        </div>

        <div class="actions">
          <button class="btn btn-danger" @click="cancelOrder">取消订单</button>
          <button class="btn btn-primary" @click="confirmPayment">确定</button>
        </div>
      </div>
    </div>
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      order: {},
      countdown: 180, // 3分钟倒计时
      orderStatus: "awaiting_payment", // 订单状态
      intervalId: null,
    };
  },
  computed: {
    ...mapGetters(["getOrderById"]),

    formattedOrderDate() {
      if (!this.order.order_date) {
        return "无效的日期";
      }
      return new Date(this.order.order_date).toLocaleString();
    },

    orderTotalAmount() {
      const amount = parseFloat(this.order.total_amount); // 确保转换为数字类型
      return isNaN(amount) ? "0.00" : amount.toFixed(2);
    },

    orderStatusText() {
      switch (this.orderStatus) {
        case "awaiting_payment":
          return "等待支付";
        case "paied":
          return "已支付";
        case "payment_failed":
          return "支付失败";
        case "cancelled":
          return "已取消";
        default:
          return "未知状态";
      }
    },
  },
  mounted() {
    this.fetchOrderDetails();
    this.startCountdown();
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  },
  methods: {
    fetchOrderDetails() {
      const orderId = this.$route.params.orderId;
      if (!orderId) {
        console.error("Order ID is undefined");
        return;
      }
      axios
        .get(`http://localhost:8000/api/orders/${orderId}/`)
        .then((response) => {
          this.order = response.data;
          this.orderStatus = this.order.order_status; // 确保状态同步
        })
        .catch((error) => {
          console.error("Failed to fetch order details:", error);
        });
    },

    startCountdown() {
      this.intervalId = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown -= 1;
        } else {
          this.orderStatus = "payment_failed";
          clearInterval(this.intervalId);
          this.updateOrderStatus(); // 倒计时结束时更新订单状态
        }
      }, 1000);
    },

    toggleOrderStatus() {
      if (this.orderStatus === "awaiting_payment") {
        this.orderStatus = "paied";
      } else if (this.orderStatus === "paied") {
        this.orderStatus = "payment_failed";
      } else if (this.orderStatus === "payment_failed") {
        this.orderStatus = "awaiting_payment";
      }
      this.updateOrderStatus();
    },

    cancelOrder() {
      this.orderStatus = "cancelled";
      this.updateOrderStatus(() => {
        this.$router.push("/cart"); // 状态更新后再跳转
      });
    },

    confirmPayment() {
      if (this.orderStatus === "paied") {
        this.$router.push("/cart");
      } else {
        alert("订单未支付，无法完成");
      }
    },

    updateOrderStatus(callback = () => {}) {
      axios
        .patch(`http://localhost:8000/api/orders/${this.order.number}/`, {
          order_status: this.orderStatus,
        })
        .then(() => {
          console.log("Order status updated successfully");
          callback(); // 更新成功后调用回调
        })
        .catch((error) => {
          console.error("Failed to update order status:", error);
        });
    },
  },
};
</script>

<style scoped>
.payment-modal-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.payment-modal {
  width: 400px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.qr-code {
  width: 200px;
  height: 200px;
  margin: 20px 0;
}

.order-info {
  margin-bottom: 20px;
}

.order-status {
  cursor: pointer;
  color: #007bff;
}

.order-status:hover {
  text-decoration: underline;
}

.actions {
  display: flex;
  justify-content: space-between;
}

.actions .btn {
  width: 45%;
}
</style>
