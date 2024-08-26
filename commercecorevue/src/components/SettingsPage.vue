<template>
  <BaseTemplate>
    <!-- 开发者模式切换 -->
    <section class="developer-mode-section">
      <h2>开发者模式</h2>
      <div class="form-group">
        <label for="developerKey">输入开发者秘钥</label>
        <input
          type="password"
          id="developerKey"
          v-model="developerKey"
          class="form-control"
          placeholder="输入开发者秘钥..."
        />
      </div>
      <button @click="toggleDeveloperMode" class="btn btn-primary">确认</button>
    </section>

    <!-- 开发者模式内容 -->
    <section v-if="isDeveloperMode" class="mysql-shell-section">
      <h2>MySQL Shell</h2>
      <form @submit.prevent="executeQuery">
        <div class="form-group">
          <label for="sqlQuery">输入 SQL 查询</label>
          <textarea
            id="sqlQuery"
            v-model="sqlQuery"
            class="form-control"
            rows="5"
            placeholder="输入 SQL 查询..."
          ></textarea>
        </div>
        <button type="submit" class="btn btn-primary">执行查询</button>
      </form>
      <div v-if="queryResult" class="query-result">
        <h3>查询结果</h3>
        <table class="table">
          <thead>
            <tr>
              <th v-for="(header, index) in queryResult.headers" :key="index">
                {{ header }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in queryResult.rows" :key="index">
              <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                {{ cell }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>尚无查询结果。</p>
      </div>
    </section>

    <!-- 非开发者模式内容 -->
    <section v-else class="settings-section">
      <h2>设置</h2>
      <p>暂无设置选项。</p>
    </section>
  </BaseTemplate>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie";

export default {
  data() {
    return {
      developerKey: "",
      isDeveloperMode: false,
      sqlQuery: "SHOW TABLES;", // 默认查询所有表
      queryResult: null,
    };
  },
  methods: {
    toggleDeveloperMode() {
      const correctKey = "1350989414";
      this.isDeveloperMode = this.developerKey === correctKey;
      if (!this.isDeveloperMode) {
        alert("开发者秘钥错误！");
      }
    },
    executeQuery() {
      if (!this.isDeveloperMode) return;

      axios
        .post(
          "http://localhost:8000/api/mysql-shell/",
          { query: this.sqlQuery }, // 这里确保 query 被正确传递
          {
            headers: {
              "X-CSRFToken": Cookies.get("csrftoken"), // 添加CSRF令牌
            },
          }
        )
        .then((response) => {
          this.queryResult = response.data;
        })
        .catch((error) => {
          console.error("Failed to execute query:", error);
          alert("执行查询时发生错误");
        });
    },
  },
};
</script>

<style scoped>
.mysql-shell-section,
.settings-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  max-width: 800px;
  margin: 20px auto;
}

.developer-mode-section {
  padding: 20px;
  background: rgba(240, 240, 240, 0.9);
  border-radius: 10px;
  max-width: 800px;
  margin: 20px auto;
  margin-bottom: 20px;
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

.query-result {
  margin-top: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f2f2f2;
}
</style>
