<template>
  <p class="title-tip">共享充电宝管理系统 -- {{ title }}</p>
</template>

<script setup>
import { computed, defineProps } from 'vue'
import { useChangeThemeColorStore } from '@/stores/themeColor.js'
const changeThemeColor = useChangeThemeColorStore()
const titleBorderColor = computed(() => changeThemeColor.getCurrentColor())

const props = defineProps({
  title: {
    type: String,
    default: ''
  }
})

const title = computed(() => props.title)
</script>

<style>
.title-tip {
  margin: 13px 0px;
  border-top: 2px dashed v-bind(titleBorderColor);
  border-bottom: 2px dashed v-bind(titleBorderColor);
}
</style>
