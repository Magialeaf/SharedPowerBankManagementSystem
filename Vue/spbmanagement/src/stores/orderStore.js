import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $successMsg, $errorMsg } from '@/utils/msg'
import {
  getOrderRentalAPI,
  getOrderRentalListAPI,
  createOrderRentalAPI,
  updateOrderRentalAPI,
  deleteOrderRentalAPI,
  getOrderReturnAPI,
  getOrderReturnListAPI,
  createOrderReturnAPI,
  updateOrderReturnAPI,
  deleteOrderReturnAPI,
  getOrderFeeAPI,
  getOrderFeeListAPI,
  createOrderFeeAPI,
  updateOrderFeeAPI,
  deleteOrderFeeAPI,
  getOrderListAPI,
  rentalPowerBankAPI,
  returnPowerBankAPI,
  payFeeAPI
} from '@/api/orderAPI.js'
import { convertBackendTimestampToLocalTime } from '@/utils/convert.js'

/* 租赁订单 */
export const useOrderRentalStore = defineStore('orderRentalList', () => {
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
    return getOrderRentalAPI(id)
      .then((res) => {
        res.data.rental_date = convertBackendTimestampToLocalTime(res.data.rental_date)
        return res
      })
      .catch(handleApiError)
  }

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getOrderRentalListAPI(page, uploadConditions.value)
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
    return createOrderRentalAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    if (data.rental_date) {
      data.rental_date = data.rental_date.replace(/\//g, '-')
    }
    return updateOrderRentalAPI(id, {}, data)
      .then((res) => {
        res.data.rental_date = convertBackendTimestampToLocalTime(res.data.rental_date)
        return handleApiSuccess(res, true)
      })
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deleteOrderRentalAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.returned = item.returned ? '是' : '否'
        item.rental_date = convertBackendTimestampToLocalTime(item.rental_date)
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

/* 归还订单 */
export const useOrderReturnStore = defineStore('orderReturnList', () => {
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
    return getOrderReturnAPI(id)
      .then((res) => {
        res.data.return_date = convertBackendTimestampToLocalTime(res.data.return_date)
        return res
      })
      .catch(handleApiError)
  }

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getOrderReturnListAPI(page, uploadConditions.value)
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
    return createOrderReturnAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    if (data.return_date) {
      data.return_date = data.return_date.replace(/\//g, '-')
    }
    return updateOrderReturnAPI(id, {}, data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deleteOrderReturnAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.return_date = convertBackendTimestampToLocalTime(item.return_date)
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

/* 费用订单 */
export const useOrderFeeStore = defineStore('orderFeeList', () => {
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
    return getOrderFeeAPI(id)
      .then((res) => res)
      .catch(handleApiError)
  }

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getOrderFeeListAPI(page, uploadConditions.value)
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
    return createOrderFeeAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    return updateOrderFeeAPI(id, {}, data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deleteOrderFeeAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.paid = item.paid ? '是' : '否'
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

/* 用户对订单操作 */
export const useOrderUserStore = defineStore('orderUserList', () => {
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

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    getConditions.value = conditions
    pageInfo.value.currentPage = page
    return getOrderListAPI(page, uploadConditions.value)
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
    return rentalPowerBankAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data, type) {
    if (type === 'return') {
      return returnPowerBankAPI(id, {}, data)
        .then((res) => handleApiSuccess(res, true))
        .catch(handleApiError)
    } else if (type === 'fee') {
      return payFeeAPI(id, {}, data)
        .then((res) => handleApiSuccess(res, true))
        .catch(handleApiError)
    } else {
      throw new Error('类型错误')
    }
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.rental_date = convertBackendTimestampToLocalTime(item.rental_date)
        item.return_date = convertBackendTimestampToLocalTime(item.return_date)
        item.pay_date = convertBackendTimestampToLocalTime(item.pay_date)
        if (item.returned === false && !item.paid) {
          item.now_type = 'return'
        } else if (item.returned === true && item.paid === false) {
          item.now_type = 'fee'
        } else {
          item.now_type = 'null'
        }
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
    getList,
    createInfo,
    updateInfo
  }
})
