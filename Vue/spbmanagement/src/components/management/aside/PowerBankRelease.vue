<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNewSPB">{{
        ifAddNewSPB ? '充电宝投放列表' : '新增充电宝'
      }}</el-button>
    </div>
    <div v-if="!ifAddNewSPB" class="right-operation">
      <div class="search-SPB">
        <!--<SelectAddress />-->
        <Search @search="handleSearch" searchTip="搜素充电宝名称、商户名称" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNewSPB" class="SPB-list">
    <SPBList :SPBData="SPBList" />
    <div class="pagination">
      <Pagination :pageInfo="SPBStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <SPBOperation :ifNew="true" v-else />
</template>

<script setup>
import { ref, onBeforeMount, computed, watch } from 'vue'
import { useSPBStore } from '@/stores/SPBStore.js'
import { lockFunction } from '@/utils/myLock'
// import { useAreaStore } from '@/stores/areaStore'
import Search from '@/components/management/utils/Search.vue'
import SPBList from '@/components/management/spbRelease/SPBReleaseList.vue'
import SPBOperation from '@/components/management/spbRelease/SPBReleaseOperation.vue'
import Pagination from '@/components/management/utils/Pagination.vue'
import SelectAddress from '@/components/management/utils/SelectAddress.vue'

const ifAddNewSPB = ref(false)
// const codeList = ref(['00', '0000', '000000'])
// const searchKey = ref({
//   keyword: '',
//   keyAreaId: ''
// })
// const selectArea = ref('')

// const areaStore = useAreaStore()
const SPBStore = useSPBStore()

// const areaOptions = ref([])
// const SPBList = computed(() => SPBStore.getList())

// onBeforeMount(() => initList())

// watch(selectArea, () => {
//   searchKey.value.keyAreaId = selectArea.value
//   SPBStore.getSPBList(1, {
//     keyword: searchKey.value.keyword,
//     keyAreaId: searchKey.value.keyAreaId
//   })
//     .then((res) => {
//       console.log(res)
//     })
//     .catch((e) => {})
// })
// function initList() {
//   SPBStore.initSPBList()
//     .then((res) => {})
//     .catch((e) => {})
// }

function switchAddNewSPB() {
  ifAddNewSPB.value = !ifAddNewSPB.value
  //   if (ifAddNewSPB.value === false) {
  //     SPBStore.getSPBList(SPBStore.getPageInfo().currentPage)
  //       .then((res) => {})
  //       .catch((e) => {})
  //   }
}

// function handlePageChange(page) {
//   if (searchKey.value) {
//     SPBStore.getSPBList(page, {
//       keyword: searchKey.value.keyword,
//       keyAreaId: searchKey.value.keyAreaId
//     })
//       .then()
//       .catch()
//   } else {
//     SPBStore.getSPBList(page)
//       .then((res) => {})
//       .catch((e) => {})
//   }
// }

// function handleSearch(keyword) {
//   searchKey.value.keyword = keyword
//   SPBStore.getSPBList(1, {
//     keyword: searchKey.value.keyword,
//     keyAreaId: searchKey.value.keyAreaId
//   })
//     .then()
//     .catch()
// }

// function handleSelect(lst) {
//   areaStore
//     .getAreaNameList(lst[0][2])
//     .then((res) => {
//       areaOptions.value = res.data
//     })
//     .catch((e) => {})
//   codeList.value = lst[0]
// }

// const clearCode = lockFunction(1000)(() => {
//   codeList.value = ['00', '0000', '000000']
//   searchKey.value.keyAreaId = ''
//   selectArea.value = ''
//   areaOptions.value = []
// })
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
