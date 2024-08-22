<template>
  <div>
    <!-- 导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
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
        </ul>
      </div>
    </nav>

    <!-- 横幅部分 -->
    <div class="jumbotron jumbotron-fluid">
      <div class="container">
        <h1 class="display-4">欢迎来到我们的电商网站！</h1>
        <p class="lead">我们提供最优质的商品和最优惠的价格。</p>
        <a class="btn btn-primary btn-lg" href="/products" role="button"
          >查看产品</a
        >
      </div>
    </div>

    <!-- 热门产品部分 -->
    <div class="container mt-5">
      <h2>热门产品</h2>
      <div class="row">
        <div
          class="col-md-4"
          v-for="product in featuredProducts"
          :key="product.id"
        >
          <div class="card">
            <img
              :src="product.image"
              class="card-img-top"
              :alt="product.product_name"
            />
            <div class="card-body">
              <h5 class="card-title">{{ product.product_name }}</h5>
              <p class="card-text text-muted">¥{{ product.price }}</p>
              <a :href="'/products/' + product.id" class="btn btn-primary"
                >查看详情</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer mt-auto py-3 bg-light">
      <div class="container">
        <span class="text-muted">© 2024 我的电商网站. 版权所有.</span>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "HomePage", // 将组件名称更改为多词名称
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
};
</script>

<style scoped>
.jumbotron {
  background: url("https://example.com/banner.jpg") center center no-repeat;
  background-size: cover;
  color: white;
}

.card-img-top {
  height: 200px;
  object-fit: cover;
}

.footer {
  position: relative;
  bottom: 0;
  width: 100%;
  text-align: center;
}
</style>
