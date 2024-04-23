<template>
  <div class="map">
    <tmap-map
      mapKey="GT7BZ-PXOKN-ZUFFF-SYTJJ-EXVFQ-KZB2O"
      :events="events"
      :center="center"
      :zoom="zoom"
      :doubleClickZoom="doubleClickZoom"
      :control="control"
    >
      <div class="ctrl">
        <el-button @click.stop="zoom = 15">区域</el-button>
        <el-button @click.stop="zoom = 11">县级</el-button>
        <el-button @click.stop="zoom = 8">市级</el-button>
        <el-button @click.stop="zoom = 5">省级</el-button>
      </div>
    </tmap-map>
  </div>
  <el-form class="addArea" :model="areaInfo" :inline="true">
    <div class="up-and-down-box">
      <SelectArea tip="区域选择" :codeList="codeList" @areaSelected="areaSelected" />
      <el-form-item label="区域名称">
        <el-input
          v-model="areaInfo.name"
          :maxlength="areaLen"
          placeholder="请输入区域名称"
        ></el-input>
      </el-form-item>
    </div>
    <el-form-item label="简介">
      <el-input
        type="textarea"
        :maxlength="areaDescLen"
        :rows="4"
        resize="none"
        v-model="areaInfo.description"
        placeholder="简介"
      ></el-input>
    </el-form-item>
    <div class="up-and-down-box">
      <el-form-item label="经度">
        <el-input v-model="areaInfo.longitude" @blur="updateView()"></el-input>
      </el-form-item>
      <el-form-item label="纬度">
        <el-input v-model="areaInfo.latitude" @blur="updateView()"></el-input>
      </el-form-item>
    </div>
    <el-form-item>
      <el-button :type="ifHaveArea ? 'primary' : 'success'" @click="modifyArea()">{{
        ifHaveArea ? '更新' : '新增'
      }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref } from 'vue'
import { lockFunction } from '@/utils/myLock.js'
import { areaLen, areaDescLen, validate_longitude, validate_latitude } from '@/utils/validateArea'
import { useAreaStore, useAddressStore } from '@/stores/areaStore'
import SelectArea from '@/components/management/utils/SelectArea.vue'
import { $errorMsg } from '@/utils/msg'

const areaStore = useAreaStore()
const addressStore = useAddressStore()
const center = ref(areaStore.getCenter())
const len = ref(areaStore.getLatAndLonLen())
const ifHaveArea = ref(false)

const zoom = ref(15)
const doubleClickZoom = ref(false)

const control = {
  scale: {},
  zoom: {
    position: 'bottomRight'
  }
}

const codeList = ref(['00', '0000', '000000'])
const areaInfo = ref({
  id: -1,
  code: '000000',
  name: '',
  description: '',
  latitude: center.value.lat.toFixed(len.value),
  longitude: center.value.lng.toFixed(len.value)
})

const events = {
  dblclick: handleMapDoubleClick
}

function handleMapDoubleClick(e) {
  const { latLng } = e
  updateView(latLng.lat, latLng.lng)
}

const updateView = lockFunction(500)((
  lat = areaInfo.value.latitude || 0,
  lng = areaInfo.value.longitude || 0
) => {
  areaInfo.value.latitude = validate_latitude(lat, len.value)
  areaInfo.value.longitude = validate_longitude(lng, len.value)
  center.value = { lat: areaInfo.value.latitude, lng: areaInfo.value.longitude }
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

function getAreaFromAPI() {
  areaStore
    .getAreaByLatAndLon(areaInfo.value.latitude, areaInfo.value.longitude)
    .then((res) => {
      areaInfo.value = res.data
      codeList.value = [
        areaInfo.value.code.slice(0, 2),
        areaInfo.value.code.slice(0, 4),
        areaInfo.value.code
      ]
      ifHaveArea.value = true
      return true
    })
    .catch(() => {
      ifHaveArea.value = false
      areaInfo.value.id = -1
      areaInfo.value.name = ''
      areaInfo.value.description = ''
      codeList.value = ['00', '0000', '000000']
      return false
    })
}

const modifyArea = lockFunction()(() => {
  if (ifHaveArea.value) {
    areaStore.updateArea(areaInfo.value.id, areaInfo.value, false)
  } else {
    areaStore.createArea(areaInfo.value, false).then((res) => {
      areaInfo.value = res.data
      ifHaveArea.value = true
    })
  }
})

function areaSelected(value) {
  const address = value[1].reduce((pre, cur) => {
    return pre + cur
  }, '')
  addressStore
    .geocode(address)
    .then((res) => {
      const lngLat = res.result.location
      areaInfo.value.latitude = validate_latitude(lngLat.lat, len.value)
      areaInfo.value.longitude = validate_longitude(lngLat.lng, len.value)
      center.value = { lat: areaInfo.value.latitude, lng: areaInfo.value.longitude }
    })
    .catch((e) => {
      $errorMsg(e.message)
    })
}

onBeforeMount(() => {
  getAreaFromAPI()
})
</script>

<style scoped>
.map {
  width: 100%;
  height: 75%;
  margin-bottom: 20px;
}

.ctrl {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1001;
  display: flex;
  align-items: center;
}

.addArea {
  display: flex;
  justify-content: space-around;
}

.up-and-down-box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
}
</style>
