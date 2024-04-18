<template>
  <label class="search">
    <el-input v-model="searchKeyword" placeholder="请输入关键词进行搜索" />
    <el-button type="info" @click="handleSearch"
      ><el-icon
        ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" data-v-ea893728="">
          <path
            fill="currentColor"
            d="m795.904 750.72 124.992 124.928a32 32 0 0 1-45.248 45.248L750.656 795.904a416 416 0 1 1 45.248-45.248zM480 832a352 352 0 1 0 0-704 352 352 0 0 0 0 704"
          ></path></svg></el-icon
    ></el-button>
  </label>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import { lockFunction } from '@/utils/myLock'

const emits = defineEmits(['search'])

const searchKeyword = ref('')

const handleSearch = lockFunction(1000)(() => {
  emits('search', searchKeyword.value)
})
</script>

<style scoped>
.search {
  display: flex;
  justify-content: center;
}
</style>
