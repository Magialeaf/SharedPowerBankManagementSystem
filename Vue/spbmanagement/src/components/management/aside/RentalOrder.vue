<template>
  <div class="operation">
    <div class="left-operation">
      <el-button v-if="ifUpIdentity" type="primary" @click="switchAddNewSPB">{{
        ifAddNewSPB ? '租赁列表' : '新增租赁记录'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewSPB && ifUpIdentity" class="right-operation">
      <div class="search-SPB">
        <el-select v-model="searchKey.power_bank" @change="handleSearch" placeholder="搜索充电宝">
          <el-option
            v-for="item in powerBankList"
            :key="item.id"
            :label="item.id + '.' + item.name"
            :value="item.id"
          ></el-option>
        </el-select>
        <el-select v-model="searchKey.user" @change="handleSearch" placeholder="搜索用户">
          <el-option
            v-for="item in userList"
            :key="item.id"
            :label="item.id + '.' + item.name"
            :value="item.id"
          ></el-option>
        </el-select>
        <el-button type="warning" @click="clearSearch">清空</el-button>
      </div>
    </div>
  </div>
  <div v-if="!ifAddNewSPB" class="SPB-list">
    <OrderList
      :orderRentalData="orderRentalList"
      :ifUpIdentity="ifUpIdentity"
      @filter-returned="handleFilterReturned"
      @sort-by="handleSortBy"
    />
    <div class="pagination">
      <Pagination :pageInfo="orderRentalStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <OrderOperation :ifNew="true" v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import { useOrderRentalStore } from '@/stores/orderStore.js'
import { useUserNameStore, usePowerBankNameStore } from '@/stores/nameList.js'
import { useJwtTokenStore, useIdentityStore } from '@/stores/authenticationStore'
import { lockFunction } from '@/utils/myLock'
import Pagination from '@/components/management/utils/Pagination.vue'
import OrderList from '@/components/management/orderRental/OrderRentalList.vue'
import OrderOperation from '@/components/management/orderRental/OrderRentalOperation.vue'

const ifAddNewSPB = ref(false)
const ifUpIdentity = ref(false)

const searchKey = ref({
  power_bank: null,
  user: null,
  returned: null,
  order_by: null
})

const orderRentalStore = useOrderRentalStore()
const orderRentalList = computed(() => orderRentalStore.showList())

const userNameStore = useUserNameStore()
const powerBankNameStore = usePowerBankNameStore()
const jwtTokenStore = useJwtTokenStore()
const identityStore = useIdentityStore()

onBeforeMount(() => initList())

const powerBankList = computed(() => powerBankNameStore.showList())
const userList = computed(() => userNameStore.showList())

function initList() {
  const identityCode = jwtTokenStore.getIdentityCode()
  if (identityCode === identityStore.Admin || identityCode === identityStore.SuperAdmin) {
    ifUpIdentity.value = true
  }

  orderRentalStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
  if (ifUpIdentity.value) {
    powerBankNameStore
      .initList()
      .then((res) => {})
      .catch((e) => {})
    userNameStore
      .initList()
      .then((res) => {})
      .catch((e) => {})
  }
}

function switchAddNewSPB() {
  ifAddNewSPB.value = !ifAddNewSPB.value
  if (!ifAddNewSPB.value) {
    orderRentalStore.initList()
  }
}

function handlePageChange(page) {
  if (searchKey.value) {
    orderRentalStore
      .getList(page, searchKey.value)
      .then((res) => {})
      .catch((e) => {})
  } else {
    orderRentalStore
      .getList(page)
      .then((res) => {})
      .catch((e) => {})
  }
}

function clearSearch() {
  Object.keys(searchKey.value).forEach((key) => {
    searchKey.value[key] = ''
  })
  handleSearch(1)
}

function handleSearch(page = orderRentalStore.getPageInfo().currentPage) {
  orderRentalStore
    .getList(page, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}

function handleFilterReturned(returned) {
  searchKey.value.returned = returned
  handleSearch()
}

function handleSortBy(order_by) {
  searchKey.value.order_by = [order_by]
  handleSearch()
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

.search-SPB {
  width: 60%;
  display: flex;
}

.search-btn {
  margin-right: 10px;
}

.SPB-list {
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
