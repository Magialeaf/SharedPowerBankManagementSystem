<template>
  <div class="cards-container">
    <Card v-for="item in noticeList" :key="item.id" :data="item" @card-clicked="cardClicked" />
  </div>
</template>
<script setup>
import { computed } from 'vue'
import Card from '@/components/home/utils/Card.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const noticeList = computed(() => props.data)

const props = defineProps({
  data: {
    type: Object,
    default: () => {}
  }
})

function cardClicked(id) {
  router.push({ name: 'notice-id', params: { id } })
}
</script>

<style scoped>
.cards-container {
  display: flex;
  flex-wrap: wrap; /* 允许卡片换行 */
  gap: 1.2rem; /* 卡片之间的间距 */
  justify-content: space-between; /* 分布在一行上，两端对齐 */
}
</style>
