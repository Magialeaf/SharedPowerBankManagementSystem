import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createPageInfo } from '@/stores/pageInfo.js'
import { convertBackendTimestampToLocalTime } from '@/utils/convert.js'
import { $successMsg, $errorMsg } from '@/utils/msg'
import { useAddressStore } from '@/stores/areaStore.js'
import {
  getPowerBankAPI,
  getPowerBankListAPI,
  createPowerBankAPI,
  updatePowerBankAPI,
  deletePowerBankAPI,
  uploadPowerBankImgAPI,
  getPowerBankMaintenanceAPI,
  getPowerBankMaintenanceListAPI,
  createPowerBankMaintenanceAPI,
  updatePowerBankMaintenanceAPI,
  deletePowerBankMaintenanceAPI
} from '@/api/powerBankAPI.js'

export const useSPBConfigStore = defineStore('SPBConfig', () => {
  const defaultImgURL = ref('http://127.0.0.1:8000/media/images/power_bank_img/default.png')

  const powerBankStatusChoices = ref({
    0: '空闲',
    1: '充电中',
    2: '已借出',
    3: '已损坏',
    4: '已报废'
  })

  const powerBankErrorStatusChoices = ref({
    3: '已损坏',
    4: '已报废'
  })

  function getDefaultImgURL() {
    return defaultImgURL.value
  }

  function getPowerBankStatusChoices() {
    return powerBankStatusChoices.value
  }

  function getStatusDisplay(status) {
    return powerBankStatusChoices.value[status]
  }

  function getErrorStatusChoices() {
    return powerBankErrorStatusChoices.value
  }

  function getErrorStatusDisplay(status) {
    return powerBankErrorStatusChoices.value[status]
  }

  return {
    getDefaultImgURL,
    getPowerBankStatusChoices,
    getStatusDisplay,
    getErrorStatusChoices,
    getErrorStatusDisplay
  }
})

// 充电宝列表
export const useSPBStore = defineStore('SPBList', () => {
  const addressStore = useAddressStore()

  const dataList = ref([])

  const constConditions = ref({})
  const getConditions = ref()
  const uploadConditions = ref({})

  const pageInfo = ref(createPageInfo())

  const powerBankConfig = useSPBConfigStore()

  const getPageInfo = () => {
    return pageInfo.value
  }
  const showList = () => {
    return dataList.value
  }

  async function initList() {
    return getList(pageInfo.value.currentPage, {})
  }

  async function getInfo(id) {
    return getPowerBankAPI(id)
      .then((res) => {
        res.data.areaCodeList = [
          res.data.area_data.slice(0, 2),
          res.data.area_data.slice(0, 4),
          res.data.area_data.slice(0, 6)
        ]
        res.data.status_name = powerBankConfig.getStatusDisplay(res.data.status)
        return res
      })
      .catch(handleApiError)
  }

  async function getList(page = pageInfo.value.currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getPowerBankListAPI(page, uploadConditions.value)
      .then((res) => {
        extraOperation(res.data)
        dataList.value = res.data
        pageInfo.value.total = res.extra.total
        pageInfo.value.pageSize = res.extra.pageSize
        pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        return res
      })
      .catch(handleApiError)
  }
  async function createInfo(data) {
    return createPowerBankAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    return updatePowerBankAPI(id, {}, data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deletePowerBankAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function uploadImg(fileData) {
    return uploadPowerBankImgAPI(fileData)
      .then((res) => res)
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.status_name = powerBankConfig.getStatusDisplay(item.status)
        let address
        if (item.area_code) {
          const addressList = addressStore.codeListToAddrList([
            item.area_code.slice(0, 2),
            item.area_code.slice(0, 4),
            item.area_code.slice(0, 6)
          ])
          address = addressList.reduce((pre, cur) => pre + cur)
        } else {
          address = null
        }
        item.areaName = address
        if (item.area_name) item.areaName += item.area_name
        if (item.merchant_address) item.areaName += item.merchant_address
        item.merchantName = item.merchant_name
      })
    }
  }

  const handleApiSuccess = (res, ifRefresh = false) => {
    $successMsg(res.message)
    if (ifRefresh) {
      getList(pageInfo.value.currentPage, uploadConditions.value)
    }
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return {
    getPageInfo,
    showList,
    initList,
    getInfo,
    getList,
    createInfo,
    updateInfo,
    deleteInfo,
    uploadImg
  }
})

export const useSPBMaintenanceStore = defineStore('SPBMaintenanceList', () => {
  const powerBankConfig = useSPBConfigStore()

  const dataList = ref([])

  const constConditions = ref({})
  const getConditions = ref()
  const uploadConditions = ref({})

  const pageInfo = ref(createPageInfo())

  const getPageInfo = () => {
    return pageInfo.value
  }
  const showList = () => {
    return dataList.value
  }

  async function initList() {
    return getList(getPageInfo().currentPage, {})
  }

  async function getInfo(id) {
    return getPowerBankMaintenanceAPI(id)
      .then((res) => {
        res.data.date = convertBackendTimestampToLocalTime(res.data.date)
        if (res.data.date) {
          res.data.date = res.data.date.replace(/\//g, '-')
        }
        return res
      })
      .catch(handleApiError)
  }

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getPowerBankMaintenanceListAPI(page, uploadConditions.value)
      .then((res) => {
        extraOperation(res.data)
        dataList.value = res.data
        pageInfo.value.total = res.extra.total
        pageInfo.value.pageSize = res.extra.pageSize
        pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        return res
      })
      .catch(handleApiError)
  }
  async function createInfo(data) {
    return createPowerBankMaintenanceAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    return updatePowerBankMaintenanceAPI(id, {}, data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deletePowerBankMaintenanceAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.status = powerBankConfig.getStatusDisplay(item.status)
        item.date = convertBackendTimestampToLocalTime(item.date)
        item.finished = item.finished ? '是' : '否'
      })
    }
    return data
  }

  const handleApiSuccess = (res, ifRefresh = false) => {
    $successMsg(res.message)
    if (ifRefresh) {
      getList(pageInfo.value.currentPage, uploadConditions.value)
    }
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return {
    getPageInfo,
    showList,
    initList,
    getInfo,
    getList,
    createInfo,
    updateInfo,
    deleteInfo
  }
})
