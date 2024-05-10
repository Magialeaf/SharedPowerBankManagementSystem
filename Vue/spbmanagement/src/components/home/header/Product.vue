<template>
  <div class="operation">
    <div class="search-SPB">
      <SelectAddress
        tip="搜索"
        :codeList="codeList"
        :areaOption="selectArea"
        @select-area="handleSelectArea"
        @clear-code-list="handleClearCodeList"
      />
      <div style="margin-right: 10px"></div>
      <Search @search="handleSearch" searchTip="搜素充电宝名称、商户名称" />
    </div>
  </div>
  <div class="content-box">
    <ProductCards :data="powerBankList" />
  </div>
  <div class="pagination">
    <Pagination
      :pageInfo="powerBankStore.getPageInfo()"
      @page-change="handlePageChange"
      :ifGoTop="false"
    />
  </div>
</template>

<script setup>
import { ref, onBeforeMount, computed, watch, nextTick } from 'vue'
import { useSPBStore } from '@/stores/SPBStore.js'
import { lockFunction } from '@/utils/myLock'
import Search from '@/components/management/utils/Search.vue'
import ProductCards from '@/components/home/product/ProductCards.vue'
import Pagination from '@/components/management/utils/Pagination.vue'
import SelectAddress from '@/components/management/utils/SelectAddress.vue'

const codeList = ref(['00', '0000', '000000'])
const searchKey = ref({
  keyword: '',
  keyAreaId: ''
})
const selectArea = ref('')

const powerBankStore = useSPBStore()

const powerBankList = computed(() => powerBankStore.showList())

onBeforeMount(() => initList())

watch(selectArea, () => {
  searchKey.value.keyAreaId = selectArea.value
  powerBankStore
    .getList(1, {
      keyword: searchKey.value.keyword,
      keyAreaId: searchKey.value.keyAreaId
    })
    .then((res) => {})
    .catch((e) => {})
})

function initList() {
  powerBankStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
}

function handlePageChange(page) {
  if (searchKey.value) {
    powerBankStore
      .getList(page, {
        keyword: searchKey.value.keyword,
        keyAreaId: searchKey.value.keyAreaId
      })
      .then((res) => {
        nextTick(() => {
          window.scrollTo({ top: 300, behavior: 'smooth' }) // 执行平滑滚动
        })
      })
      .catch((e) => {})
  } else {
    powerBankStore
      .getList(page)
      .then((res) => {
        nextTick(() => {
          window.scrollTo({ top: 300, behavior: 'smooth' }) // 执行平滑滚动
        })
      })
      .catch((e) => {})
  }
}

function handleSearch(keyword) {
  searchKey.value.keyword = keyword
  powerBankStore
    .getList(1, {
      keyword: searchKey.value.keyword,
      keyAreaId: searchKey.value.keyAreaId
    })
    .then()
    .catch()
}

function handleSelectArea(value) {
  selectArea.value = value
}

const handleClearCodeList = lockFunction(1000)(() => {
  codeList.value = ['00', '0000', '000000']
  selectArea.value = null
})
</script>

<style scoped>
.operation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-SPB {
  width: 100%;
  display: flex;
  justify-content: center;
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
