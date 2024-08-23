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
        <img
          :src="avatarUrl || 'default-avatar.jpg'"
          class="user-avatar"
          @click="goToAccount"
          alt="User Avatar"
        />
      </div>
    </nav>

    <!-- 我的账户信息 -->
    <section class="account-section">
      <div class="account-card">
        <h2>我的账户</h2>

        <!-- 基本信息 -->
        <div class="section-block">
          <h3>基本信息</h3>
          <div class="profile-container">
            <img
              :src="tempAvatarUrl || avatarUrl || 'default-avatar.jpg'"
              alt="Avatar"
              class="avatar-image"
              @click="isEditing ? changeAvatar() : ''"
              :class="{ clickable: isEditing, 'avatar-hover': isHovering }"
              @mouseover="handleMouseOver"
              @mouseleave="handleMouseLeave"
            />
            <div class="profile-details">
              <label>用户名:</label>
              <input
                type="text"
                v-model="editableUser.username"
                :readonly="!isEditing"
              />
              <label>性别:</label>
              <input
                type="text"
                v-model="editableUser.sex"
                :readonly="!isEditing"
              />
              <label>注册日期:</label>
              <p>{{ formatDate(user.registration_date) }}</p>
            </div>
          </div>
        </div>

        <!-- 联系信息 -->
        <div class="section-block">
          <h3>联系信息</h3>
          <label>邮箱:</label>
          <input
            type="email"
            v-model="editableUser.email"
            :readonly="!isEditing"
          />
          <label>电话号码:</label>
          <input
            type="text"
            v-model="editableUser.phone_number"
            :readonly="!isEditing"
          />
          <label>联系方式:</label>
          <input
            type="text"
            v-model="editableUser.tel"
            :readonly="!isEditing"
          />
          <label>地址:</label>
          <input
            type="text"
            v-model="editableUser.address"
            :readonly="!isEditing"
          />
        </div>

        <!-- 个人信息 -->
        <div class="section-block">
          <h3>个人信息</h3>
          <label>生日:</label>
          <input
            type="date"
            v-model="editableUserProfile.birthdate"
            :readonly="!isEditing"
          />
          <label>个人简介:</label>
          <textarea
            v-model="editableUserProfile.bio"
            :readonly="!isEditing"
          ></textarea>
        </div>

        <!-- 修改按钮 -->
        <div class="section-block">
          <button @click="toggleEditMode" class="btn btn-primary">
            {{ isEditing ? "取消修改" : "修改信息" }}
          </button>
          <button v-if="isEditing" @click="confirmSave" class="btn btn-success">
            确认保存
          </button>
        </div>

        <!-- 额外操作 -->
        <div class="section-block">
          <h3>账户操作</h3>
          <button @click="clearBrowsingHistory" class="btn btn-warning">
            清除浏览记录
          </button>
          <button @click="clearPurchaseHistory" class="btn btn-warning">
            清除购买记录
          </button>
          <button @click="confirmAccountDeletion" class="btn btn-danger">
            注销账号
          </button>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      user: {},
      userProfile: {},
      editableUser: {},
      editableUserProfile: {},
      isEditing: false,
      avatarUrl: null,
      tempAvatarUrl: null, // 临时存储新头像的URL
      isHovering: false, // 控制头像悬停效果
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    fetchUserInfo() {
      axios
        .get("http://localhost:8000/api/user/profile/")
        .then((response) => {
          this.user = response.data;
          this.userProfile = response.data.profile;
          this.editableUser = { ...this.user };
          this.editableUserProfile = { ...this.userProfile };
          this.avatarUrl = `http://localhost:8000${this.userProfile.avatar}`;
        })
        .catch((error) => {
          console.error("Failed to fetch user profile:", error);
        });
    },
    toggleEditMode() {
      this.isEditing = !this.isEditing;
    },
    confirmSave() {
      if (confirm("确定要保存修改吗？")) {
        this.saveChanges();
      }
    },
    saveChanges() {
      const formData = new FormData();
      if (this.tempAvatarFile) {
        formData.append("avatar", this.tempAvatarFile);
      }
      formData.append("username", this.editableUser.username);
      formData.append("sex", this.editableUser.sex);
      formData.append("email", this.editableUser.email);
      formData.append("phone_number", this.editableUser.phone_number);
      formData.append("tel", this.editableUser.tel);
      formData.append("address", this.editableUser.address);
      formData.append("profile.birthdate", this.editableUserProfile.birthdate);
      formData.append("profile.bio", this.editableUserProfile.bio);

      axios
        .patch("http://localhost:8000/api/user/profile/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.user = response.data;
          this.userProfile = response.data.profile;
          this.avatarUrl = `http://localhost:8000${this.userProfile.avatar}`;
          this.tempAvatarUrl = null;
          this.toggleEditMode();
        })
        .catch((error) => {
          console.error("Failed to save changes:", error);
        });
    },
    changeAvatar() {
      const fileInput = document.createElement("input");
      fileInput.type = "file";
      fileInput.accept = "image/*";
      fileInput.onchange = (event) => {
        const file = event.target.files[0];
        this.tempAvatarUrl = URL.createObjectURL(file);
        this.tempAvatarFile = file; // 保存文件以便后续上传
      };
      fileInput.click();
    },
    handleMouseOver() {
      if (this.isEditing) {
        this.isHovering = true;
      }
    },
    handleMouseLeave() {
      this.isHovering = false;
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: url("../assets/background.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
}

.navbar {
  /* Your existing navbar styles */
}

.account-section {
  flex: 1;
  padding: 2rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.account-card {
  background: rgba(255, 255, 255, 0.8);
  padding: 2rem;
  border-radius: 10px;
  max-width: 800px;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.section-block {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input[readonly],
textarea[readonly] {
  background-color: #f0f0f0;
  cursor: not-allowed;
}

input,
textarea {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.avatar-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.avatar-image.clickable {
  cursor: pointer;
  border: 2px solid #007bff;
}

.avatar-hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 123, 255, 0.5);
}

.profile-container {
  display: flex;
  align-items: center;
}

.profile-details {
  margin-left: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-success {
  background-color: #28a745;
  color: white;
}

.btn-warning {
  background-color: #ffc107;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}
</style>
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

/* 中间块 */
.center-block {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  margin-top: 2rem;
}

.center-content {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 10px;
  text-align: center;
  color: #333;
}

.center-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.center-content p {
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
  background: transparent;
}

/* 容器居中，设置最大宽度 */
.product-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1600px;
  flex-wrap: flex;
  gap: 20px;
}

/* 商品卡片容器 */
.product-card-container {
  flex: 0 1 300px;
}

/* 商品卡片样式 */
.product-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 10px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 420px;
}

.card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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
  margin-bottom: 0.5rem;
}

/* 推荐标签的样式 */
.recommended-label {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  border-radius: 0.25rem;
  margin-top: 0.5rem;
}

/* 星星评分样式 */
.product-score {
  margin-bottom: 1rem;
}

.star {
  color: #ffd700;
  font-size: 1.25rem;
}

/* 滑动控制按钮 */
.slider-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.slider-arrow {
  background-color: #007bff;
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  margin: 0 1rem;
}

.slider-arrow:hover {
  background-color: #0056b3;
}

/* 滑动条样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
}

.dot {
  width: 10px;
  height: 10px;
  background-color: #ddd;
  border-radius: 50%;
  margin: 0 5px;
  cursor: pointer;
}

.dot.active {
  background-color: #007bff;
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

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  max-width: 600px;
  width: 100%;
  text-align: center;
  overflow-y: auto;
  max-height: 80vh;
  backdrop-filter: blur(10px);
}

/* 模态框内容图片 */
.modal-image {
  max-width: 100%;
  height: auto;
  margin-bottom: 15px;
}

.modal-details {
  text-align: left;
}

.details-container {
  max-height: 150px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-bottom: 15px;
}

/* 动画效果 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
