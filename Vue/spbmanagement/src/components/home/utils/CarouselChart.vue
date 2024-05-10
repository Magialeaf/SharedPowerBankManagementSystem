<template>
  <div class="carousel-container">
    <el-carousel
      v-if="imgList"
      direction="vertical"
      trigger="click"
      :interval="4000"
      height="300px"
    >
      <el-carousel-item v-for="item in imgList" :key="item.id">
        <img class="carousel-img" :src="item.img" />
      </el-carousel-item>
    </el-carousel>
    <el-carousel v-else :interval="4000" trigger="click" direction="vertical" height="300px">
      <el-carousel-item v-for="item in 3" :key="item">
        <h3 text="2xl" justify="center">暂无图片</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup>
import { useCarouselChartStore } from '@/stores/carouselChartStore'
import { ref, onBeforeMount } from 'vue'

const carouselChart = useCarouselChartStore()

const imgList = ref()

onBeforeMount(() => {
  carouselChart
    .showCarouselChart()
    .then((res) => {
      if (res.data.length > 0) imgList.value = res.data
    })
    .catch((e) => {})
})
</script>

<style scoped>
.carousel-container {
  margin-bottom: -40px;
}

.carousel-img {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  transition: all 0.5s;
  transform: scale(1.1);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
