<template>
  <div class="search-box">
    <div class="search-merchant">
      <SelectArea tip="搜索" :codeList="codeList" @areaSelected="handleSelect" />
      <el-select
        v-model="selectArea"
        placeholder="具体区域"
        style="width: 218px; margin-left: 42px"
      >
        <el-option v-for="item in areaOptions" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
      <el-button class="search-btn" type="primary" @click="clearCode()" style="margin-right: 10px"
        >清空</el-button
      >
      <Search @search="handleSearch" searchTip="搜素名称、地址、联系人" />
    </div>
  </div>
  <div class="content-box">
    <PartnerCards :data="merchantList" />
  </div>
  <div class="footer-box">
    <div class="pagination">
      <Pagination
        :pageInfo="merchantStore.getPageInfo()"
        @page-change="handlePageChange"
        :ifGoTop="false"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, computed, watch, nextTick } from 'vue'
import { useMerchantStore } from '@/stores/merchantStore.js'
import { lockFunction } from '@/utils/myLock'
import { useAreaStore } from '@/stores/areaStore'
import Search from '@/components/management/utils/Search.vue'
import SelectArea from '@/components/management/utils/SelectArea.vue'
import PartnerCards from '@/components/home/partner/PartnerCards.vue'

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
      // console.log(res)
    })
    .catch((e) => {})
})
function initList() {
  merchantStore
    .initMerchantList()
    .then((res) => {})
    .catch((e) => {})
}

function handlePageChange(page) {
  if (searchKey.value) {
    merchantStore
      .getMerchantList(page, {
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
    merchantStore
      .getMerchantList(page)
      .then((res) => {
        nextTick(() => {
          window.scrollTo({ top: 300, behavior: 'smooth' }) // 执行平滑滚动
        })
      })
      .catch((e) => {})
  }
}

function handleSearch(keyword = searchKey.value.keyword) {
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
.search-box {
  width: 100%;
  height: 30px;
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.search-merchant {
  display: flex;
}

.footer-box {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 10px;
}
</style>
