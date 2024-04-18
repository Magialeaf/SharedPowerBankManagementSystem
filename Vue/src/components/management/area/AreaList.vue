<template>
    <el-table :data="areaList" stripe border>
      <el-table-column class="table-column" min-width="10%" prop="id" label="id" />
      <el-table-column class="table-column" min-width="20%" prop="codeName" label="区域" />
      <el-table-column class="table-column" min-width="20%" prop="name" label="区域名称" />
      <el-table-column class="table-column" min-width="25%" prop="description" label="区域描述" />
      <el-table-column class="table-column" min-width="10%" prop="latitude" label="纬度" />
      <el-table-column class="table-column" min-width="10%" prop="longitude" label="经度" />
  
      <el-table-column min-width="20%" label="操作">
        <template v-slot="scope">
          <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
          <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  
    <el-drawer v-model="drawer" size="50%" :with-header="false">
      <AreaOperation v-if="drawer" :id="selectedId"
    /></el-drawer>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import AreaOperation from '@/components/management/area/AreaOperation.vue'
  import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
  import { useAreaStore } from '@/stores/areaStore'
  
  const areaStore = useAreaStore()
  
  const areaList = ref(
    computed(() => {
      return prop.areaData
    })
  )
  
  const drawer = ref(false)
  const selectedId = ref(undefined)
  
  const prop = defineProps({
    areaData: {
      type: Array
    }
  })
  
  function showDetails(row) {
    selectedId.value = row.id
    drawer.value = true // 打开抽屉
  }
  
  function deleteRow(row) {
    $confirmDeleteMsg('确定删除该区域吗?')
      .then(() => {
        areaStore.deleteArea(row.id)
      })
      .catch(() => {
        $errorMsg('取消删除')
      })
  }
  </script>
  
  <style scoped></style>
  