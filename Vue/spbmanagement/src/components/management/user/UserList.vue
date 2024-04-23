<template>
  <el-table :data="userList" stripe border>
    <el-table-column class="table-column" min-width="5%" prop="id" label="uid" />
    <el-table-column class="table-column" min-width="15%" prop="username" label="用户名" />
    <el-table-column class="table-column" min-width="5%" prop="sex" label="性别" />
    <el-table-column class="table-column" min-width="10%" label="头像">
      <template #default="{ row }">
        <img :src="row.avatar" alt="用户头像" style="max-width: 48px; max-height: 48px" />
      </template>
    </el-table-column>
    <el-table-column class="table-column" min-width="15%" prop="profile" label="简介" />
    <el-table-column class="table-column" min-width="10%" prop="birthday" label="生日" />
    <template v-if="props.identityCode == identityStore.Maintainer">
      <el-table-column
        class="table-column"
        min-width="20%"
        prop="maintain_areas"
        label="维护区域"
      />
    </template>
    <el-table-column min-width="30%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <OneUserInfo v-if="drawer" :uid="selectedUid" :identityCode="props.identityCode"
  /></el-drawer>
</template>

<script setup>
import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
import { useIdentityStore } from '@/stores/authenticationStore'
import { useUserStore } from '@/stores/userStore'
import { ref, computed } from 'vue'
import OneUserInfo from '@/components/management/user/OneUserInfo.vue'

const userList = computed(() => props.userData)

const drawer = ref(false)
const selectedUid = ref(undefined)
const userStore = useUserStore()
const identityStore = useIdentityStore()

const props = defineProps({
  userData: {
    type: Array
  },
  identityCode: {
    type: Number
  }
})

function showDetails(row) {
  selectedUid.value = row.id // 获取当前点击行的 uid
  drawer.value = true // 打开抽屉
}

function deleteRow(row) {
  $confirmDeleteMsg('确定删除用户吗?')
    .then(() => {
      userStore.deleteOneInfo(row.id)
    })
    .catch((e) => {
      $errorMsg('取消删除')
    })
}
</script>

<style scoped>
.operation {
  margin-bottom: 20px;
}
</style>
