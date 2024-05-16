<template>
  <div class="switch">
    <el-button type="primary" @click="switchView">{{
      switchValue ? '切换至账户信息' : '切换至用户信息'
    }}</el-button>
    <el-button
      v-if="
        accountInfo.identity == identityStore.Maintainer &&
        (jwtTokenStore.getIdentityCode() === identityStore.SuperAdmin ||
          jwtTokenStore.getIdentityCode() === identityStore.Admin)
      "
      type="primary"
      @click="maintenanceValue = true"
      >{{ '切换至区域管理' }}</el-button
    >
  </div>
  <div class="info">
    <UserOperation
      v-if="switchValue && !maintenanceValue"
      :userData="userInfo"
      :ifMyself="ifMyself"
      @updateUserInfo="updateUserInfo"
    />
    <AccountOperation
      v-else-if="!switchValue && !maintenanceValue"
      :accountData="accountInfo"
      :ifMyself="ifMyself"
    />
    <MaintenanceOperation v-else-if="maintenanceValue" :aid="accountInfo.id" />
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { convertBackendTimestampToLocalTime } from '@/utils/convert.js'
import { useUserStore } from '@/stores/userStore'
import { useJwtTokenStore, useIdentityStore } from '@/stores/authenticationStore'
import MaintenanceOperation from '@/components/management/user/MaintenanceOperation.vue'
import AccountOperation from '@/components/management/user/AccountOperation.vue'
import UserOperation from '@/components/management/user/UserOperation.vue'

const switchValue = ref(true)
const maintenanceValue = ref(false)

const userStore = useUserStore()
const identityStore = useIdentityStore()
const jwtTokenStore = useJwtTokenStore()

const ifMyself = ref(true)

const accountInfo = ref({
  id: '',
  account: '',
  email: '',
  identity: '',
  create_time: '',
  last_login_time: ''
})

const userInfo = ref({
  id: '',
  username: '',
  avatar: '',
  profile: '',
  birthday: ''
})

const props = defineProps({
  uid: { type: Number, required: false },
  identityCode: { type: Number, required: false }
})

onBeforeMount(() => {
  if (props.uid === undefined) {
    ifMyself.value = true
    userStore
      .getMyInfo()
      .then((res) => {
        accountInfo.value = res.data[0]
        userInfo.value = res.data[1]
        accountInfo.value['last_login_time'] = convertBackendTimestampToLocalTime(
          accountInfo.value['last_login_time']
        )
        accountInfo.value['create_time'] = convertBackendTimestampToLocalTime(
          accountInfo.value['create_time']
        )
      })
      .catch((e) => {})
  } else {
    ifMyself.value = false
    userStore
      .getOneInfo(props.uid)
      .then((res) => {
        accountInfo.value = res.data[0]
        userInfo.value = res.data[1]
        accountInfo.value['last_login_time'] = convertBackendTimestampToLocalTime(
          accountInfo.value['last_login_time']
        )
        accountInfo.value['create_time'] = convertBackendTimestampToLocalTime(
          accountInfo.value['create_time']
        )
      })
      .catch((e) => {})
  }
})

function updateUserInfo(value) {
  for (const key in value) {
    if (Object.prototype.hasOwnProperty.call(userInfo.value, key)) {
      userInfo.value[key] = value[key]
    }
  }
}

function switchView() {
  switchValue.value = !switchValue.value
  maintenanceValue.value = false
}
</script>

<style scoped>
.switch {
  margin-bottom: 20px;
}
</style>
