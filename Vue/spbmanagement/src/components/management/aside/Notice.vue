<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewNotice">{{
        ifAddNewNotice ? '公告列表' : '新增公告记录'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewNotice" class="right-operation">
      <div class="search-notice"></div>
    </div>
  </div>
  <div v-if="!ifAddNewNotice" class="notice-list">
    <NoticeList :noticeData="noticeList" />
    <div class="pagination">
      <Pagination :pageInfo="noticeStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <NoticeOperation :ifNew="true" v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import { useNoticeStore } from '@/stores/noticeStore'
import { lockFunction } from '@/utils/myLock'
import Pagination from '@/components/management/utils/Pagination.vue'
import NoticeList from '@/components/management/notice/NoticeList.vue'
import NoticeOperation from '@/components/management/notice/NoticeOperation.vue'

const ifAddNewNotice = ref(false)

const searchKey = ref({
  power_bank: '',
  user: ''
})

const noticeStore = useNoticeStore()
const noticeList = computed(() => noticeStore.showList())

onBeforeMount(() => initList())

function initList() {
  noticeStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
}

function switchAddNewNotice() {
  ifAddNewNotice.value = !ifAddNewNotice.value
  if (!ifAddNewNotice.value) {
    noticeStore.initList()
  }
}

function handlePageChange(page) {
  if (searchKey.value) {
    noticeStore
      .getList(page, searchKey.value)
      .then((res) => {})
      .catch((e) => {})
  } else {
    noticeStore
      .getList(page)
      .then((res) => {})
      .catch((e) => {})
  }
}

function clearSearch() {
  Object.keys(searchKey.value).forEach((key) => {
    searchKey.value[key] = ''
  })
  handleSearch()
}

function handleSearch() {
  noticeStore
    .getList(1, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}
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

.search-Notice {
  width: 60%;
  display: flex;
}

.search-btn {
  margin-right: 10px;
}

.notice-list {
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
