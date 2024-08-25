<template>
  <BaseTemplate>
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
          <!-- 注销账号按钮 -->
          <button @click="confirmDeleteAccount" class="btn btn-danger">
            注销账号
          </button>
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
      user: {},
      editableUser: {},
      editableUserProfile: {},
      isEditing: false,
      tempAvatarUrl: null, // 临时存储新头像的URL
      isHovering: false, // 控制头像悬停效果
      password1: "",
      password2: "",
      errorMessage: "",
    };
  },
  mounted() {
    this.fetchUserInfo();
  },
  methods: {
    // 账户注销确认提示
    confirmDeleteAccount() {
      this.password1 = prompt("请输入密码以确认注销账号：", "");
      this.password2 = prompt("请再次输入密码以确认注销账号：", "");

      if (this.password1 === null || this.password2 === null) {
        this.errorMessage = "操作已取消";
        return;
      }

      if (this.password1 !== this.password2) {
        alert("两次输入的密码不一致，请重试");
        return;
      }

      if (confirm("您确定要注销您的账号吗？此操作无法撤销！")) {
        this.deleteAccount();
      }
    },

    deleteAccount() {
      axios
        .post("http://localhost:8000/api/user/delete-account/", {
          password: this.password1,
        })
        .then(() => {
          // 清除本地存储中的 token
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");

          // 强制刷新页面清除缓存
          location.reload();
        })
        .catch((error) => {
          this.errorMessage = error.response.data.error || "注销失败，请重试";
          alert(this.errorMessage);
        });
    },

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

      // 将用户基本信息添加到formData
      formData.append("username", this.editableUser.username);
      formData.append("sex", this.editableUser.sex);
      formData.append("email", this.editableUser.email);
      formData.append("phone_number", this.editableUser.phone_number);
      formData.append("tel", this.editableUser.tel);
      formData.append("address", this.editableUser.address);

      // 将profile相关的字段添加到formData中
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
/* 与之前相同的样式 */
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
