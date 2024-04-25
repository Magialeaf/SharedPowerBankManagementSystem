<template>
  <el-form label-position="left" label-width="20%" :model="merchantInfo" style="max-width: 600px">
    <el-form-item v-if="merchantInfo.id" label="商户名称">
      <el-input v-model="merchantInfo.shop_name" :maxlength="shopNameLen"></el-input>
    </el-form-item>
    <el-form-item v-if="merchantInfo.id" label="商户区域">
      <SelectArea :codeList="codeList" @areaSelected="areaSelected" />
      <el-select
        v-model="merchantInfo.area"
        placeholder="具体区域"
        style="width: 218px; margin-left: 42px; margin-top: 2px"
      >
        <el-option v-for="item in areaOptions" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
    </el-form-item>
    <el-form-item v-if="merchantInfo.id" label="商户地址">
      <el-input v-model="merchantInfo.address" :maxlength="addressLen"></el-input>
    </el-form-item>
    <el-form-item v-if="merchantInfo.id" label="联系人">
      <el-input v-model="merchantInfo.liaison" :maxlength="liaisonLen"></el-input>
    </el-form-item>
    <el-form-item v-if="merchantInfo.id" label="联系电话">
      <el-input v-model="merchantInfo.phone" :maxlength="phoneLen"></el-input>
    </el-form-item>
    <el-form-item v-if="merchantInfo.id" label="商户图片">
      <UploadImg
        :imgUrl="merchantInfo.shop_img"
        :ifUpload="ifUploadValue"
        :uploadFunc="merchantStore.uploadImg"
        @updateIfUpload="onUpdateIfUpload"
        @updateImgUrl="onUpdateImgUrl"
        @uploadSuccess="afterUploadImgSuccess"
      />
    </el-form-item>
    <el-form-item v-if="merchantInfo.id">
      <el-button type="success" @click="updateMerchant">{{
        ifNew ? '新建商户' : '更新信息'
      }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { useMerchantStore } from '@/stores/merchantStore'
import { useAreaStore } from '@/stores/areaStore'
import {
  shopNameLen,
  addressLen,
  liaisonLen,
  phoneLen,
  validate_shop_name,
  validate_address,
  validate_liaison,
  validate_phone
} from '@/utils/validateMerchant'
import UploadImg from '@/components/management/utils/UploadImg.vue'
import SelectArea from '@/components/management/utils/SelectArea.vue'
import { lockFunction } from '@/utils/myLock'

const merchantStore = useMerchantStore()
const areaStore = useAreaStore()

const ifUploadValue = ref(false)
const areaOptions = ref([])
const codeList = ref(['00', '0000', '000000'])

const props = defineProps({
  id: {
    type: Number,
    default: -1
  },
  ifNew: {
    type: Boolean,
    default: false
  }
})

function areaSelected(value) {
  codeList.value = value[0]
  areaStore
    .getAreaNameList(codeList.value[2])
    .then((res) => {
      areaOptions.value = res.data
    })
    .catch((e) => {
      merchantInfo.value.area = null
      areaOptions.value = []
    })
}

const merchantInfo = ref({
  id: -1,
  shop_name: '',
  area: '',
  address: '',
  liaison: '',
  phone: '',
  shop_img: ''
})

onBeforeMount(() => {
  if (!props.ifNew) {
    merchantInfo.value.id = props.id
    merchantStore
      .getMerchant(props.id)
      .then((res) => {
        merchantInfo.value = res.data
        codeList.value = res.data.areaCodeList
        areaSelected([codeList.value, ''])
      })
      .catch((e) => {})
  }
})

const onUpdateImgUrl = (value) => {
  merchantInfo.value.shop_img = value
}
const onUpdateIfUpload = (value) => {
  ifUploadValue.value = value
}

const updateMerchant = lockFunction()(() => {
  if (!validate_shop_name(merchantInfo.value.shop_name)) return false
  if (!validate_address(merchantInfo.value.address)) return false
  if (!validate_liaison(merchantInfo.value.liaison)) return false
  if (!validate_phone(merchantInfo.value.phone)) return false
  ifUploadValue.value = true
})

function afterUploadImgSuccess(value) {
  let inputData = { ...merchantInfo.value }
  inputData.shop_img = value.data.img
  if (props.ifNew) {
    merchantStore
      .createMerchant(inputData, false)
      .then((res) => {})
      .catch((e) => {})
  } else {
    merchantStore
      .updateMerchant(inputData.id, inputData, true)
      .then((res) => {
        merchantInfo.value = res.data[0]
        codeList.value = [
          res.data[0].area_data.slice(0, 2),
          res.data[0].area_data.slice(0, 4),
          res.data[0].area_data.slice(0, 6)
        ]
      })
      .catch((e) => {})
  }
}
</script>

<style scoped>
.el-select__wrapper {
  padding-top: 0px;
  padding-bottom: 0px;
}
</style>
