<template>
  <div class="sub-header">
    <el-button type="primary" @click="goBack()">返回上一页</el-button>
    <h2 class="sub-title">{{ props.title }}</h2>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
  title: {
    type: String,
    default: ''
  }
})

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.sub-header {
  width: 100%;
  height: 40px;
  display: flex;
  align-items: center;
  background-color: rgb(64, 158, 255);
}

.sub-title {
  min-width: 1%;
  background-color: #fff;
  text-align: center;
  margin: 0px 0px 0px 20px;
  padding: 0px 15px;
  font-size: 20px;
  font-weight: 400;
  border-radius: 10px;
}
</style>
