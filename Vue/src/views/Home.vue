<template>
  <div class="container">
    <div class="top">
      <header class="header-box">
        <HomeHeader />
      </header>
      <div class="content-box">
        <HomeMain />
      </div>
    </div>
    <div class="bottom">
      <footer class="footer-box">
        <HomeFooter />
      </footer>
    </div>
  </div>
</template>

<script setup>
import HomeHeader from '@/components/home/index/HomeHeader.vue'
import HomeMain from '@/components/home/index/HomeMain.vue'
import HomeFooter from '@/components/home/index/HomeFooter.vue'
</script>

<style scoped>
.header-box {
  position: fixed;
  top: 0px;
  left: -2px;
  width: 100%;
  height: 100px;
  z-index: 100;
}

.content-box {
  position: relative;
  width: 100%;
  margin-top: 100px;
}

.container {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
