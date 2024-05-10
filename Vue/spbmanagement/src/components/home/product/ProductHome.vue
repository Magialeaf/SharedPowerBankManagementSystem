<template>
  <div class="home">
    <div class="title">
      <SubHeader :title="data.name" />
    </div>
    <div class="content">
      <SubContent :data="data" :tips="tips" />
    </div>
    <div class="divide-line">
      <hr />
    </div>
    <div class="operation">
      <div class="button-box">
        <el-button :disabled="!data.merchant" type="primary" @click="jumpMerchant()"
          >跳转到对应商户</el-button
        >
        <el-button :disabled="!(data.status === 0)" type="primary" @click="lease()"
          >租用该充电宝</el-button
        >
      </div>
    </div>
    <div class="footer"></div>
  </div>
</template>
<script setup>
import { onBeforeMount, ref } from 'vue'
import { useOrderUserStore } from '@/stores/orderStore'
import { useSPBStore, useSPBConfigStore } from '@/stores/SPBStore'
import { useRoute, useRouter } from 'vue-router'
import SubHeader from '@/components/home/utils/SubHeader.vue'
import SubContent from '@/components/home/utils/SubContent.vue'

const powerBankStore = useSPBStore()
const spbConfigStore = useSPBConfigStore()
const orderUserStore = useOrderUserStore()
const route = useRoute()
const router = useRouter()
const nowId = ref(route.params.id)

const data = ref({
  id: nowId.value,
  name: '',
  merchant: null
})

const tips = ref({
  id: '充电宝id',
  name: '充电宝名称',
  area: '所属区域',
  status_name: '充电宝状态',
  merchant: '所属商户ID',
  hourly_fee: '每小时收费',
  electricity_percentage: '剩余电量'
})

onBeforeMount(() => {
  powerBankStore
    .getInfo(nowId.value)
    .then((res) => {
      data.value = res.data
    })
    .catch((e) => {})
})

function jumpMerchant() {
  router.push({ name: 'partner-id', params: { id: data.value.merchant } })
}

function lease() {
  orderUserStore
    .createInfo({ power_bank: nowId.value })
    .then((res) => {
      data.value.status = 2
      data.value.status_name = spbConfigStore.getStatusDisplay(data.value.status)
    })
    .catch((e) => {})
}
</script>

<style scoped>
.home {
  width: 70%;
  margin-left: 15%;
}

.title {
  width: 100%;
  margin-top: 90px;
}

.content {
  min-height: 400px;
  width: 100%;
  margin-top: 30px;
}

.divide-line {
  margin: 10px 0px;
}
</style>
