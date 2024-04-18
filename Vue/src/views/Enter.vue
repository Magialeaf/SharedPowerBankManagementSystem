<template>
  <div class="enter-body">
    <div class="enter-container">
      <EnterPage />
    </div>
  </div>
</template>

<script setup>
import EnterPage from '@/components/enter/EnterPage.vue'
</script>

<style scoped>
.enter-body {
  background: linear-gradient(to right, rgb(247, 209, 215), rgb(191, 227, 241));
  height: 100vh;

  display: flex;
  justify-content: center;
  align-items: center;
}

.enter-container {
  height: 80%;
  width: 60%;

  margin-top: -10px;
}
</style>
