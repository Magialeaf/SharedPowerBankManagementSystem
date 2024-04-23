<template>
  <SelectArea v-model:codeList="codeList" @areaSelected="handleSelect" />
  <el-select v-model="selectArea" placeholder="具体区域" style="width: 218px; margin-left: 42px">
    <el-option v-for="item in areaOptions" :key="item.id" :label="item.name" :value="item.id" />
  </el-select>
  <el-button class="search-btn" type="primary" @click="clearCode()">清空</el-button>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, onBeforeMount } from 'vue'
import { useAreaStore } from '@/stores/areaStore'

const areaStore = useAreaStore()
const areaOptions = ref([])

const props = defineProps({
  codeList: {
    type: Array
  },
  areaOption: {
    type: Number
  }
})

const codeList = ref(props.codeList)
const selectArea = ref(props.areaOption)

const emits = defineEmits(['select-area', 'clear-code-list'])

function handleSelect(lst) {
  areaStore
    .getAreaNameList(lst[0][2])
    .then((res) => {
      areaOptions.value = res.data
    })
    .catch((e) => {})
}

watch(selectArea, (val) => {
  emits('select-area', val)
})

function clearCode() {
  emits('clear-code-list')
  codeList.value = ['00', '0000', '000000']
  selectArea.value = ''
}

onBeforeMount(() => {
  areaStore
    .getAreaNameList(codeList.value[2], false)
    .then((res) => {
      areaOptions.value = res.data
    })
    .catch((e) => {})
})
</script>

<style scoped></style>
