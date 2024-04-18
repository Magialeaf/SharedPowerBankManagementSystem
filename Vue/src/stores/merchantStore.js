import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getMerchantAPI,
  getMerchantListAPI,
  createMerchantAPI,
  updateMerchantAPI,
  deleteMerchantAPI,
  uploadMerchantImgAPI
} from '@/api/merchantAPI'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $successMsg, $errorMsg } from '@/utils/msg'

export const useMerchantStore = defineStore('merchantList', () => {
  const merchantList = ref()

  const getConditions = ref({})

  const pageInfo = ref(createPageInfo())

  const getList = () => {
    return merchantList.value
  }

  const getPageInfo = () => {
    return pageInfo.value
  }

  // 初始化数据
  const initMerchantList = () => {
    return getMerchantList(pageInfo.value.currentPage)
  }

  // 通过ID获得区域
  const getMerchant = (id) => {
    return getMerchantAPI(id)
      .then((res) => res)
      .catch((error) => {
        throw error
      })
  }

  // 获得区域列表
  const getMerchantList = (page, conditions = {}) => {
    pageInfo.value.currentPage = page
    getConditions.value = conditions
    return getMerchantListAPI(page, conditions)
      .then((res) => {
        merchantList.value = res.data
        extraOperateList()
        pageInfo.value.total = res.extra.total
        pageInfo.value.pageSize = res.extra.pageSize
        pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        return res
      })
      .catch(handleApiError)
  }

  // 创建区域
  const createMerchant = (data = {}, ifRefresh = true) => {
    return createMerchantAPI(data)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 修改区域
  const updateMerchant = (id, data = {}, ifRefresh = true) => {
    return updateMerchantAPI(id, data)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 删除区域
  const deleteMerchant = (id, ifRefresh = true) => {
    return deleteMerchantAPI(id)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 上传商店照片
  function uploadImg(fileData) {
    return uploadMerchantImgAPI(fileData)
      .then((res) => res)
      .catch(handleApiError)
  }

  const handleApiSuccess = (res, ifRefresh) => {
    $successMsg(res.message)
    if (ifRefresh) {
      return getMerchantList(pageInfo.value.currentPage, getConditions.value)
    } else {
      return res
    }
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  const extraOperateList = () => {}

  return {
    getList,
    getPageInfo,
    initMerchantList,
    getMerchant,
    getMerchantList,
    createMerchant,
    updateMerchant,
    deleteMerchant,
    uploadImg
  }
})
