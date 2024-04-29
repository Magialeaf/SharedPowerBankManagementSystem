<template>
  <div class="operation">
    <div class="left-operation">
      <el-button type="primary" @click="switchAddNew">{{
        ifAddNew ? tip.listTip : tip.addTip
      }}</el-button>
    </div>
    <div v-if="!ifAddNew" class="right-operation">
      <div class="search-area">
        <SelectAddress
          v-if="props.identityCode === identityStore.Maintainer"
          :codeList="codeList"
          :areaOption="null"
          @select-area="handleSelectArea"
          @clear-code-list="handleClearCodeList"
        />
        <Search @search="handleSearch" searchTip="搜索用户名、简介" />
      </div>
    </div>
  </div>
  <div v-if="!ifAddNew" class="user-list">
    <UserList :userData="userList" :identityCode="props.identityCode" />
    <div class="pagination">
      <Pagination :pageInfo="userStore.getPageInfo()" @page-change="handlePageChange" />
    </div>
  </div>
  <AddNewUser :identityCode="props.identityCode" v-else />
</template>

<script setup>
import Search from '@/components/management/utils/Search.vue'
import UserList from '@/components/management/user/UserList.vue'
import AddNewUser from '@/components/management/user/AddNewUser.vue'
import { computed, onBeforeMount, ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useIdentityStore } from '@/stores/authenticationStore'
import SelectAddress from '@/components/management/utils/SelectAddress.vue'

const userStore = useUserStore()
const identityStore = useIdentityStore()

const props = defineProps({
  identityCode: {
    type: Number
  }
})

const currentPage = ref(1)

const ifAddNew = ref(false)
const searchKey = ref({
  keyword: '',
  areaId: null
})
const tip = ref({
  listTip: '',
  addTip: ''
})

const codeList = ref(['00', '0000', '000000'])

const userList = computed(() => userStore.getList())

onBeforeMount(() => initList())

function initList() {
  userStore
    .initUserList(props.identityCode)
    .then((res) => {})
    .catch((e) => {})
  if (props.identityCode == identityStore.User) {
    tip.value.listTip = '用户列表'
    tip.value.addTip = '添加用户'
  } else if (props.identityCode == identityStore.Maintainer) {
    tip.value.listTip = '维护人员列表'
    tip.value.addTip = '添加维护人员'
  } else {
    tip.value.listTip = '未知列表'
    tip.value.addTip = '添加未知用户'
  }
}

function handleSearch(keyword) {
  searchKey.value.keyword = keyword
  userStore
    .getUserList(1, {
      keyword: searchKey.value.keyword
    })
    .then()
    .catch()
}

function handlePageChange(page) {
  currentPage.value = page
  if (searchKey.value) {
    userStore
      .getUserList(page, {
        keyword: searchKey.value.keyword,
        areaId: searchKey.value.areaId
      })
      .then()
      .catch()
  } else {
    userStore
      .getUserList(page)
      .then((res) => {})
      .catch((e) => {})
  }
}

function handleSelectArea(id) {
  searchKey.value.areaId = id
  handlePageChange(1)
}

function handleClearCodeList() {
  codeList.value = ['00', '0000', '000000']
  handleSelectArea()
}

function switchAddNew() {
  ifAddNew.value = !ifAddNew.value
  if (!ifAddNew.value) {
    userStore.initUserList(props.identityCode)
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

.user-list {
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

.search-area {
  display: flex;
  justify-content: flex-end;
}
</style>
