<template>
  <div v-if="isVisible" class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <div class="modal-header">
        <slot name="header">
          <h3>模态框标题</h3>
        </slot>
        <button class="close-button" @click="closeModal">×</button>
      </div>
      <div class="modal-body">
        <slot name="body">模态框内容</slot>
      </div>
      <div class="modal-footer">
        <slot name="footer">
          <button class="btn btn-primary" @click="closeModal">关闭</button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isVisible: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
  watch: {
    isVisible(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.$refs.modal.classList.add("open");
        });
      } else {
        this.$refs.modal.classList.remove("open");
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modal {
  background: white;
  padding: 1.5rem;
  border-radius: 15px; /* 圆角效果 */
  max-width: 500px;
  width: 100%;
  z-index: 1001;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  transform: scale(0.9);
  transition: transform 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.modal-body {
  margin: 1rem 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.modal.open {
  opacity: 1;
  transform: scale(1);
}

.modal-overlay {
  opacity: 1;
}
</style>
