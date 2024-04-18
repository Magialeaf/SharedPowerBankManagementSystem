<template>
    <el-form label-position="left" label-width="20%" :model="merchantInfo" style="max-width: 600px">
      <el-form-item v-if="merchantInfo.id" label="商户名称">
        <el-input v-model="merchantInfo.shop_name" :maxlength="shopNameLen"></el-input>
      </el-form-item>
      <el-form-item v-if="merchantInfo.id" label="商户区域">
        <SelectArea :codeList="codeList" @areaSelected="areaSelected" />
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
        <el-button type="success" @click="updateMerchant">保存修改</el-button>
      </el-form-item>
    </el-form>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useMerchantStore } from '@/stores/merchantStore'
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
  
  const merchantStore = useMerchantStore()
  
  const ifUploadValue = ref(false)
  const codeList = ['00', '0000', '000000']
  
  function areaSelected(value) {
    codeList.value = value[0]
    merchantInfo.value.area = codeList.value[2]
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
  
  const onUpdateImgUrl = (value) => {
    merchantInfo.value.shop_img = value
  }
  const onUpdateIfUpload = (value) => {
    ifUploadValue.value = value
  }
  
  const updateMerchant = () => {
    if (!validate_shop_name(merchantInfo.value.shop_name)) return false
    if (!validate_address(merchantInfo.value.address)) return false
    if (!validate_liaison(merchantInfo.value.liaison)) return false
    if (!validate_phone(merchantInfo.value.phone)) return false
    ifUploadValue.value = true
  }
  
  function afterUploadImgSuccess(value) {
    merchantInfo.value.shop_img = value.data.shop_img
    merchantStore.createMerchant(merchantInfo.value, false)
  }
  </script>
  