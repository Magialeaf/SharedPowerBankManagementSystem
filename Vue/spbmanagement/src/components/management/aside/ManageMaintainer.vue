<template>
  <ManagePerson :identityCode="identityStore.Maintainer" />
</template>

<script setup>
import { useIdentityStore } from '@/stores/authenticationStore'
import ManagePerson from '@/components/management/user/ManagePerson.vue'

const identityStore = useIdentityStore()
</script>
