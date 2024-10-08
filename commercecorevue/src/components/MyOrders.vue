<template>
  <BaseTemplate>
    <section class="orders-section">
      <h2>我的订单</h2>
      <div v-if="orders.length === 0" class="no-orders">
        <p>您还没有订单。</p>
      </div>
      <div
        v-for="order in orders"
        :key="order.number"
        class="order-card glass-card"
      >
        <div class="order-header">
          <p><strong>订单号：</strong>{{ order.number }}</p>
          <p><strong>订单时间：</strong>{{ formatDate(order.order_date) }}</p>
          <p><strong>总金额：</strong>{{ order.total_amount }} 元</p>
          <p>
            <strong>订单状态：</strong>{{ getStatusText(order.order_status) }}
          </p>
        </div>
        <div class="order-details">
          <h4>订单详情：</h4>
          <div
            v-for="detail in order.order_details"
            :key="detail.id"
            class="order-detail-item"
          >
            <img
              :src="getProductImageUrl(detail.product_image)"
              alt="商品图片"
              class="product-image"
            />
            <p><strong>商品名称：</strong>{{ detail.product_name }}</p>
            <p><strong>数量：</strong>{{ detail.quantity }}</p>
            <p><strong>单价：</strong>{{ detail.unit_price }} 元</p>
            <p><strong>折扣：</strong>{{ detail.discount }} 元</p>
            <p><strong>税额：</strong>{{ detail.tax }} 元</p>
            <p>
              <strong>总价：</strong>
              {{
                (
                  Number(detail.unit_price) * Number(detail.quantity) -
                  Number(detail.discount) +
                  Number(detail.tax)
                ).toFixed(2)
              }}
              元
            </p>
            <button
              v-if="order.order_status === 'paied'"
              class="btn btn-primary"
              @click="goToReview(detail.product_id)"
            >
              评价
            </button>
          </div>
        </div>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      orders: [],
    };
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    fetchOrders() {
      axios
        .get("http://localhost:8000/api/orders/")
        .then((response) => {
          console.log(response.data); // 打印API返回的数据
          this.orders = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch orders:", error);
        });
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    getStatusText(status) {
      switch (status) {
        case "awaiting_payment":
          return "等待支付";
        case "paied":
          return "已支付";
        case "shipped":
          return "已发货";
        case "delivered":
          return "已送达";
        case "cancelled":
          return "已取消";
        default:
          return "未知状态";
      }
    },
    getProductImageUrl(imagePath) {
      return `http://localhost:8000${imagePath}`;
    },
    goToReview(productId) {
      if (productId) {
        this.$router.push({
          name: "ReviewPage",
          params: { productId }, // 确保传递正确的参数
        });
      } else {
        console.error("Product ID is missing.");
      }
    },
  },
};
</script>

<style scoped>
.orders-section {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.no-orders {
  text-align: center;
  font-size: 1.2rem;
  color: #555;
}

.order-card {
  padding: 1.5rem;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.order-header {
  margin-bottom: 1rem;
  font-weight: bold;
}

.order-details {
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.order-detail-item {
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.order-detail-item:last-child {
  border-bottom: none;
}

.btn {
  margin-left: auto;
}
</style>
