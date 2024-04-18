<template>
  <div class="operation">
    <el-button type="info">新增</el-button>
    <el-button type="info">删除</el-button>
  </div>
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
    <template v-if="haveMaintainArea">
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
        <el-button type="warning">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <OneUserInfo v-if="drawer" :uid="selectedUid"
  /></el-drawer>
</template>

<script setup>
import OneUserInfo from '@/components/management/user/OneUserInfo.vue'
import { ref, computed } from 'vue'

const haveMaintainArea = ref(false)

const userList = ref(
  computed(() => {
    identify()
    return prop.userData
  })
)

function identify() {
  for (let i = 0; i < prop.userData?.length; i++) {
    if (prop.userData[i].maintain_areas) {
      haveMaintainArea.value = true
      break
    }
  }
}

const drawer = ref(false)
const selectedUid = ref(undefined)

const prop = defineProps({
  userData: {
    type: Array
  }
})

function showDetails(row) {
  selectedUid.value = row.id // 获取当前点击行的 uid
  drawer.value = true // 打开抽屉
}
</script>

<style scoped>
.operation {
  margin-bottom: 20px;
}
</style>
