<template>
  <div class="home">
    <div class="title">
      <SubHeader :title="data.shop_name" />
    </div>
    <div class="content">
      <SubContent :data="data" :tips="tips" />
    </div>
    <div class="divide-line">
      <hr />
    </div>
    <div class="operation">
      <h2 class="operation-title">该商户管理的共享充电宝</h2>
      <div class="operation-content">
        <div class="charging-banks-row">
          <div
            v-for="(powerBank, index) in powerBankList"
            :key="index"
            class="power-bank-item"
            :class="{ 'last-in-row': index % 5 === 4 }"
            @click="showDetail(powerBank.id)"
          >
            <img class="power-bank-img" :src="powerBank.img" />
            <el-button class="power-bank-button" type="primary">
              {{ powerBank.name }}
            </el-button>
          </div>
        </div>
      </div>
    </div>
    <div class="footer"></div>
  </div>
</template>
<script setup>
import { computed, onBeforeMount, ref } from 'vue'
import { usePowerBankNameStore } from '@/stores/nameList'
import { useMerchantStore } from '@/stores/merchantStore'
import { useRoute, useRouter } from 'vue-router'
import SubHeader from '@/components/home/utils/SubHeader.vue'
import SubContent from '@/components/home/utils/SubContent.vue'

const merchantStore = useMerchantStore()
const powerBankNameStore = usePowerBankNameStore()

const route = useRoute()
const router = useRouter()
const nowId = ref(route.params.id)
const powerBankList = computed(() => powerBankNameStore.showList())

const data = ref({
  id: nowId.value,
  shop_name: ''
})

const tips = ref({
  id: '商户id',
  shop_name: '商户名称',
  area: '所属区域',
  address: '详细地址',
  liaison: '联系人',
  phone: '联系电话'
})

onBeforeMount(() => {
  merchantStore
    .getMerchant(nowId.value)
    .then((res) => {
      data.value = res.data
    })
    .catch((e) => {})
  powerBankNameStore
    .getList({ merchant: nowId.value })
    .then((res) => {
      // console.log(res)
      // console.log(powerBankList.value)
    })
    .catch((e) => {})
})

// 添加点击事件处理函数
const showDetail = (powerBankId) => {
  // 假设路由模式为 /powerBank/:id

  router.push({ name: 'product-id', params: { id: powerBankId } })
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

.operation-title {
  margin-top: 10px;
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
  width: 100%;
}

.operation-content {
  width: 100%;
  display: flex;
}

.charging-banks-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  width: 100%;
}

.last-in-row {
  margin-right: 0; /* 取消最后一列的右边距 */
}

.power-bank-item {
  flex: 0 0 calc(17% + 3px); /* 调整宽度并减去左右间距 */
  margin: 10px; /* 上下左右的外边距 */
  border: 1px solid rgb(64, 158, 255);
  border-radius: 3px;
  text-align: center;
  cursor: pointer;
}

.power-bank-img {
  width: 100%;
  height: 80%;
}

.power-bank-button {
  width: 100%;
  height: 20%;
  line-height: 20%; /* 确保文本垂直居中 */
  white-space: nowrap; /* 不换行 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 显示省略号 */
}
</style>
