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
    <el-form-item v-if="ifNew" label="充电宝">
      <el-select v-model="powerBankInfo.power_bank" placeholder="请选择">
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
        :value="powerBankInfo.power_bank + '.' + powerBankInfo.power_bank_name"
        :disabled="true"
      ></el-input>
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="powerBankInfo.status" placeholder="请选择" :disabled="finished">
        <el-option
          v-for="(label, value) in spbConfigStore.getErrorStatusChoices()"
          :key="value"
          :label="label"
          :value="value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="维护人员"
      v-if="
        jwtTokenStore.getIdentityCode() === identityStore.SuperAdmin ||
        jwtTokenStore.getIdentityCode() === identityStore.Admin ||
        powerBankInfo.finished
      "
    >
      <el-select
        v-model="powerBankInfo.maintainer_account"
        placeholder="请选择"
        :disabled="finished"
      >
        <el-option
          v-for="item in maintainerList"
          :key="item.id"
          :label="item.id + '.' + item.name"
          :value="item.id"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="维护人员" v-else>
      <el-input :value="userInfo[0].id + '.' + userInfo[1].username" :disabled="true" />
    </el-form-item>
    <el-form-item label="问题描述" :maxlength="50"
      ><el-input v-model="powerBankInfo.question_description" :disabled="finished"></el-input
    ></el-form-item>
    <el-form-item v-if="!ifNew" label="处理时间">
      <el-date-picker
        v-model="powerBankInfo.date"
        type="datetime"
        placeholder="选择日期"
        format="YYYY/MM/DD HH:mm:ss"
        value-format="YYYY-MM-DD HH:mm:ss"
        :disabled="finished"
      ></el-date-picker>
    </el-form-item>
    <el-form-item v-if="!ifNew" label="是否处理">
      <el-switch v-model="powerBankInfo.finished" :disabled="finished"></el-switch>
    </el-form-item>
    <el-form-item v-if="!ifNew" label="维护结果" :maxlength="50">
      <el-input v-model="powerBankInfo.maintenance_result" :disabled="finished"></el-input>
    </el-form-item>
    <el-form-item label="处理后状态">
      <el-select v-model="powerBankInfo.new_status" placeholder="请选择" :disabled="finished">
        <el-option
          v-for="(label, value) in spbConfigStore.getPowerBankStatusChoices()"
          :key="value"
          :label="label"
          :value="value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item v-if="!finished">
      <el-button type="success" @click="onSubmit">{{
        ifNew ? '新增充电宝' : '更新充电宝'
      }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref, defineProps, computed } from 'vue'
import { useJwtTokenStore, useIdentityStore } from '@/stores/authenticationStore'
import { useUserStore } from '@/stores/userStore'
import { useSPBConfigStore, useSPBMaintenanceStore } from '@/stores/SPBStore'
import { useMaintainNameStore, usePowerBankNameStore } from '@/stores/nameList.js'
import { lockFunction } from '@/utils/myLock'

const spbConfigStore = useSPBConfigStore()
const powerBankNameStore = usePowerBankNameStore()
const spbMaintenance = useSPBMaintenanceStore()
const maintainNameStore = useMaintainNameStore()
const jwtTokenStore = useJwtTokenStore()
const identityStore = useIdentityStore()
const userStore = useUserStore()

const powerBankList = computed(() => powerBankNameStore.showList())
const maintainerList = computed(() => maintainNameStore.showList())

const finished = ref(false)

const powerBankInfo = ref({
  id: -1,
  power_bank: null,
  power_bank_name: null,
  status: '3',
  maintainer_account: null,
  question_description: null,
  finished: false,
  date: null,
  maintenance_result: '',
  new_status: '1'
})

const userInfo = ref([{ id: -1 }, { username: null }])

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
  let inputData = { ...powerBankInfo.value }
  delete inputData.power_bank_name
  if (ifNew.value) {
    spbMaintenance
      .createInfo(inputData)
      .then((res) => {
        // console.log(res)
      })
      .catch((err) => {})
  } else {
    spbMaintenance
      .updateInfo(props.id, inputData)
      .then((res) => {
        // console.log(res)
        finished.value = res.data.finished
      })
      .catch((err) => {})
  }
})

onBeforeMount(() => {
  if (!ifNew.value) {
    spbMaintenance.getInfo(props.id).then((res) => {
      powerBankInfo.value = res.data
      powerBankInfo.value.status = res.data.status.toString()
      powerBankInfo.value.new_status = '0'
      finished.value = res.data.finished

      if (jwtTokenStore.getIdentityCode() === identityStore.Maintainer) {
        userStore
          .getMyInfo()
          .then((res) => {
            userInfo.value = res.data
            powerBankInfo.value.maintainer_account = userInfo.value[0].id
          })
          .catch((e) => {})
      }
    })
  } else {
    powerBankNameStore
      .initList()
      .then((res) => {})
      .catch((e) => {})

    if (jwtTokenStore.getIdentityCode() === identityStore.Maintainer) {
      userStore
        .getMyInfo()
        .then((res) => {
          userInfo.value = res.data
          powerBankInfo.value.maintainer_account = userInfo.value[0].id
        })
        .catch((e) => {})
    }
  }

  maintainNameStore
    .initList()
    .then((res) => {
      maintainerList.value = res.data
    })
    .catch((e) => {})
})
</script>

<style scoped></style>
