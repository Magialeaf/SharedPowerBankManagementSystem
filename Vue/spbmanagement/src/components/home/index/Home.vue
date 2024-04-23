<template>
  <CarouselChart :imgList="imgList" />
</template>

<script setup>
import CarouselChart from '@/components/home/utils/CarouselChart.vue'
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

<style scoped></style>
