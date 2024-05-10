<template>
  <UserHome :data="data" />
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { useUserStore } from '@/stores/userStore'
import UserHome from '@/components/home/user/UserHome.vue'

const userStore = useUserStore()

onBeforeMount(() => initData())

const data = ref()

function initData() {
  userStore
    .getMyInfo()
    .then((res) => {
      let accountInfo = res.data[0]
      let userInfo = res.data[1]

      const aid = accountInfo.id
      delete accountInfo.id // 删除旧的 'id' 属性
      accountInfo.aid = aid // 添加新的 'aid' 属性

      const uid = userInfo.id
      delete userInfo.id
      userInfo.uid = uid

      delete userInfo.aid_id

      data.value = {
        ...accountInfo,
        ...userInfo
      }
    })
    .catch((e) => {})
}
</script>

<style scoped></style>
