import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getMerchantAPI,
  getMerchantListAPI,
  getMerchantIdNameAPI,
  createMerchantAPI,
  updateMerchantAPI,
  deleteMerchantAPI,
  uploadMerchantImgAPI
} from '@/api/merchantAPI'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $successMsg, $errorMsg } from '@/utils/msg'
import { useAddressStore } from '@/stores/areaStore.js'

export const useMerchantStore = defineStore('merchantList', () => {
  const addressStore = useAddressStore()

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

  // 通过ID获得商户
  const getMerchant = (id) => {
    return getMerchantAPI(id)
      .then((res) => {
        res.data.areaCodeList = [
          res.data.area_data.slice(0, 2),
          res.data.area_data.slice(0, 4),
          res.data.area_data.slice(0, 6)
        ]
        return res
      })
      .catch((error) => {
        throw error
      })
  }

  // 通过areaId获得商户
  const getMerchantByAreaId = async (areaId) => {
    return getMerchantIdNameAPI(areaId)
      .then((res) => res)
      .catch(handleApiError)
  }

  // 获得商户列表
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

  // 创建商户
  const createMerchant = (data = {}, ifRefresh = false) => {
    return createMerchantAPI(data)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 修改商户
  const updateMerchant = (id, data = {}, ifRefresh = true) => {
    if (data.area_data) delete data.area_data
    if (data.areaCodeList) delete data.areaCodeList

    return updateMerchantAPI(id, data)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 删除商户
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

  const extraOperateList = () => {
    merchantList.value.forEach((item) => {
      const addrList = addressStore.codeListToAddrList([
        item.area_data.slice(0, 2),
        item.area_data.slice(0, 4),
        item.area_data.slice(0, 6)
      ])

      item.areaName = addrList.reduce((pre, cur) => pre + cur) + item.area_data.slice(7)
    })
  }

  return {
    getList,
    getPageInfo,
    initMerchantList,
    getMerchant,
    getMerchantList,
    getMerchantByAreaId,
    createMerchant,
    updateMerchant,
    deleteMerchant,
    uploadImg
  }
})
