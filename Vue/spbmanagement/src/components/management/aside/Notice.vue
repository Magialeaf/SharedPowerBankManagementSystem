<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewNotice">{{
        ifAddNewNotice ? '公告列表' : '新增公告记录'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewNotice" class="right-operation">
      <div class="search-tip">搜索</div>
      <div class="search-input">
        <Search @search="handleSearch" searchTip="搜素标题、内容、发布者名字" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNewNotice" class="notice-list">
    <NoticeList :noticeData="noticeList" @filter-type="handleFilterType" @sort-by="handleSortBy" />
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
import Search from '@/components/management/utils/Search.vue'
import Pagination from '@/components/management/utils/Pagination.vue'
import NoticeList from '@/components/management/notice/NoticeList.vue'
import NoticeOperation from '@/components/management/notice/NoticeOperation.vue'

const ifAddNewNotice = ref(false)

const searchKey = ref({
  keyword: '',
  type: null,
  order_by: []
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

function handleSearch(value) {
  searchKey.value.keyword = value
  noticeStore
    .getList(1, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}

function handleFilterType(value) {
  searchKey.value.type = value
  noticeStore
    .getList(noticeStore.getPageInfo().currentPage, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}

function handleSortBy(value) {
  searchKey.value.order_by = [value]
  noticeStore
    .getList(noticeStore.getPageInfo().currentPage, searchKey.value)
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
  justify-content: flex-start;
  align-items: center;
}

.search-tip {
  height: 100%;
  font-size: 14px;
  margin-right: 10px;
}

.search-notice {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.search-input {
  width: 30%;
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
