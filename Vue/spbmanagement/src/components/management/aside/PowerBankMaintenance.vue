<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewSPB">{{
        ifAddNewSPB ? '充电宝维护列表' : '新增充电宝维护记录'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewSPB" class="right-operation">
      <div class="search-SPB">
        <el-select v-model="searchKey.power_bank" @change="handleSearch" placeholder="搜索充电宝">
          <el-option
            v-for="item in powerBankList"
            :key="item.id"
            :label="item.id + '.' + item.name"
            :value="item.id"
          ></el-option>
        </el-select>
        <el-select
          v-model="searchKey.maintainer_account"
          @change="handleSearch"
          placeholder="搜索维护人员"
        >
          <el-option
            v-for="item in maintainerList"
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
    <SPBList :powerBankData="powerBankMaintenanceList" />
    <div class="pagination">
      <Pagination
        :pageInfo="powerBankMaintenanceStore.getPageInfo()"
        @page-change="handlePageChange"
      />
    </div>
  </div>
  <SPBOperation :ifNew="true" v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed, watch } from 'vue'
import { useSPBMaintenanceStore } from '@/stores/SPBStore.js'
import { useMaintainNameStore, usePowerBankNameStore } from '@/stores/nameList.js'
import { lockFunction } from '@/utils/myLock'
import Pagination from '@/components/management/utils/Pagination.vue'
import SPBList from '@/components/management/spbMaintenance/SPBMaintenanceList.vue'
import SPBOperation from '@/components/management/spbMaintenance/SPBMaintenanceOperation.vue'

const ifAddNewSPB = ref(false)

const searchKey = ref({
  power_bank: '',
  maintainer_account: ''
})

const powerBankMaintenanceStore = useSPBMaintenanceStore()
const powerBankMaintenanceList = computed(() => powerBankMaintenanceStore.showList())

const maintainNameStore = useMaintainNameStore()
const powerBankNameStore = usePowerBankNameStore()

onBeforeMount(() => initList())

const powerBankList = computed(() => powerBankNameStore.showList())
const maintainerList = computed(() => maintainNameStore.showList())

function initList() {
  powerBankMaintenanceStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
  powerBankNameStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
  maintainNameStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
}

function switchAddNewSPB() {
  ifAddNewSPB.value = !ifAddNewSPB.value
  if (!ifAddNewSPB.value) {
    powerBankMaintenanceStore.initList()
  }
}

function handlePageChange(page) {
  if (searchKey.value) {
    powerBankMaintenanceStore
      .getList(page, searchKey.value)
      .then((res) => {})
      .catch((e) => {})
  } else {
    powerBankMaintenanceStore
      .getList(page)
      .then((res) => {})
      .catch((e) => {})
  }
}

function clearSearch() {
  searchKey.value.power_bank = ''
  searchKey.value.maintainer_account = ''
  handleSearch()
}

function handleSearch() {
  powerBankMaintenanceStore
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
