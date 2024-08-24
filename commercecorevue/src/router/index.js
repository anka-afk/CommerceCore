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
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (!token && to.name !== "LoginPage") {
    next({ name: "LoginPage" });
  } else {
    next();
  }
});

export default router;
