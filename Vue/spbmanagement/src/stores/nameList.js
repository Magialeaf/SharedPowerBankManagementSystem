import { defineStore } from 'pinia'
import { ref } from 'vue'
import { $errorMsg } from '@/utils/msg'
import { getUserNameListAPI, getMaintainNameListAPI } from '@/api/userAPI.js'
import { getPowerBankNameListAPI } from '@/api/powerBankAPI.js'

// 获得维护人员名字列表
export const useMaintainNameStore = defineStore('maintainNameList', () => {
  const maintainNameList = ref([])
  async function initList(conditions) {
    return getMaintainNameListAPI(conditions)
      .then((res) => {
        maintainNameList.value = res.data
        return res
      })
      .catch(handleApiError)
  }

  function showList() {
    return maintainNameList.value
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return { showList, initList }
})

// 获取充电宝名字列表
export const usePowerBankNameStore = defineStore('powerBankNameList', () => {
  const powerBankNameList = ref([])
  async function initList() {
    return getPowerBankNameListAPI()
      .then((res) => {
        powerBankNameList.value = res.data
        return res
      })
      .catch(handleApiError)
  }

  function showList() {
    return powerBankNameList.value
  }

  function getList(conditions) {
    return getPowerBankNameListAPI(conditions)
      .then((res) => {
        powerBankNameList.value = res.data
        return res
      })
      .catch(handleApiError)
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return { showList, getList, initList }
})

// 获取用户名字列表
export const useUserNameStore = defineStore('userNameList', () => {
  const userNameList = ref([])
  async function initList() {
    return getUserNameListAPI()
      .then((res) => {
        userNameList.value = res.data
        return res
      })
      .catch(handleApiError)
  }

  function showList() {
    return userNameList.value
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }
  return { showList, initList }
})
