<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewMerchant">{{
        ifAddNewMerchant ? '商户列表' : '新增商户'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewMerchant" class="right-operation">
      <div class="search-merchant">
        <SelectArea tip="搜索" :codeList="codeList" @merchantSelected="handleSelect" />
        <el-button class="search-btn" type="primary" @click="clearCode()">清空</el-button>
        <Search @search="handleSearch" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNewMerchant" class="merchant-list">
    <MerchantList :merchantData="merchantList" />
    <div class="pagination">
      <Pagination :pageInfo="merchantStore.getPageInfo()" @pageChange="handlePageChange" />
    </div>
  </div>
  <AddNewMerchant v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import { useMerchantStore } from '@/stores/merchantStore.js'
import Search from '@/components/management/utils/Search.vue'
import SelectArea from '@/components/management/utils/SelectArea.vue'
import MerchantList from '@/components/management/merchant/MerchantList.vue'
import AddNewMerchant from '@/components/management/merchant/AddNewMerchant.vue'
import Pagination from '@/components/management/utils/Pagination.vue'
import { lockFunction } from '@/utils/myLock'

const ifAddNewMerchant = ref(false)
const codeList = ref(['00', '0000', '000000'])
const searchKey = ref({
  keyword: '',
  keycode: ''
})
const merchantStore = useMerchantStore()

const merchantList = computed(() => merchantStore.getList())

onBeforeMount(() => initList())

function initList() {
  merchantStore
    .initMerchantList()
    .then((res) => {})
    .catch((e) => {})
}

function switchAddNewMerchant() {
  ifAddNewMerchant.value = !ifAddNewMerchant.value
  if (ifAddNewMerchant.value === false) {
    merchantStore
      .getMerchantList(merchantStore.getPageInfo().currentPage)
      .then((res) => {})
      .catch((e) => {})
  }
}

function handlePageChange(page) {
  merchantStore.getPageInfo().currentPage = page
  if (searchKey.value) {
    merchantStore
      .getMerchantList(page, {
        keyword: searchKey.value.keyword,
        keycode: searchKey.value.keycode
      })
      .then()
      .catch()
  } else {
    merchantStore
      .getMerchantList(page)
      .then((res) => {})
      .catch((e) => {})
  }
}

function handleSearch(keyword) {
  searchKey.value.keyword = keyword
  merchantStore
    .getMerchantList(1, {
      keyword: searchKey.value.keyword,
      keycode: searchKey.value.keycode
    })
    .then()
    .catch()
}

function handleSelect(lst) {
  searchKey.value.keyword = lst[0]
  searchKey.value.keycode = lst[0][2]
  merchantStore
    .getMerchantList(1, {
      keyword: searchKey.value.keyword,
      keycode: searchKey.value.keycode
    })
    .then()
    .catch()
}

const clearCode = lockFunction(1000)(() => {
  codeList.value = ['00', '0000', '000000']
  searchKey.value.keycode = ''
  merchantStore
    .getMerchantList(1, {
      keyword: searchKey.value.keyword,
      keycode: searchKey.value.keycode
    })
    .then()
    .catch()
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

.search-merchant {
  display: flex;
}

.search-btn {
  margin-right: 10px;
}

.merchant-list {
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
