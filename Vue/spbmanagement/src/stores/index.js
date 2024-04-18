import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStudioStore = defineStore('Studio', () => {
  const studioName = ref('共享充电宝管理系统')
  const webVersion = ref('V1.0')

  return { studioName, webVersion }
})
