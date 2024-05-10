<template>
  <div class="home">
    <div class="title"></div>
    <div class="content">
      <SubContent :data="data" :tips="tips" />
    </div>
    <div class="divide-line">
      <hr />
    </div>
    <div class="operation">
      <div class="Record-box">
        <UseRecord :data="orderData" />
      </div>
      <div class="pagination">
        <Pagination
          :pageInfo="orderStore.getPageInfo()"
          @page-change="handlePageChange"
          :ifGoTop="false"
        />
      </div>
    </div>
    <div class="footer"></div>
  </div>
  <div class="home"></div>
</template>

<script setup>
import { computed, onBeforeMount, nextTick } from 'vue'
import { useOrderUserStore } from '@/stores/orderStore'
import UseRecord from '@/components/home/user/UseRecord.vue'
import SubContent from '@/components/home/utils/SubContent.vue'

const props = defineProps({
  data: { type: Object, default: () => {} }
})

const data = computed(() => props.data)
const orderData = computed(() => orderStore.showList())

const tips = {
  uid: 'uid',
  username: '用户信息',
  profile: '简介',
  sex: '性别',
  email: '邮箱',
  birthday: '生日',
  create_time: '创建时间',
  last_login_time: '上次登录时间'
}

const orderStore = useOrderUserStore()

onBeforeMount(() => {
  orderStore
    .initList()
    .then((res) => {})
    .catch((e) => {})
})

function handlePageChange(page) {
  orderStore
    .getList(page)
    .then((res) => {
      nextTick(() => {
        window.scrollTo({ top: 500, behavior: 'smooth' }) // 执行平滑滚动
      })
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

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  margin-bottom: 10px;
}
</style>
