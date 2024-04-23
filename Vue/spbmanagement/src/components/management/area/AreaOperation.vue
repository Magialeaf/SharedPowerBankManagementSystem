<template>
  <el-form label-position="left" label-width="20%" :model="areaInfo" style="max-width: 600px">
    <el-form-item v-if="areaInfo.id" label="id">
      <el-input v-model="areaInfo.id" disabled />
    </el-form-item>
    <el-form-item v-if="areaInfo.id" label="区域">
      <SelectArea :codeList="codeList" @areaSelected="areaSelected" />
    </el-form-item>
    <el-form-item v-if="areaInfo.id" label="区域名字">
      <el-input v-model="areaInfo.name" :maxlength="areaLen" />
    </el-form-item>
    <el-form-item v-if="areaInfo.id" label="描述">
      <el-input
        type="textarea"
        :rows="4"
        resize="none"
        v-model="areaInfo.description"
        :maxlength="areaDescLen"
      />
    </el-form-item>
    <el-form-item v-if="areaInfo.id" label="经度">
      <el-input v-model="areaInfo.longitude" @blur="updateView()" />
    </el-form-item>
    <el-form-item v-if="areaInfo.id" label="纬度">
      <el-input v-model="areaInfo.latitude" @blur="updateView()" />
    </el-form-item>
    <el-form-item v-if="areaInfo.id">
      <el-button type="success" @click="updateAreaInfo()">保存更改</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { areaLen, areaDescLen, validate_longitude, validate_latitude } from '@/utils/validateArea'
import { $errorMsg } from '@/utils/msg'
import { useAddressStore } from '@/stores/areaStore'
import { useAreaStore } from '@/stores/areaStore'
import { lockFunction } from '@/utils/myLock'

const areaStore = useAreaStore()
const addressStore = useAddressStore()
const len = ref(areaStore.getLatAndLonLen())

const codeList = ref(['00', '0000', '000000'])

const areaInfo = ref({
  id: 0,
  code: '000000',
  name: '',
  description: '',
  longitude: 0,
  latitude: 0
})

const prop = defineProps({
  id: { type: Number, required: true }
})

const updateAreaInfo = lockFunction()(() => {
  areaStore
    .updateArea(areaInfo.value.id, areaInfo.value)
    .then(() => {})
    .catch(() => {})
})

onBeforeMount(() => {
  areaStore.getArea(prop.id).then((res) => {
    areaInfo.value = res.data
    codeList.value = [
      areaInfo.value.code.slice(0, 2),
      areaInfo.value.code.slice(0, 4),
      areaInfo.value.code.slice(0, 6)
    ]
  })
})

function getAreaFromAPI() {
  areaStore
    .getAreaByLatAndLon(areaInfo.value.latitude, areaInfo.value.longitude)
    .then((res) => {
      const id = res.data.id
      if (id !== areaInfo.value.id) $errorMsg('区域已存在')

      return true
    })
    .catch(() => {
      return false
    })
}

const updateView = lockFunction(500)((
  lat = areaInfo.value.latitude || 0,
  lng = areaInfo.value.longitude || 0
) => {
  areaInfo.value.latitude = validate_latitude(lat, len.value)
  areaInfo.value.longitude = validate_longitude(lng, len.value)
  if (!getAreaFromAPI()) {
    addressStore.reverseGeocode(areaInfo.value.latitude, areaInfo.value.longitude).then((res) => {
      if (res.result.ad_info.adcode) {
        areaInfo.value.code = res.result.ad_info.adcode
        areaInfo.value.name = res.result.address_component.street_number
          ? res.result.address_component.street_number
          : res.result.address_component.street
      } else {
        areaInfo.value.code = '000000'
        areaInfo.value.name = ''
      }
      codeList.value = [
        areaInfo.value.code.slice(0, 2),
        areaInfo.value.code.slice(0, 4),
        areaInfo.value.code
      ]
    })
  }
})

function areaSelected(lst) {
  codeList.value = lst[0]
  areaInfo.value.code = lst[0][2]
  const address = lst[1].reduce((pre, cur) => pre + cur)
  addressStore
    .geocode(address)
    .then((res) => {
      const lngLat = res.result.location
      areaInfo.value.latitude = validate_latitude(lngLat.lat, len.value)
      areaInfo.value.longitude = validate_longitude(lngLat.lng, len.value)
    })
    .catch((e) => {
      $errorMsg(e.message)
    })
}
</script>

<style scoped></style>
