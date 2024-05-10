import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $successMsg, $errorMsg } from '@/utils/msg'
import {
  getByPkAPI,
  createByPkAPI,
  updateByPkAPI,
  deleteByPkAPI,
  uploadImageAPI
} from '@/api/APIBase'

// CRUD模板
export const useTemplateStore = defineStore('TemplateList', () => {
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
    return getByPkAPI(id)
      .then((res) => res)
      .catch(handleApiError)
  }

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getByPkAPI(page, uploadConditions.value)
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
    return createByPkAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    return updateByPkAPI(id, {}, data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deleteByPkAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function uploadImg(fileData) {
    return uploadImageAPI(fileData)
      .then((res) => res)
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {})
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
    deleteInfo,
    uploadImg
  }
})
