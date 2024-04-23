<template>
  <el-table :data="chartList" stripe border>
    <el-table-column class="table-column" min-width="10%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="15%" prop="title" label="标题" />
    <el-table-column class="table-column" min-width="15%" label="轮播图">
      <template #default="{ row }">
        <img :src="row.img" alt="用户头像" style="max-width: 48px; max-height: 48px" />
      </template>
    </el-table-column>
    <el-table-column class="table-column" min-width="15%" prop="create_time" label="创建时间" />
    <el-table-column class="table-column" min-width="15%" prop="update_time" label="修改时间" />
    <el-table-column
      class="table-column"
      min-width="10%"
      prop="active"
      label="状态"
      :formatter="formatActiveStatus"
    />
    <el-table-column min-width="20%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <ChartOperation v-if="drawer" :id="selectedId"
  /></el-drawer>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue'
import ChartOperation from '@/components/management/carouselChart/ChartOperation.vue'

const chartList = computed(() => props.chartData)
const drawer = ref(false)
const selectedId = ref(-1)

const props = defineProps({
  chartData: { type: Array, required: true }
})

function showDetails(row) {
  selectedId.value = row.id // 获取当前点击行的 uid
  drawer.value = true // 打开抽屉
}

function formatActiveStatus(row) {
  return row.active === 1 ? '启用' : '禁用'
}
</script>

<style scoped></style>
