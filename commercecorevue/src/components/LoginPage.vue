<template>
  <div class="container mt-5">
    <h1 class="mb-4">登录</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">用户名</label>
        <input
          type="text"
          v-model="username"
          class="form-control"
          id="username"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input
          type="password"
          v-model="password"
          class="form-control"
          id="password"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">登录</button>
      <div v-if="error" class="text-danger mt-3">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/login/", {
          username: this.username,
          password: this.password,
        });
        // 存储Token到本地存储
        localStorage.setItem("token", response.data.token);
        // 重定向到主页
        this.$router.push("/");
      } catch (error) {
        this.error = "用户名或密码不正确";
      }
    },
  },
};
</script>
