<template>
  <div class="bubble" @click="handleClick">
    <div class="bubble-img-box">
      <img class="bubble-img avatar" :src="avatarUrl" alt="" />
    </div>
    <div class="title-box">
      <div class="title">{{ data?.shop_name || data?.name || data?.title || '' }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const data = computed(() => props.data)

const avatarUrl = computed(() => {
  return data.value?.avatar ?? data.value?.shop_img ?? data.value?.img ?? ''
})

const handleClick = () => {
  emit('bubble-clicked', data.value.id)
}

const emit = defineEmits(['bubble-clicked'])
</script>

<style scoped>
.bubble {
  width: 31%;
  height: 250px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: transform 0.2s;
  padding: 5px;
}

/* 鼠标悬停时添加阴影效果，保留上浮效果 */
.bubble:hover,
.bubble[aria-selected='true'] {
  transform: translateY(-4px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.bubble-img-box {
  position: relative; /* 添加定位属性，以便应用溢出隐藏 */
  height: 75%;
  width: 50%;
  margin-right: 1rem;
  overflow: hidden; /* 隐藏超出容器的内容 */
}

/* 更新此处样式以使图片变为圆形 */
.bubble-img-box .bubble-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.title-box {
  height: 20%;
  width: 100%;
  margin-top: 5%;
  background: rgb(241, 241, 241);
  border: 1px solid rgb(241, 241, 241);
  border-radius: 10px;
  display: flex;
  justify-content: center;
}

.title {
  margin: 0;
  font-weight: bold;
  color: rgb(44, 120, 183);
  white-space: nowrap; /* 防止标题换行 */
  overflow: hidden; /* 避免标题过长时溢出 */
  text-overflow: ellipsis; /* 添加省略号 */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
