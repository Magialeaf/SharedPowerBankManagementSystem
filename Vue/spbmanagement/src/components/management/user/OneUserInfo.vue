<template>
  <div class="switch">
    <el-button type="primary" @click="switchValue = !switchValue">{{
      switchValue ? '切换至账户信息' : '切换至用户信息'
    }}</el-button>
  </div>
  <div class="info">
    <UserOperation
      v-if="switchValue"
      :userData="userInfo"
      :ifMyself="ifMyself"
      @updateUserInfo="updateUserInfo"
    />
    <AccountOperation v-else :accountData="accountInfo" :ifMyself="ifMyself" />
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { convertBackendTimestampToLocalTime } from '@/utils/convert.js'
import { useUserStore } from '@/stores/userStore'
import AccountOperation from '@/components/management/user/AccountOperation.vue'
import UserOperation from '@/components/management/user/UserOperation.vue'

const switchValue = ref(true)
const userStore = useUserStore()

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
  birthday: '',
  phone: ''
})

const prop = defineProps({
  uid: { type: Number, required: false }
})

onBeforeMount(() => {
  if (prop.uid === undefined) {
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
      .getOneInfo(prop.uid)
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
</script>

<style scoped>
.switch {
  margin-bottom: 20px;
}
</style>
