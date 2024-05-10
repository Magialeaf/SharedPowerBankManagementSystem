<template>
  <div class="operation">
    <div class="left-operation">
      <!-- <el-button type="primary" @click="switchAddNewSPB">{{
          ifAddNewSPB ? '归还列表' : '新增归还记录'
        }}</el-button> -->
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
      :orderFeeData="orderFeeList"
      :ifUpIdentity="ifUpIdentity"
      @filter-paid="handleFilterPaid"
      @sort-by="handleSortBy"
    />
    <div class="pagination">
      <Pagination :pageInfo="orderFeeStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <!--<OrderOperation :ifNew="true" v-else />-->
</template>

<script setup>
import { ref, onBeforeMount, computed } from 'vue'
import { useOrderFeeStore } from '@/stores/orderStore.js'
import { useUserNameStore, usePowerBankNameStore } from '@/stores/nameList.js'
import { useJwtTokenStore, useIdentityStore } from '@/stores/authenticationStore'
import { lockFunction } from '@/utils/myLock'
import Pagination from '@/components/management/utils/Pagination.vue'
import OrderList from '@/components/management/orderFee/OrderFeeList.vue'
import OrderOperation from '@/components/management/orderFee/OrderFeeOperation.vue'

const ifAddNewSPB = ref(false)
const ifUpIdentity = ref(false)

const searchKey = ref({
  power_bank: '',
  user: '',
  paid: null,
  order_by: []
})

const orderFeeStore = useOrderFeeStore()
const orderFeeList = computed(() => orderFeeStore.showList())

const userNameStore = useUserNameStore()
const powerBankNameStore = usePowerBankNameStore()

onBeforeMount(() => initList())

const powerBankList = computed(() => powerBankNameStore.showList())
const userList = computed(() => userNameStore.showList())

const jwtTokenStore = useJwtTokenStore()
const identityStore = useIdentityStore()

function initList() {
  const identityCode = jwtTokenStore.getIdentityCode()
  if (identityCode === identityStore.Admin || identityCode === identityStore.SuperAdmin) {
    ifUpIdentity.value = true
  }

  orderFeeStore
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
    orderFeeStore.initList()
  }
}

function handlePageChange(page) {
  if (searchKey.value) {
    orderFeeStore
      .getList(page, searchKey.value)
      .then((res) => {})
      .catch((e) => {})
  } else {
    orderFeeStore
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

function handleSearch(page = orderFeeStore.getPageInfo().currentPage) {
  orderFeeStore
    .getList(page, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}

function handleFilterPaid(value) {
  searchKey.value.paid = value
  handleSearch()
}

function handleSortBy(value) {
  searchKey.value.order_by = [value]
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
