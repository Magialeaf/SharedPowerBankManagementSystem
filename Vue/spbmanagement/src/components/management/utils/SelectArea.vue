<template>
  <div id="app">
    <span class="tip" :style="props.tip ? tipStyles : {}">{{ props.tip }}</span>
    <el-cascader
      :options="regionData"
      v-model="selectedOptions"
      @change="handleAreaChange"
    ></el-cascader>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, computed, onBeforeMount } from 'vue'
import { regionData } from 'element-china-area-data'
import { useAddressStore } from '@/stores/areaStore'

const addressStore = useAddressStore()

const props = defineProps({
  tip: String,
  codeList: Array
})

const tipStyles = {
  fontSize: '14px',
  paddingRight: '12px'
}

const selectedOptions = ref()
const tempSelectedOptions = computed(() => props.codeList)

watch(tempSelectedOptions, () => {
  selectedOptions.value = tempSelectedOptions.value
})
const emit = defineEmits(['areaSelected'])

function handleAreaChange(selectedOptions) {
  const selectedName = addressStore.codeListToAddrList(selectedOptions)
  emit('areaSelected', [selectedOptions, selectedName])
}

onBeforeMount(() => {
  selectedOptions.value = tempSelectedOptions.value
})
</script>

<style scoped></style>
