<template>
  <div>
    <!-- 导航栏 -->
    <nav
      class="navbar navbar-expand-lg navbar-light bg-light shadow-sm sticky-top"
    >
      <a class="navbar-brand" href="#">我的电商网站</a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link" href="/products">产品列表</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/cart">购物车</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">我的账户</a>
          </li>
          <li class="nav-item">
            <button
              class="btn btn-outline-primary ml-2"
              @click="openContactModal"
            >
              联系我们
            </button>
          </li>
        </ul>
      </div>
    </nav>

    <!-- 横幅部分 -->
    <div class="jumbotron jumbotron-fluid text-center text-white">
      <div class="overlay"></div>
      <div class="container position-relative">
        <h1 class="display-4 font-weight-bold">欢迎来到我们的电商网站！</h1>
        <p class="lead">我们提供最优质的商品和最优惠的价格。</p>
        <a class="btn btn-primary btn-lg mr-2" href="/products" role="button"
          >查看产品</a
        >
        <a
          class="btn btn-secondary btn-lg"
          href="#popular-products"
          role="button"
          >热门产品</a
        >
      </div>
    </div>

    <!-- 热门产品部分 -->
    <div id="popular-products" class="container mt-5">
      <h2 class="text-center mb-4">热门产品</h2>
      <div class="row">
        <div
          class="col-md-4"
          v-for="product in featuredProducts"
          :key="product.id"
        >
          <div class="card shadow-sm mb-4 product-card">
            <img
              :src="product.image"
              class="card-img-top"
              :alt="product.product_name"
            />
            <div class="card-body">
              <h5 class="card-title">{{ product.product_name }}</h5>
              <p class="card-text text-muted">¥{{ product.price }}</p>
              <a
                :href="'/products/' + product.id"
                class="btn btn-primary btn-block"
                >查看详情</a
              >
              <button
                class="btn btn-success btn-block mt-2"
                @click="addToCart(product.id)"
              >
                添加到购物车
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer mt-auto py-3 bg-dark text-white">
      <div class="container">
        <span>© 2024 我的电商网站. 版权所有.</span>
      </div>
    </footer>

    <!-- 联系我们模态窗口 -->
    <div
      class="modal fade"
      id="contactModal"
      tabindex="-1"
      aria-labelledby="contactModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
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
            <p>如果您有任何问题，请通过以下方式联系我们：</p>
            <ul>
              <li>电话：123-456-7890</li>
              <li>邮箱：support@ecommerce.com</li>
              <li>地址：某某市某某区某某路123号</li>
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
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      featuredProducts: [], // 热门产品列表
    };
  },
  created() {
    // 获取热门产品数据
    axios
      .get("http://127.0.0.1:8000/api/products/?suggest=true")
      .then((response) => {
        this.featuredProducts = response.data;
      })
      .catch((error) => {
        console.error(
          "There was an error fetching the featured products:",
          error
        );
      });
  },
  methods: {
    openContactModal() {
      // 打开联系模态窗口
      window.$("#contactModal").modal("show");
    },
    addToCart(productId) {
      console.log("Adding product to cart:", productId);
      // 这里可以添加购物车功能的逻辑
    },
  },
};
</script>

<style scoped>
.navbar {
  padding: 1rem 2rem;
}

.jumbotron {
  background: url("https://example.com/banner.jpg") center center no-repeat;
  background-size: cover;
  position: relative;
}

.jumbotron .overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.card-img-top {
  height: 200px;
  object-fit: cover;
  transition: transform 0.3s ease-in-out;
}

.card-img-top:hover {
  transform: scale(1.05);
}

.product-card:hover {
  transform: scale(1.02);
  transition: transform 0.3s ease-in-out;
}

.card-title {
  font-weight: 600;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  transition: background-color 0.3s ease-in-out;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
  transition: background-color 0.3s ease-in-out;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #218838;
}

.footer {
  background-color: #343a40;
  color: white;
  text-align: center;
}

.modal-content {
  border-radius: 0.75rem;
  overflow: hidden;
}

.modal-header {
  border-bottom: none;
}

.modal-footer {
  border-top: none;
}
</style>
