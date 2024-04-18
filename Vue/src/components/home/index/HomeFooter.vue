<template>
  <div class="footer" ref="footerElement">
    <div class="footerContent">
      <p>&copy; {{ systemName }}</p>
      <!--<p>&copy; {{ startYear }} - {{ endYear }} By {{ author }}</p>-->
      <p>版本: {{ version }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted, onBeforeUnmount } from 'vue'

const startYear = 2024
const endYear = new Date().getFullYear()
const author = 'Magialeaf'
const systemName = '共享充电宝管理系统'
const version = 'V1.0'

const footerElement = ref(null)

function handleMouseOver() {
  if (footerElement.value) {
    footerElement.value.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.3)'
  }
}

function handleMouseLeave() {
  if (footerElement.value) {
    footerElement.value.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)'
  }
}

// 在挂载完成后添加事件监听器
onMounted(() => {
  footerElement.value.addEventListener('mouseover', handleMouseOver)
  footerElement.value.addEventListener('mouseleave', handleMouseLeave)

  // 当组件卸载时，移除事件监听器以防止内存泄漏
  onBeforeUnmount(() => {
    footerElement.value.removeEventListener('mouseover', handleMouseOver)
    footerElement.value.removeEventListener('mouseleave', handleMouseLeave)
  })
})
</script>

<style scoped>
.footer {
  width: 100%;
  height: 100px;
  background-color: #ffffff;
  color: #000000;
  border: 3px solid rgba(204, 204, 204, 0.5);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.footerContent {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}
</style>
