<template>
  <BaseTemplate>
    <!-- 帮助内容 -->
    <section class="help-section">
      <h2>帮助中心</h2>
      <div class="help-content">
        <h3>常见问题</h3>
        <ul class="faq-list">
          <li>
            <strong>问:</strong> 如何重置密码？<br /><strong>答:</strong>
            点击"忘记密码"链接，并按照指示操作。
          </li>
          <li>
            <strong>问:</strong> 如何联系客户支持？<br /><strong>答:</strong>
            您可以通过电子邮件或电话与我们联系。详情请参见下文。
          </li>
          <li>
            <strong>问:</strong> 订单发货需要多长时间？<br /><strong
              >答:</strong
            >
            通常情况下，订单将在1-3个工作日内发货。
          </li>
        </ul>

        <h3>联系我们</h3>
        <p>您可以通过以下方式联系我们：</p>
        <ul>
          <li>电子邮件: 1350989414@qq.com</li>
          <li>电话: 暂无</li>
        </ul>
      </div>
    </section>
  </BaseTemplate>
</template>

<script>
import BaseTemplate from "./BaseTemplate.vue";

export default {
  data() {
    return {};
  },
  mounted() {},
  methods: {},
  components: { BaseTemplate },
};
</script>

<style scoped>
/* 帮助内容 */
.help-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  max-width: 800px;
  margin: 20px auto;
}

.help-content h3 {
  margin-top: 20px;
  font-size: 1.5rem;
}

.faq-list {
  list-style: none;
  padding: 0;
}

.faq-list li {
  margin-bottom: 15px;
}
</style>
