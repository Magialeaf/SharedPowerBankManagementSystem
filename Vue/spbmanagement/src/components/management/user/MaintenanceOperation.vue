<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="10%"
    :model="areaOptions"
    style="max-width: 700px"
  >
    <el-form-item v-for="(codeList, index) in codeLists" :key="index" :label="`区域${index + 1}`">
      <SelectAddress
        :codeList="codeList"
        :areaOption="areaOptions[index]"
        @select-area="(value) => selectArea(index, value)"
        @clear-code-list="() => clearCodeList(index)"
      />
    </el-form-item>

    <el-form-item>
      <el-button type="success" @click="onSubmit">提交</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, defineProps, onBeforeMount } from 'vue'
import { lockFunction } from '@/utils/myLock'
import { useMaintainStore } from '@/stores/maintainStore'
import { useUserStore } from '@/stores/userStore'
import SelectAddress from '@/components/management/utils/SelectAddress.vue'

const props = defineProps({
  aid: { type: Number }
})

const userStore = useUserStore()
const maintainStore = useMaintainStore()

const codeLists = ref([])

const maintenanceId = ref([0, 0, 0])
const areaOptions = ref([0, 0, 0])

function selectArea(index, value) {
  if (typeof value === 'string') {
    value = parseInt(value, 10) || 0
  }

  areaOptions.value[index] = value
}

function clearCodeList(index) {
  codeLists.value[index] = ['00', '0000', '000000']
}

const onSubmit = lockFunction()(() => {
  let uploadAreaOptions = areaOptions.value
  uploadAreaOptions = uploadAreaOptions.map((value) => (value === null ? 0 : value))

  maintainStore
    .updateMaintain(props.aid, maintenanceId.value, uploadAreaOptions)
    .then((res) => {
      userStore
        .getUserList()
        .then((res) => {})
        .catch((e) => {})
    })
    .catch((e) => {})
})

onBeforeMount(() => {
  maintainStore
    .getMaintain(props.aid)
    .then((res) => {
      for (let i = 0; i < res.data.length; i++) {
        maintenanceId.value[i] = res.data[i].id
        areaOptions.value[i] = res.data[i].area_id
        codeLists.value[i] = [
          res.data[i].code.slice(0, 2),
          res.data[i].code.slice(0, 4),
          res.data[i].code.slice(0, 6)
        ]
      }
    })
    .catch((e) => {})
})
</script>

<style scoped></style>
