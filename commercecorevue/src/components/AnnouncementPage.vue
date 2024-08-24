<template>
  <BaseTemplate>
    <!-- 公告内容 -->
    <section class="announcement-section">
      <h2>最新公告</h2>
      <div class="announcement-list">
        <div
          class="announcement-item"
          v-for="announcement in announcements"
          :key="announcement.id"
        >
          <h3>{{ announcement.title }}</h3>
          <p>{{ announcement.content }}</p>
          <p class="announcement-date">
            {{ formatDate(announcement.updated_at) }}
          </p>
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
      announcements: [], // 公告列表
    };
  },
  mounted() {
    this.fetchAnnouncements();
  },
  methods: {
    fetchAnnouncements() {
      axios
        .get("http://localhost:8000/api/announcements/")
        .then((response) => {
          this.announcements = response.data;
        })
        .catch((error) => {
          console.error("Failed to fetch announcements:", error);
        });
    },
    formatDate(dateString) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
  },
};
</script>

<style scoped>
/* 公告内容 */
.announcement-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  max-width: 800px;
  margin: 20px auto;
}

.announcement-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.announcement-item {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.announcement-item h3 {
  margin-bottom: 10px;
  font-size: 1.25rem;
}

.announcement-item p {
  margin-bottom: 5px;
}

.announcement-date {
  font-size: 0.875rem;
  color: #6c757d;
  text-align: right;
}
</style>
