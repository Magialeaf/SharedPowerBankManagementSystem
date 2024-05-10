<template>
  <div class="card" @click="handleClick">
    <div class="card-image">
      <img :src="data?.shop_img || data?.img || ''" alt="Card Image" />
    </div>
    <div class="card-content">
      <div class="card-top">
        <div class="card-title">{{ data?.shop_name || data?.name || data?.title || '' }}</div>
      </div>
      <div class="card-bottom">
        <div class="card-extra">{{ data?.areaName || data?.update_time }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits, defineProps } from 'vue'

const props = defineProps({
  data: { type: Object, required: true }
})

const data = computed(() => props.data)

const handleClick = () => {
  emit('card-clicked', data.value.id)
}

const emit = defineEmits(['card-clicked'])
</script>

<style scoped>
.card {
  display: flex;
  height: 150px;
  width: 49%;
  cursor: pointer;
  transition: transform 0.2s;
  border: 3px solid rgba(206, 201, 201, 0.2);
  box-shadow: 0 0 0 rgba(0, 0, 0, 0);
  padding: 5px;
}

/* 鼠标悬停时添加阴影效果，保留上浮效果 */
.card:hover,
.card[aria-selected='true'] {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-image {
  height: 100%;
  width: 30%;
  margin-right: 1.2rem;
}

.card-image img {
  width: 100%;
  height: 100%;
}

.card-title {
  margin: 0;
  font-size: 19px;
  font-weight: bold;
  white-space: nowrap; /* 防止标题换行 */
  overflow: hidden; /* 避免标题过长时溢出 */
  text-overflow: ellipsis; /* 添加省略号 */
}

.card-content {
  width: calc(70% - 1.2rem);
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
}

.card-top {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-end;
  overflow: hidden; /* 防止内容溢出 */
}

.card-extra {
  margin: 0;
  font-size: 14px;
  color: #666;
  white-space: wrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
