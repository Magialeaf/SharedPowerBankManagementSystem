<template>
  <el-table
    :data="noticeList"
    stripe
    border
    @filter-change="handleFilter"
    @sort-change="handleSort"
  >
    <el-table-column class="table-column" min-width="5%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="10%" prop="title" label="标题" />
    <el-table-column class="table-column" min-width="12%" label="图片">
      <template v-slot="scope">
        <img :src="scope.row.img" alt="图片" style="width: 100px; height: 100px" />
      </template>
    </el-table-column>
    <el-table-column class="table-column" min-width="15%" prop="content" label="内容" />
    <el-table-column
      class="table-column"
      column-key="type"
      :filters="typeList"
      :filter-multiple="false"
      min-width="10%"
      prop="type_name"
      label="类型"
    />
    <el-table-column class="table-column" min-width="5%" prop="uid" label="发布者用户id" />
    <el-table-column class="table-column" min-width="9%" prop="uid_name" label="发布者用户名" />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="10%"
      prop="create_time"
      label="创建时间"
    />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="10%"
      prop="update_time"
      label="更新时间"
    />

    <el-table-column min-width="14%" label="操作">
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
import { useNoticeStore, useNoticeConfigStore } from '@/stores/noticeStore'
import NoticeOperation from '@/components/management/notice/NoticeOperation.vue'

const noticeStore = useNoticeStore()
const noticeConfigStore = useNoticeConfigStore()

const noticeList = computed(() => prop.noticeData)
const typeList = computed(() =>
  Object.entries(noticeConfigStore.showList()).map(([value, text]) => ({
    text,
    value: parseInt(value)
  }))
)

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

const emits = defineEmits(['filter-type', 'sort-by'])

function handleFilter(filters) {
  emits('filter-type', filters.type[0])
}

function handleSort(sort) {
  const { prop, order } = sort
  if (order === 'ascending') {
    emits('sort-by', `${prop}`)
  } else {
    emits('sort-by', `-${prop}`)
  }
}
</script>

<style scoped></style>
