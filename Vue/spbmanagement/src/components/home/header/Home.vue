<template>
  <div class="hot-partner box">
    <div class="title partner-title">热门合作商户</div>
    <div class="bubble-container">
      <Bubble
        v-for="(item, index) in merchantData"
        :data="item"
        :key="index"
        @bubble-clicked="(value) => jumpContent('partner-id', value)"
      />
    </div>
    <div class="more-btn">
      <el-button type="primary" @click="jumpPage('/partner')">查看更多</el-button>
    </div>
  </div>
  <div class="hot-product box">
    <div class="title product-title">热门充电宝</div>
    <div class="bubble-container">
      <Bubble
        v-for="(item, index) in powerBankData"
        :data="item"
        :key="index"
        @bubble-clicked="(value) => jumpContent('product-id', value)"
      />
    </div>
    <div class="more-btn">
      <el-button type="primary" @click="jumpPage('/product')">查看更多</el-button>
    </div>
  </div>
  <div class="new-notice box">
    <div class="title notice-title">最新公告</div>
    <div class="bubble-container">
      <Bubble
        v-for="(item, index) in noticeData"
        :data="item"
        :key="index"
        @bubble-clicked="(value) => jumpContent('notice-id', value)"
      />
    </div>
    <div class="more-btn">
      <el-button type="primary" @click="jumpPage('/notice')">查看更多</el-button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onBeforeMount } from 'vue'
import { getHotMerchantListAPI } from '@/api/merchantAPI'
import { getHotPowerBankListAPI } from '@/api/powerBankAPI'
import { useRouter } from 'vue-router'
import { useNoticeStore } from '@/stores/noticeStore'
import Bubble from '@/components/home/utils/Bubble.vue'
import { $errorMsg } from '@/utils/msg'

const noticeStore = useNoticeStore()

const merchantData = ref()
const powerBankData = ref()
const noticeData = computed(() => noticeStore.showList())

const router = useRouter()

onBeforeMount(() => {
  noticeStore
    .getList(1, { order_by: ['-update_time'] })
    .then(() => {})
    .catch((e) => {})
  getHotMerchantListAPI({ order_by: ['-update_time'] })
    .then((res) => {
      merchantData.value = res.data
    })
    .catch((e) => {
      $errorMsg(e.message)
    })
  getHotPowerBankListAPI({ order_by: ['-update_time'] })
    .then((res) => {
      powerBankData.value = res.data
    })
    .catch((e) => {
      $errorMsg(e.message)
    })
})

function jumpPage(url) {
  router.push(url)
}

function jumpContent(urlName, id) {
  router.push({ name: urlName, params: { id } })
}
</script>

<style scoped>
.box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 80px;
}

.title {
  font-size: 30px;
  font-weight: 600;
  margin-bottom: 30px;
}

.bubble-container {
  width: 100%;
  margin-left: 2%;
  display: flex;
  flex-wrap: wrap; /* 允许卡片换行 */
  gap: 2rem; /* 卡片之间的间距 */
  justify-content: flex-start;
}

.more-btn {
  margin: 20px 0px;
}
</style>
