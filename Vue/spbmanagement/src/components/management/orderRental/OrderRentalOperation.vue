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
    <el-form-item v-if="!ifNew && !hadReturned" label="归还">
      <el-switch
        v-model="orderInfo.returned"
        active-color="#13ce66"
        inactive-color="#ff4949"
      ></el-switch>
    </el-form-item>
    <el-form-item v-if="!ifNew" label="租赁日期">
      <el-input v-model="orderInfo.rental_date" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button v-if="!hadReturned" type="success" @click="onSubmit">{{
        ifNew ? '新增租赁记录' : '更新租赁记录'
      }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref, defineProps, computed } from 'vue'
import { useOrderRentalStore } from '@/stores/orderStore'
import { useUserNameStore, usePowerBankNameStore } from '@/stores/nameList.js'
import { lockFunction } from '@/utils/myLock'

const powerBankNameStore = usePowerBankNameStore()
const orderRentalStore = useOrderRentalStore()
const userNameStore = useUserNameStore()

const powerBankList = computed(() => powerBankNameStore.showList())
const userList = computed(() => userNameStore.showList())

const orderInfo = ref({
  id: -1,
  power_bank: null,
  power_bank_name: null,
  user: null,
  user_name: null,
  returned: false,
  rental_date: null
})

const hadReturned = ref(false)

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
    orderRentalStore
      .createInfo(inputData)
      .then((res) => {
        // console.log(res)
      })
      .catch((err) => {})
  } else {
    orderRentalStore
      .updateInfo(props.id, inputData)
      .then((res) => {
        orderInfo.value = res.data
        hadReturned.value = res.data.returned
      })
      .catch((err) => {})
  }
})

onBeforeMount(() => {
  if (!ifNew.value) {
    orderRentalStore.getInfo(props.id).then((res) => {
      orderInfo.value = res.data
      hadReturned.value = res.data.returned
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
