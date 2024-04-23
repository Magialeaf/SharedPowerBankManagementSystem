<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewMerchant">{{
        ifAddNewMerchant ? '商户列表' : '新增商户'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewMerchant" class="right-operation">
      <div class="search-merchant">
        <SelectArea tip="搜索" :codeList="codeList" @areaSelected="handleSelect" />
        <el-select
          v-model="selectArea"
          placeholder="具体区域"
          style="width: 218px; margin-left: 42px"
        >
          <el-option
            v-for="item in areaOptions"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
        <el-button class="search-btn" type="primary" @click="clearCode()">清空</el-button>
        <Search @search="handleSearch" searchTip="搜素名称、地址、联系人" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNewMerchant" class="merchant-list">
    <MerchantList :merchantData="merchantList" />
    <div class="pagination">
      <Pagination :pageInfo="merchantStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <MerchantOperation :ifNew="true" v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed, watch } from 'vue'
import { useMerchantStore } from '@/stores/merchantStore.js'
import { lockFunction } from '@/utils/myLock'
import { useAreaStore } from '@/stores/areaStore'
import Search from '@/components/management/utils/Search.vue'
import SelectArea from '@/components/management/utils/SelectArea.vue'
import MerchantList from '@/components/management/merchant/MerchantList.vue'
import MerchantOperation from '@/components/management/merchant/MerchantOperation.vue'
import Pagination from '@/components/management/utils/Pagination.vue'

const ifAddNewMerchant = ref(false)
const codeList = ref(['00', '0000', '000000'])
const searchKey = ref({
  keyword: '',
  keyAreaId: ''
})
const selectArea = ref('')

const areaStore = useAreaStore()
const merchantStore = useMerchantStore()

const areaOptions = ref([])
const merchantList = computed(() => merchantStore.getList())

onBeforeMount(() => initList())

watch(selectArea, () => {
  searchKey.value.keyAreaId = selectArea.value
  merchantStore
    .getMerchantList(1, {
      keyword: searchKey.value.keyword,
      keyAreaId: searchKey.value.keyAreaId
    })
    .then((res) => {
      console.log(res)
    })
    .catch((e) => {})
})
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
  if (searchKey.value) {
    merchantStore
      .getMerchantList(page, {
        keyword: searchKey.value.keyword,
        keyAreaId: searchKey.value.keyAreaId
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
      keyAreaId: searchKey.value.keyAreaId
    })
    .then()
    .catch()
}

function handleSelect(lst) {
  areaStore
    .getAreaNameList(lst[0][2])
    .then((res) => {
      areaOptions.value = res.data
    })
    .catch((e) => {})
  codeList.value = lst[0]
}

const clearCode = lockFunction(1000)(() => {
  codeList.value = ['00', '0000', '000000']
  searchKey.value.keyAreaId = ''
  selectArea.value = ''
  areaOptions.value = []
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
