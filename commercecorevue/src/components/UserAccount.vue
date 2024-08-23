<template>
  <div class="account-container">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <ul class="sidebar-menu">
        <li @click="currentSection = 'profile'">个人信息</li>
        <li @click="currentSection = 'password'">修改密码</li>
        <li @click="currentSection = 'address'">设置地址</li>
        <!-- 其他功能 -->
      </ul>
    </aside>

    <!-- 主内容区域 -->
    <section class="content">
      <!-- 返回上一页面按钮 -->
      <button @click="goBack" class="btn btn-secondary">返回上一页</button>

      <!-- 仅在 user 和 user.profile 对象存在时渲染内容 -->
      <div v-if="user && user.profile && currentSection === 'profile'">
        <h2>个人信息</h2>
        <form @submit.prevent="updateUser">
          <div class="form-group">
            <label for="username">用户名</label>
            <input
              type="text"
              id="username"
              class="form-control"
              v-model="user.username"
              disabled
            />
          </div>
          <div class="form-group">
            <label for="email">邮箱</label>
            <input
              type="email"
              id="email"
              class="form-control"
              v-model="user.email"
            />
          </div>
          <div class="form-group">
            <label for="avatar">头像</label>
            <input type="file" id="avatar" @change="onFileChange" />
          </div>
          <div class="form-group">
            <label for="birthdate">生日</label>
            <input
              type="date"
              id="birthdate"
              class="form-control"
              v-model="user.profile.birthdate"
            />
          </div>
          <div class="form-group">
            <label for="bio">个人简介</label>
            <textarea
              id="bio"
              class="form-control"
              v-model="user.profile.bio"
            ></textarea>
          </div>
          <button type="submit" class="btn btn-primary">更新信息</button>
        </form>
      </div>

      <div v-else-if="currentSection === 'password'">
        <h2>修改密码</h2>
        <!-- 修改密码表单 -->
      </div>

      <div v-else-if="currentSection === 'address'">
        <h2>设置地址</h2>
        <!-- 设置地址表单 -->
      </div>

      <div v-else>
        <p>加载中...</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentSection: "profile",
      user: {
        username: "",
        email: "",
        profile: {
          birthdate: null,
          bio: "",
          avatar: null,
        },
      },
      error: "",
      avatar: null, // 保存选中的头像文件
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    async fetchUserData() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/user/profile/",
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        // 确保响应数据结构和预期的一致
        this.user = {
          username: response.data.username,
          email: response.data.email,
          profile: response.data.profile || {
            birthdate: null,
            bio: "",
            avatar: null,
          },
        };
      } catch (error) {
        console.error("Error fetching user data:", error);
        this.error = "无法加载用户信息，请重试";
      }
    },
    async updateUser() {
      try {
        const token = localStorage.getItem("token");
        const formData = new FormData();
        formData.append("email", this.user.email);
        formData.append("profile.birthdate", this.user.profile.birthdate);
        formData.append("profile.bio", this.user.profile.bio);
        if (this.avatar) {
          formData.append("profile.avatar", this.avatar);
        }

        const response = await axios.patch(
          "http://127.0.0.1:8000/api/user/profile/",
          formData,
          {
            headers: {
              Authorization: `Token ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
        this.user = response.data || { profile: {} };
        alert("用户信息更新成功！");
      } catch (error) {
        console.error("Error updating user data:", error);
        this.error = "无法更新用户信息，请重试";
      }
    },
    onFileChange(event) {
      this.avatar = event.target.files[0];
    },
    goBack() {
      this.$router.go(-1); // 返回上一页面
    },
  },
};
</script>

<style scoped>
.account-container {
  display: flex;
  margin-top: 20px;
}

.sidebar {
  width: 200px;
  background-color: #f8f9fa;
  padding: 15px;
  border-right: 1px solid #ddd;
}

.sidebar-menu {
  list-style: none;
  padding: 0;
}

.sidebar-menu li {
  padding: 10px 0;
  cursor: pointer;
}

.sidebar-menu li:hover {
  background-color: #007bff;
  color: white;
}

.content {
  flex-grow: 1;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.btn-primary {
  width: 100%;
}

.btn-secondary {
  margin-bottom: 15px;
}
</style>
