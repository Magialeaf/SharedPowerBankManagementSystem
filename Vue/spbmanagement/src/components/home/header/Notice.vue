<template>
  <div class="operation">
    <div class="search-notice">
      <div class="search-tip">搜索</div>
      <div class="search-input">
        <Search @search="handleSearch" searchTip="搜素标题、内容、发布者名字" />
      </div>
    </div>
  </div>
  <div class="content-box">
    <NoticeCards :data="noticeList" />
  </div>
  <div class="pagination">
    <Pagination
      :pageInfo="noticeStore.getPageInfo()"
      @page-change="handlePageChange"
      :ifGoTop="false"
    />
  </div>
</template>

<script setup>
import { ref, onBeforeMount, computed, nextTick } from 'vue'
import { useNoticeStore } from '@/stores/noticeStore'
import { lockFunction } from '@/utils/myLock'
import Pagination from '@/components/management/utils/Pagination.vue'
import NoticeCards from '@/components/home/notice/NoticeCards.vue'

const searchKey = ref({
  keyword: ''
})

const noticeStore = useNoticeStore()
const noticeList = computed(() => noticeStore.showList())

onBeforeMount(() => initList())

function initList() {
  noticeStore
    .getList(1, { order_by: ['-update_time'] })
    .then((res) => {})
    .catch((e) => {})
}

function handlePageChange(page) {
  if (searchKey.value) {
    noticeStore
      .getList(page, searchKey.value)
      .then((res) => {
        nextTick(() => {
          window.scrollTo({ top: 300, behavior: 'smooth' }) // 执行平滑滚动
        })
      })
      .catch((e) => {})
  } else {
    noticeStore
      .getList(page)
      .then((res) => {
        nextTick(() => {
          window.scrollTo({ top: 300, behavior: 'smooth' }) // 执行平滑滚动
        })
      })
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
</script>

<style scoped>
.operation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  width: 25%;
}

.search-btn {
  margin-right: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 10px;
}
</style>
