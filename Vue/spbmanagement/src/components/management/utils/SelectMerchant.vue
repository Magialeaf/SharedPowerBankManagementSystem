<template>
  <el-select v-model="merchantIdValue" @change="updateMerchantId" placeholder="请选择">
    <el-option
      v-for="value in merchantsList"
      :key="value.id"
      :label="value.name"
      :value="value.id"
    ></el-option>
  </el-select>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, computed } from 'vue'
import { useMerchantStore } from '@/stores/merchantStore'
import { $errorMsg } from '@/utils/msg'

const merchantStore = useMerchantStore()
const first = ref(true)

const props = defineProps({
  areaId: {
    required: true
  },
  merchantId: {
    required: true
  }
})
const areaId = computed(() => props.areaId)
const tempMerchantId = computed(() => props.merchantId)
const merchantIdValue = ref()

const merchantsList = ref([])

const emits = defineEmits(['update-merchant-id'])

watch(areaId, () => {
  if (areaId.value) {
    merchantStore
      .getMerchantByAreaId(areaId.value)
      .then((res) => {
        merchantsList.value = res.data
        console.log(merchantsList.value)
        if (merchantsList.value.length === 0) {
          if (!first.value) $errorMsg('该区域暂无商户')
          else first.value = false
          merchantIdValue.value = ''
        } else {
          let flag = false
          for (let i = 0; i < merchantsList.value.length; i++) {
            if (merchantsList.value[i].id === tempMerchantId.value) {
              flag = true
              break
            }
          }
          if (!flag) merchantIdValue.value = ''
        }
      })
      .catch((e) => {})
  }
})

watch(tempMerchantId, () => {
  if (merchantIdValue.value !== tempMerchantId.value) merchantIdValue.value = tempMerchantId.value
})

function updateMerchantId(id) {
  emits('update-merchant-id', id)
}
</script>

<style scoped></style>
