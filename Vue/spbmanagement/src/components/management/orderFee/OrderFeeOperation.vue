<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="orderInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="!ifNew" label="id">
      <el-input v-model="orderInfo.id" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item v-if="ifNew" label="充电宝">
      <el-select v-model="orderInfo.power_bank" placeholder="请选择">
        <el-option
          v-for="item in powerBankList"
          :key="item.id"
          :label="item.id + '.' + item.name"
          :value="item.id"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item v-else label="充电宝">
      <el-input
        :value="orderInfo.power_bank + '.' + orderInfo.power_bank_name"
        :disabled="true"
      ></el-input>
    </el-form-item>
    <el-form-item v-if="ifNew" label="用户">
      <el-select v-model="orderInfo.user" placeholder="请选择">
        <el-option
          v-for="item in userList"
          :key="item.id"
          :label="item.id + '.' + item.name"
          :value="item.id"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item v-else label="用户">
      <el-input :value="orderInfo.user + '.' + orderInfo.user_name" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item v-if="!ifNew && !hadPaid" label="是否支付">
      <el-switch
        v-model="orderInfo.paid"
        active-color="#13ce66"
        inactive-color="#ff4949"
      ></el-switch>
    </el-form-item>
    <el-form-item v-if="!ifNew" label="费用">
      <el-input v-model="orderInfo.fee" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button v-if="!hadPaid" type="success" @click="onSubmit">{{
        ifNew ? '新增缴费记录' : '更新缴费记录'
      }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref, defineProps, computed } from 'vue'
import { useOrderFeeStore } from '@/stores/orderStore'
import { useUserNameStore, usePowerBankNameStore } from '@/stores/nameList.js'
import { lockFunction } from '@/utils/myLock'

const powerBankNameStore = usePowerBankNameStore()
const orderFeeStore = useOrderFeeStore()
const userNameStore = useUserNameStore()

const powerBankList = computed(() => powerBankNameStore.showList())
const userList = computed(() => userNameStore.showList())

const orderInfo = ref({
  id: -1,
  power_bank: null,
  power_bank_name: null,
  user: null,
  user_name: null,
  fee: 0,
  paid: false
})

const hadPaid = ref(false)

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

const onSubmit = lockFunction()(() => {
  let inputData = { ...orderInfo.value }
  delete inputData.power_bank_name
  delete inputData.user_name
  if (ifNew.value) {
    orderFeeStore
      .createInfo(inputData)
      .then((res) => {
        // console.log(res)
      })
      .catch((err) => {})
  } else {
    orderFeeStore
      .updateInfo(props.id, inputData)
      .then((res) => {
        orderInfo.value = res.data
        hadPaid.value = res.data.paid
      })
      .catch((err) => {})
  }
})

onBeforeMount(() => {
  if (!ifNew.value) {
    orderFeeStore.getInfo(props.id).then((res) => {
      orderInfo.value = res.data
      hadPaid.value = res.data.paid
    })
  } else {
    powerBankNameStore
      .initList()
      .then((res) => {})
      .catch((e) => {})
    userNameStore
      .initList()
      .then((res) => {
        orderInfo.value = res.data
      })
      .catch((e) => {})
  }
})
</script>

<style scoped></style>
