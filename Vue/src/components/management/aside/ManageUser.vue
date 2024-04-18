<template>
  <Search />
  <UserList :userData="userList" />
</template>

<script setup>
import Search from '@/components/management/utils/Search.vue'
import UserList from '@/components/management/user/UserList.vue'
import { computed, onBeforeMount, ref } from 'vue'
import { useIdentityStore } from '@/stores/authenticationStore.js'
import { useUserStore } from '@/stores/userStore'

const userStore = useUserStore()
const identityStore = useIdentityStore()

const page = ref(1)
const userList = computed(() => userStore.getList())

onBeforeMount(() => initList())

function initList() {
  userStore
    .initUserList(identityStore.User)
    .then((res) => {})
    .catch((e) => {})
}
</script>

<style scoped></style>
