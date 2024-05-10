<template>
  <div class="container">
    <div class="top">
      <header class="header-box">
        <HomeHeader />
      </header>
      <div v-if="ifSubPage" class="content-box">
        <CarouselChart />
      </div>
      <div class="main-box">
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
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import HomeHeader from '@/components/home/index/HomeHeader.vue'
import HomeMain from '@/components/home/index/HomeMain.vue'
import HomeFooter from '@/components/home/index/HomeFooter.vue'
import CarouselChart from '@/components/home/utils/CarouselChart.vue'

const ifSubPage = ref(true)
const route = useRoute()

watch(
  () => route.path,
  (newPath) => {
    const pathArray = newPath.split('/')
    if (pathArray.length > 2) {
      ifSubPage.value = false
    } else if (pathArray[1] === 'user') {
      ifSubPage.value = false
    } else {
      ifSubPage.value = true
    }
  },
  { immediate: true }
)
</script>

<style scoped>
.header-box {
  position: fixed;
  top: 0px;
  left: -2px;
  width: 100%;
  height: 60px;
  z-index: 100;
}

.content-box {
  position: relative;
  width: 100%;
  margin-top: 60px;
}

.main-box {
  margin-left: 10%;
  width: 80%;
}

.container {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
</style>
