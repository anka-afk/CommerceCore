<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-navbar">
      <a class="navbar-brand" href="#">我的电商网站</a>
      <div class="navbar-menu">
        <router-link class="nav-link" to="/products">产品列表</router-link>
        <router-link class="nav-link" to="/cart">购物车</router-link>
        <button class="btn-contact" @click="openContactModal">联系我们</button>
        <img
          src="user-avatar.jpg"
          class="user-avatar"
          @click="goToAccount"
          alt="User Avatar"
        />
      </div>
    </nav>

    <!-- Jumbotron 横幅 -->
    <section class="jumbotron">
      <div class="content">
        <h1>欢迎来到我的电商网站</h1>
        <p>这里有最好的产品，最优惠的价格。</p>
        <button class="btn btn-primary btn-lg">立即购物</button>
      </div>
    </section>

    <!-- 产品展示 -->
    <section class="product-section">
      <div class="product-slider" ref="slider">
        <div
          class="product-slide"
          v-for="product in products"
          :key="product.id"
        >
          <div class="card product-card">
            <img :src="product.image" class="card-img-top" alt="产品图片" />
            <div class="card-body">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="card-text">{{ product.description }}</p>
              <button class="btn btn-primary">添加到购物车</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <span>&copy; 2024 我的电商网站. 版权所有.</span>
      </div>
    </footer>

    <!-- 联系我们 模态框 -->
    <div
      class="modal fade"
      id="contactModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="contactModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="contactModalLabel">联系我们</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>您可以通过以下方式联系我们：</p>
            <ul>
              <li>电子邮件: support@example.com</li>
              <li>电话: 123-456-7890</li>
            </ul>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-dismiss="modal"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      products: [
        {
          id: 1,
          name: "产品1",
          description: "这是产品1的描述。",
          image: "https://via.placeholder.com/200",
        },
        {
          id: 2,
          name: "产品2",
          description: "这是产品2的描述。",
          image: "https://via.placeholder.com/200",
        },
        {
          id: 3,
          name: "产品3",
          description: "这是产品3的描述。",
          image: "https://via.placeholder.com/200",
        },
        // 添加更多产品
      ],
    };
  },
  mounted() {
    this.startAutoSlide();
  },
  methods: {
    openContactModal() {
      this.$refs.contactModal.show();
    },
    goToAccount() {
      this.$router.push("/account");
    },
    startAutoSlide() {
      setInterval(() => {
        const slider = this.$refs.slider;
        slider.scrollLeft += slider.clientWidth;
        if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth) {
          slider.scrollLeft = 0;
        }
      }, 20000); // 每20秒自动滑动
    },
  },
};
</script>

<style scoped>
/* 设置背景图片覆盖整个网页，并固定不动 */
.app-container {
  height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
}

/* 导航栏毛玻璃效果 */
.glass-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-brand {
  font-size: 1.5rem;
  color: #007bff;
}

.navbar-menu {
  display: flex;
  align-items: center;
}

.nav-link {
  margin-right: 1rem;
  color: #333;
  text-decoration: none;
}

.btn-contact {
  background: transparent;
  border: 1px solid #007bff;
  padding: 0.5rem 1rem;
  color: #007bff;
  margin-right: 1rem;
  cursor: pointer;
}

.btn-contact:hover {
  background: #007bff;
  color: white;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}

/* Jumbotron 横幅 */
.jumbotron {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  margin-top: 2rem;
}

.jumbotron .content {
  color: white;
}

.jumbotron h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.jumbotron p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

/* 产品展示 */
.product-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.product-slider {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
}

.product-slide {
  flex: 0 0 auto;
  width: 300px;
  margin-right: 20px;
}

.card {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 10px;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transition: transform 0.3s ease-in-out;
}

.card-img-top:hover {
  transform: scale(1.05);
}

.card-title {
  font-weight: bold;
}

.product-card {
  padding: 1rem;
}

/* 页脚 */
.footer {
  background: rgba(52, 58, 64, 0.8);
  color: white;
  text-align: center;
  padding: 1rem;
}

.container {
  max-width: 1140px;
  margin: 0 auto;
}

/* 模态框 */
.modal-content {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
}
</style>
