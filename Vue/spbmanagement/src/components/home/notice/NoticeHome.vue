<template>
  <div class="home">
    <div class="title">
      <SubHeader :title="data.title" />
    </div>
    <div class="content">
      <SubContent :data="data" :tips="tips" />
    </div>
    <div class="operation"></div>
    <div class="footer"></div>
  </div>
</template>
<script setup>
import { onBeforeMount, ref } from 'vue'
import { useNoticeStore } from '@/stores/noticeStore'
import { useRoute } from 'vue-router'
import SubHeader from '@/components/home/utils/SubHeader.vue'
import SubContent from '@/components/home/utils/SubContent.vue'

const noticeStore = useNoticeStore()
const route = useRoute()
const nowId = ref(route.params.id)

const data = ref({
  id: nowId.value,
  name: ''
})

const tips = ref({
  id: '公告id',
  title: '公告标题',
  uid: '发布者用户id',
  uid_name: '发布者用户名',
  content: '公告内容',
  type_name: '公告类型',
  create_time: '创建时间',
  update_time: '更新时间'
})

onBeforeMount(() => {
  noticeStore
    .getInfo(nowId.value)
    .then((res) => {
      data.value = res.data
    })
    .catch((e) => {})
})
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
</style>
