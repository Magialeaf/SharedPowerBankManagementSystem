<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="chartInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="chartInfo.id" label="标题" :max-length="20">
      <el-input v-model="chartInfo.title" />
    </el-form-item>
    <el-form-item v-if="chartInfo.id" label="轮播图">
      <UploadImg
        :imgUrl="chartInfo.img"
        :ifUpload="ifUploadValue"
        :uploadFunc="carouselChartStore.uploadImg"
        @updateIfUpload="updateIfUpload"
        @updateImgUrl="updateImgUrl"
        @uploadSuccess="afterUploadImgSuccess"
      />
    </el-form-item>
    <el-form-item v-if="chartInfo.id" label="状态">
      <el-select v-model="chartInfo.active" placeholder="请选择状态">
        <el-option label="启用" :value="1"></el-option>
        <el-option label="禁用" :value="0"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item v-if="chartInfo.id" label="创建时间">
      <el-input v-model="chartInfo.create_time" disabled></el-input>
    </el-form-item>
    <el-form-item v-if="chartInfo.id" label="更新时间">
      <el-input v-model="chartInfo.update_time" disabled></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="success" @click="onSubmit">更新轮播图</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref } from 'vue'
import { useCarouselChartStore } from '@/stores/carouselChartStore'
import UploadImg from '@/components/management/utils/UploadImg.vue'
import { lockFunction } from '@/utils/myLock'

const carouselChartStore = useCarouselChartStore()
const ifUploadValue = ref(false)

const chartInfo = ref({})

const props = defineProps({
  id: {
    type: Number,
    default: -1
  }
})

function updateIfUpload(value) {
  ifUploadValue.value = value
}

function updateImgUrl(value) {
  chartInfo.value.img = value
}

const onSubmit = lockFunction()(() => {
  ifUploadValue.value = true
})

function afterUploadImgSuccess(value) {
  const uploadValue = { ...chartInfo.value }
  uploadValue.img = value.data.img
  carouselChartStore
    .updateCarouselChart(props.id, uploadValue)
    .then((res) => {
      chartInfo.value = res.data
      chartInfo.value.id = -1
    })
    .catch((e) => {})
}

onBeforeMount(() => {
  carouselChartStore
    .getCarouselChart(props.id)
    .then((res) => {
      console.log(res.data)
      chartInfo.value = res.data
    })
    .catch((e) => {})
})
</script>
