<template>
  <BaseTemplate>
    <!-- 设置内容 -->
    <section class="settings-section">
      <h2>账户设置</h2>
      <form @submit.prevent="updateSettings">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="settings.username"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            type="email"
            id="email"
            v-model="settings.email"
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="settings.password"
            class="form-control"
          />
        </div>
        <button type="submit" class="btn btn-primary">保存更改</button>
      </form>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      settings: {
        username: "",
        email: "",
        password: "",
      },
    };
  },
  mounted() {
    this.fetchSettings();
  },
  methods: {
    fetchSettings() {
      axios
        .get("http://localhost:8000/api/user/settings/")
        .then((response) => {
          this.settings = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch settings:", error);
        });
    },
    updateSettings() {
      axios
        .post("http://localhost:8000/api/user/settings/", this.settings)
        .then(() => {
          alert("设置已更新");
        })
        .catch((error) => {
          console.error("Failed to update settings:", error);
        });
    },
  },
};
</script>

<style scoped>
/* 设置内容 */
.settings-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  max-width: 600px;
  margin: 20px auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
