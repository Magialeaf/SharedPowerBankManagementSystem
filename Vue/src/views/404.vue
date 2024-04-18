<template>
  <div class="not-found-page">
    <h1 class="title">很抱歉，您访问的页面不存在</h1>

    <div class="actions">
      <el-button type="primary" @click="goHome"> 返回首页 </el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.not-found-page {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  width: 95%;
  margin-left: 5%;
  height: 100vh;
  text-align: center;
  background: url('@/assets/img/home/404.png') no-repeat center center / cover;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-top: 140px;
}

.actions {
  display: flex;
  margin-top: 40px;
  margin-right: 20px;
}
</style>
