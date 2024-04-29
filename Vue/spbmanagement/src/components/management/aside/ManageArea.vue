<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewArea">{{
        ifAddNewArea ? '区域列表' : '新增和更新区域'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewArea" class="right-operation">
      <div class="search-area">
        <SelectArea tip="搜索" :codeList="codeList" @areaSelected="handleSelect" />
        <el-button class="search-btn" type="primary" @click="clearCode()">清空</el-button>
        <Search @search="handleSearch" searchTip="搜索名称、描述" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNewArea" class="area-list">
    <AreaList :areaData="areaList" />
    <div class="pagination">
      <Pagination :pageInfo="areaStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <AddNewArea v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import { useAreaStore } from '@/stores/areaStore.js'
import Search from '@/components/management/utils/Search.vue'
import SelectArea from '@/components/management/utils/SelectArea.vue'
import AreaList from '@/components/management/area/AreaList.vue'
import AddNewArea from '@/components/management/area/AddNewArea.vue'
import Pagination from '@/components/management/utils/Pagination.vue'
import { lockFunction } from '@/utils/myLock'

const ifAddNewArea = ref(false)
const codeList = ref(['00', '0000', '000000'])
const searchKey = ref({
  keyword: '',
  keycode: ''
})
const areaStore = useAreaStore()

const areaList = computed(() => areaStore.getList())

onBeforeMount(() => initList())

function initList() {
  areaStore
    .initAreaList()
    .then((res) => {})
    .catch((e) => {})
}

function switchAddNewArea() {
  ifAddNewArea.value = !ifAddNewArea.value
  if (ifAddNewArea.value === false) {
    areaStore
      .getAreaList(areaStore.getPageInfo().currentPage)
      .then((res) => {})
      .catch((e) => {})
  }
}

function handlePageChange(page) {
  if (searchKey.value) {
    areaStore
      .getAreaList(page, searchKey.value)
      .then((res) => {})
      .catch((e) => {})
  } else {
    areaStore
      .getAreaList(page)
      .then((res) => {})
      .catch((e) => {})
  }
}

function handleSearch(keyword) {
  searchKey.value.keyword = keyword
  areaStore
    .getAreaList(1, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}

function handleSelect(lst) {
  codeList.value = lst[0]
  searchKey.value.keycode = lst[0][2]
  areaStore
    .getAreaList(1, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}

const clearCode = lockFunction(1000)(() => {
  codeList.value = ['00', '0000', '000000']
  searchKey.value.keycode = ''
  areaStore
    .getAreaList(1, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
})
</script>

<style scoped>
.operation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.left-operation {
  width: 15%;
}

.right-operation {
  width: 80%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-area {
  display: flex;
}

.search-btn {
  margin-right: 10px;
}

.area-list {
  display: flex;
  min-height: 560px;
  flex-direction: column;
  justify-content: center;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 10px;
}
</style>
