<template>
  <div class="carousel-container">
    <el-carousel v-if="imgList" :interval="4000" type="card" height="220px">
      <el-carousel-item v-for="item in imgList" :key="item.id">
        <img class="carousel-img" :src="item.img" />
      </el-carousel-item>
    </el-carousel>
    <el-carousel v-else :interval="4000" type="card" height="220px">
      <el-carousel-item v-for="item in 3" :key="item">
        <h3 text="2xl" justify="center">暂无图片</h3>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

const imgList = computed(() => props.imgList)

const props = defineProps({
  imgList: Array
})
</script>

<style scoped>
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
