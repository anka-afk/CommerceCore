import { createRouter, createWebHistory } from "vue-router";
import ProductList from "../components/ProductList.vue";
import Home from "../components/HomePage.vue";
import Login from "../components/LoginPage.vue";
import Cart from "../components/CartPage.vue";
import UserAccount from "@/components/UserAccount.vue";
import Register from "@/components/RegisterPage.vue";
import FavoriteList from "../components/FavoriteList.vue";
import HelpPage from "../components/HelpPage.vue";
import AnnouncementPage from "../components/AnnouncementPage.vue";
import SettingsPage from "../components/SettingsPage.vue";
import ForgetPasswordPage from "../components/ForgetPasswordPage.vue";
import ProductDetailPage from "../components/ProductDetailPage.vue";
import TestPage from "../components/TestPage.vue";
import OrderConfirmation from "../components/OrderConfirmation.vue";
import PaymentPage from "../components/PaymentPage.vue";
import ReviewPage from "../components/ReviewPage.vue";
import BrowsingHistory from "../components/BrowsingHistory.vue";

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
    path: "/Home",
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
  {
    path: "/register",
    name: "RegisterPage",
    component: Register,
  },
  {
    path: "/favorites",
    name: "Favorites",
    component: FavoriteList,
  },
  {
    path: "/help",
    name: "HelpPage",
    component: HelpPage,
  },
  {
    path: "/notifications",
    name: "AnnouncementPage",
    component: AnnouncementPage,
  },
  {
    path: "/settings",
    name: "SettingsPage",
    component: SettingsPage,
  },
  {
    path: "/forget-password",
    name: "ForgetPasswordPage",
    component: ForgetPasswordPage,
  },
  {
    path: "/products/:id",
    name: "ProductDetail",
    component: ProductDetailPage,
  },
  {
    path: "/test",
    name: "TestPage",
    component: TestPage,
  },
  {
    path: "/order-confirmation",
    name: "OrderConfirmation",
    component: OrderConfirmation,
  },
  {
    path: "/payment/:orderId",
    name: "PaymentPage",
    component: PaymentPage,
  },
  {
    path: "/orders",
    name: "MyOrders",
    component: () => import("@/components/MyOrders.vue"),
  },
  {
    path: "/review/:productId",
    name: "ReviewPage",
    component: ReviewPage,
  },
  {
    path: "/browsing-history",
    name: "BrowsingHistory",
    component: BrowsingHistory,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  // 列出所有不需要认证就能访问的路由名称
  const publicPages = ["LoginPage", "RegisterPage", "ForgetPasswordPage"];
  const isPublicPage = publicPages.includes(to.name);

  // 如果没有 token 且目标页面不是公共页面，则跳转到登录页面
  if (!token && !isPublicPage) {
    next({ name: "LoginPage" });
  } else {
    next();
  }
});

export default router;
