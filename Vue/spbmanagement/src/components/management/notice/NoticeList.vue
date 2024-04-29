<template>
  <el-table :data="noticeList" stripe border>
    <el-table-column class="table-column" min-width="10%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="10%" prop="title" label="标题" />
    <el-table-column class="table-column" min-width="20%" prop="content" label="内容" />
    <el-table-column class="table-column" min-width="10%" prop="type_name" label="类型" />
    <el-table-column class="table-column" min-width="15%" prop="create_time" label="创建时间" />
    <el-table-column class="table-column" min-width="15%" prop="update_time" label="更新时间" />

    <el-table-column min-width="20%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <NoticeOperation v-if="drawer" :id="selectedId" :ifNew="false"
  /></el-drawer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
import { useNoticeStore } from '@/stores/noticeStore'
import NoticeOperation from '@/components/management/notice/NoticeOperation.vue'

const noticeStore = useNoticeStore()

const noticeList = computed(() => prop.noticeData)

const drawer = ref(false)
const selectedId = ref(undefined)

const prop = defineProps({
  noticeData: {
    type: Array
  }
})

function showDetails(row) {
  selectedId.value = row.id
  drawer.value = true // 打开抽屉
}

function deleteRow(row) {
  $confirmDeleteMsg('确定删除充电宝吗?')
    .then(() => {
      noticeStore.deleteInfo(row.id)
    })
    .catch(() => {
      $errorMsg('取消删除')
    })
}
</script>

<style scoped></style>
