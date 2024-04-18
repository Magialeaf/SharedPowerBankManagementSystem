<template>
  <Search />
  <UserList :userData="userList" />
</template>

<script setup>
import { onBeforeMount, ref, computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useIdentityStore } from '@/stores/authenticationStore.js'
import Search from '@/components/management/utils/Search.vue'
import UserList from '@/components/management/user/UserList.vue'

const userStore = useUserStore()
const identityStore = useIdentityStore()

const page = ref(1)
const userList = computed(() => userStore.getList())

onBeforeMount(() => initList())

function initList() {
  userStore
    .initUserList(identityStore.Maintainer)
    .then((res) => {})
    .catch((e) => {})
}
</script>

<style scoped></style>
