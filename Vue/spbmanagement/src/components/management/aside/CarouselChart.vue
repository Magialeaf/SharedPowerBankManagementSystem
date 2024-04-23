<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="ifAddNew = !ifAddNew">{{
        ifAddNew ? '返回轮播图列表' : '添加轮播图'
      }}</el-button>
    </div>
    <div v-if="!ifAddNew" class="right-operation">
      <div class="search-area">
        <Search @search="handleSearch" searchTip="搜索名称" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNew" class="carousel-chart-list">
    <ChartList :chartData="chartList" />
    <div class="pagination">
      <Pagination :pageInfo="chartStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <AddNewChart v-else />
</template>

<script setup>
import Search from '@/components/management/utils/Search.vue'
import ChartList from '@/components/management/carouselChart/ChartList.vue'
import AddNewChart from '@/components/management/carouselChart/AddNewChart.vue'
import { computed, onBeforeMount, ref } from 'vue'
import { useCarouselChartStore } from '@/stores/carouselChartStore'

const chartStore = useCarouselChartStore()
const ifAddNew = ref(false)
const searchKey = ref({
  keyword: ''
})

const chartList = computed(() => chartStore.getList())

onBeforeMount(() => initList())

function initList() {
  chartStore
    .initCarouselChartList()
    .then((res) => {})
    .catch((e) => {})
}

function handleSearch(keyword) {
  searchKey.value.keyword = keyword
  chartStore
    .getCarouselChartList(1, {
      keyword: searchKey.value.keyword
    })
    .then()
    .catch()
}

function handlePageChange(page) {
  if (searchKey.value) {
    chartStore
      .getCarouselChartList(page, {
        keyword: searchKey.value.keyword
      })
      .then()
      .catch()
  } else {
    chartStore
      .getCarouselChartList(page)
      .then((res) => {})
      .catch((e) => {})
  }
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

.carousel-chart-list {
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
