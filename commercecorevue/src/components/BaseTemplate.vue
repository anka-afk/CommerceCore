<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="navbar glass-navbar">
      <a class="navbar-brand" href="#">
        <img src="../assets/logo.png" alt="隙间小铺" class="navbar-logo" />
        <span class="brand-name">隙间小铺</span>
      </a>
      <div class="navbar-menu">
        <div class="nav-links">
          <router-link class="nav-link" to="/home" exact-active-class="active">
            <img src="../assets/Home.png" class="nav-icon" /> 首页
          </router-link>
          <router-link
            class="nav-link"
            to="/products"
            exact-active-class="active"
          >
            <img src="../assets/store.png" class="nav-icon" /> 商店
          </router-link>
          <router-link class="nav-link" to="/cart" exact-active-class="active">
            <img src="../assets/cart.png" class="nav-icon" /> 购物车
          </router-link>
          <router-link
            class="nav-link"
            to="/favorites"
            exact-active-class="active"
          >
            <img src="../assets/favorite.png" class="nav-icon" /> 收藏
          </router-link>
          <router-link class="nav-link" to="/help" exact-active-class="active">
            <img src="../assets/help.png" class="nav-icon" /> 帮助
          </router-link>
          <router-link
            class="nav-link"
            to="/settings"
            exact-active-class="active"
          >
            <img src="../assets/settings.png" class="nav-icon" /> 设置
          </router-link>
          <router-link
            class="nav-link"
            to="/notifications"
            exact-active-class="active"
          >
            <img src="../assets/notifications.png" class="nav-icon" /> 公告
          </router-link>
        </div>
        <div
          class="avatar-container"
          @mouseover="showDropdown = true"
          @mouseleave="showDropdown = false"
        >
          <img
            :src="avatarUrl"
            class="user-avatar"
            @click="goToAccount"
            alt="User Avatar"
          />
          <div v-if="showDropdown" class="dropdown-menu">
            <div class="dropdown-header">
              <p>你好, 用户 {{ userProfile.username }}</p>
              <p>{{ userProfile.email }}</p>
            </div>
            <button @click="goToBrowsingHistory">
              <img
                src="../assets/history.png"
                class="dropdown-icon"
                alt="历史图标"
              />
              浏览记录
            </button>
            <button @click="goToOrders">
              <img
                src="../assets/orders.png"
                class="dropdown-icon"
                alt="订单图标"
              />
              我的订单
            </button>
            <button @click="logout">
              <img
                src="../assets/logout.png"
                class="dropdown-icon"
                alt="登出图标"
              />
              登出
            </button>
          </div>
        </div>
      </div>
    </nav>
    <!-- 主要内容插槽 -->
    <section class="content-section">
      <slot></slot>
    </section>
    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <span>&copy; 2024 anka. 版权所有.</span>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentPage: 0,
      mediaUrl: "http://localhost:8000", // 将其设置为你的后端基础 URL，省略 /media/
      userProfile: {}, // 用户信息对象
      avatarUrl: null, // 头像URL
      showDropdown: false,
    };
  },
  mounted() {
    this.fetchUserProfile(); // 添加获取用户信息的方法
    this.fetchUsername(); // 调用获取用户名的方法
  },
  methods: {
    fetchUsername() {
      axios
        .get("http://localhost:8000/api/user/username/")
        .then((response) => {
          this.userProfile.username = response.data.username; // 假设返回的对象中包含 'username'
        })
        .catch((error) => {
          console.error("Failed to fetch username:", error);
        });
    },

    goToBrowsingHistory() {
      this.$router.push("/browsing-history");
    },
    goToOrders() {
      this.$router.push("/orders");
    },
    logout() {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        console.error("No refresh token found.");
        return;
      }

      axios
        .post("http://localhost:8000/api/logout/", {
          refresh_token: refreshToken,
        })
        .then(() => {
          // 清除 localStorage 中保存的 tokens
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          // 跳转到登录页面
          this.$router.push("/login");
        })
        .catch((error) => {
          console.error("Failed to logout:", error);
        });
    },

    fetchUserProfile() {
      axios
        .get("http://localhost:8000/api/user/profile/")
        .then((response) => {
          this.userProfile = response.data.profile; // 假设返回的数据中包含用户profile信息
          this.avatarUrl = `${this.mediaUrl}${this.userProfile.avatar}`;
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    },

    handleImageError(event) {
      event.target.src = "./assets/default.png"; // 使用默认图片路径替换损坏的图片
    },

    goToAccount() {
      this.$router.push("/account");
    },
  },
};
</script>

<style scoped>
/* 设置背景图片覆盖整个网页，并固定不动 */
.app-container {
  min-height: 100vh;
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
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 60px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.navbar-logo {
  height: 40px;
  margin-right: 0.5rem;
}

.brand-name {
  font-size: 1.5rem;
  font-family: "Microsoft Yahei UI light", cursive;
  color: #007bff;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  transition: color 0.3s ease, transform 0.3s ease;
}

.brand-name:hover {
  color: #0056b3;
  transform: scale(1.05);
}

.navbar-menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
}

.nav-links {
  display: flex;
  justify-content: center;
  flex: 1;
  gap: 15px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  color: #333;
  font-size: 0.9rem;
  text-decoration: none;
  transition: background 0.3s, color 0.3s;
  border-radius: 20px;
}

.nav-link:hover,
.nav-link.active {
  background: #e0f7e9;
  color: #28a745;
}

.nav-icon {
  width: 20px;
  height: 20px;
  margin-right: 0.4rem;
}

.btn-contact {
  background: transparent;
  border: 1px solid #007bff;
  padding: 0.5rem 1rem;
  color: #007bff;
  margin-right: 1rem;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
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
  border: 2px solid #28a745;
  transition: border 0.3s, transform 0.3s;
}

.user-avatar:hover {
  border-color: #1e7e34;
  transform: scale(1.1);
}

.avatar-container {
  position: relative;
  display: inline-block;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  border: 2px solid transparent;
  transition: border-color 0.3s;
}

.dropdown-menu:hover {
  border-color: #007bff;
}

.dropdown-header {
  padding: 8px;
  border-bottom: 1px solid #ddd;
  margin-bottom: 10px;
}

.dropdown-header p {
  margin: 0;
  font-size: 14px;
  color: #333;
}

.dropdown-menu button {
  background: none;
  border: none;
  padding: 8px;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.dropdown-menu button:hover {
  background-color: #f0f0f0;
  border-radius: 5px;
}

.dropdown-icon {
  width: 20px;
  height: 20px;
  margin-right: 8px;
}

/* 页脚 */
.footer {
  background: rgba(52, 58, 64, 0.8);
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

.container {
  max-width: 1140px;
  margin: 0 auto;
}
</style>
