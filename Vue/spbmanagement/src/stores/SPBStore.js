import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $successMsg, $errorMsg } from '@/utils/msg'
import { useAddressStore } from '@/stores/areaStore.js'

export const useSPBStore = defineStore('SPBList', () => {
  const pageInfo = ref(createPageInfo())

  const getPageInfo = () => {
    return pageInfo.value
  }

  return { getPageInfo }
})
