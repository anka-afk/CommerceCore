import { createRouter, createWebHistory } from "vue-router";
import ProductList from "../components/ProductList.vue";
import Home from "../components/HomePage.vue";
import Login from "../components/LoginPage.vue";
import Cart from "../components/CartPage.vue";
import UserAccount from "@/components/UserAccount.vue";

const routes = [
  {
    path: "/products",
    name: "Products",
    component: ProductList,
  },
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/login",
    name: "LoginPage",
    component: Login,
  },
  {
    path: "/cart",
    name: "CartPage",
    component: Cart, // 添加购物车页面的路由
  },
  {
    path: "/account",
    name: "account",
    component: UserAccount,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// 使用 beforeEach 钩子进行身份验证检查
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  // 如果没有 token 并且试图访问非登录页面，重定向到登录页面
  if (to.name !== "LoginPage" && !token) {
    next({ name: "LoginPage" });
  } else {
    next();
  }
});

export default router;
