<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="powerBankInfo"
    style="max-width: 680px"
  >
    <el-form-item v-if="!ifNew" label="id">
      <el-input v-model="powerBankInfo.id" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item label="名称">
      <el-input v-model="powerBankInfo.name" :maxlength="20"></el-input>
    </el-form-item>
    <el-form-item label="图片">
      <UploadImg
        :imgUrl="powerBankInfo.img"
        :ifUpload="ifUploadValue"
        :uploadFunc="spbStore.uploadImg"
        @updateIfUpload="updateIfUpload"
        @updateImgUrl="updateImgUrl"
        @uploadSuccess="afterUploadImgSuccess"
      />
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="powerBankInfo.status" placeholder="请选择">
        <el-option
          v-for="(label, value) in spbConfigStore.getPowerBankStatusChoices()"
          :key="value"
          :label="label"
          :value="value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="所属地址">
      <SelectAddress
        :codeList="codeList"
        :areaOption="powerBankInfo.area"
        @select-area="selectArea"
        @clear-code-list="clearCodeList"
    /></el-form-item>
    <el-form-item label="管理商户">
      <SelectMerchant
        :areaId="powerBankInfo.area"
        :merchantId="powerBankInfo.merchant"
        @update-merchant-id="updateMerchantId"
      />
    </el-form-item>
    <el-form-item label="每小时费用（元）">
      <el-input
        @blur="onHourlyFeeInput"
        v-model="powerBankInfo.hourly_fee"
        :maxlength="13"
      ></el-input>
    </el-form-item>
    <el-form-item label="电量百分比">
      <el-input
        @blur="onElectricityPercentageInput"
        v-model="powerBankInfo.electricity_percentage"
      ></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="success" @click="onSubmit">{{
        ifNew ? '新增充电宝' : '更新充电宝'
      }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref, defineProps } from 'vue'
import { useSPBConfigStore, useSPBStore } from '@/stores/SPBStore'
import UploadImg from '@/components/management/utils/UploadImg.vue'
import SelectAddress from '@/components/management/utils/SelectAddress.vue'
import SelectMerchant from '@/components/management/utils/SelectMerchant.vue'
import { lockFunction } from '@/utils/myLock'

const spbConfigStore = useSPBConfigStore()
const spbStore = useSPBStore()

const codeList = ref(['00', '0000', '000000'])

const powerBankInfo = ref({
  id: -1,
  name: '',
  img: spbConfigStore.getDefaultImgURL(),
  status: '0',
  area: '',
  merchant: '',
  hourly_fee: 0,
  electricity_percentage: 100
})

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
const ifNew = ref(props.ifNew)

function onHourlyFeeInput() {
  const inputStr = powerBankInfo.value.hourly_fee.trim() // 移除前导和尾随空格
  const decimalSeparator = '.' // 定义小数点字符

  // 检查输入值是否包含非法字符或超过10位（包括小数点）
  if (!/^\d*\.?\d*$/.test(inputStr) || inputStr.split(decimalSeparator).length - 1 > 1) {
    powerBankInfo.value.hourly_fee = '0.00' // 设置为默认值
    return
  }

  if (inputStr.length > 10) {
    powerBankInfo.value.hourly_fee = '99999999.99' // 设置为默认值
    return
  }

  const parsedValue = parseFloat(inputStr, 10)

  if (isNaN(parsedValue)) {
    // 输入不是数字，设置为 0.00
    powerBankInfo.value.hourly_fee = '0.00'
    return
  }

  // 保留两位小数
  powerBankInfo.value.hourly_fee = parsedValue.toFixed(2)
}
function onElectricityPercentageInput() {
  const parsedValue = parseInt(powerBankInfo.value.electricity_percentage, 10)
  const formattedValue = !isNaN(parsedValue) ? Math.min(Math.max(parsedValue, 0), 100) : 50 // 若不是数字，则设置为 50
  powerBankInfo.value.electricity_percentage = formattedValue
}

const ifUploadValue = ref(false)
function updateImgUrl(value) {
  powerBankInfo.value.img = value
}
const updateIfUpload = (value) => {
  ifUploadValue.value = value
}

function onSubmit() {
  ifUploadValue.value = true
}

function selectArea(value) {
  powerBankInfo.value.area = value
}

function clearCodeList() {
  codeList.value = ['00', '0000', '000000']
  powerBankInfo.value.area = 0
}

const updateMerchantId = lockFunction()((value) => {
  powerBankInfo.value.merchant = value
})

function afterUploadImgSuccess(value) {
  let inputData = { ...powerBankInfo.value }
  inputData.img = value.data.img
  if (ifNew.value) {
    spbStore
      .createInfo(inputData)
      .then((res) => {
        console.log(res)
      })
      .catch((err) => {})
  } else {
    spbStore
      .updateInfo(props.id, inputData)
      .then((res) => {
        console.log(res)
      })
      .catch((err) => {})
  }
}

onBeforeMount(() => {
  if (!ifNew.value) {
    spbStore.getInfo(props.id).then((res) => {
      powerBankInfo.value = res.data
      console.log(res.data.status)
      powerBankInfo.value.status = res.data.status.toString()
      if (res.data.area_code) {
        codeList.value = [
          res.data.area_code.slice(0, 2),
          res.data.area_code.slice(0, 4),
          res.data.area_code.slice(0, 6)
        ]
      }
    })
  }
})
</script>

<style scoped></style>
