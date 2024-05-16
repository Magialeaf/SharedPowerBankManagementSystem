import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $successMsg, $errorMsg } from '@/utils/msg'
import {
  getNoticeAPI,
  getNoticeListAPI,
  createNoticeAPI,
  updateNoticeAPI,
  deleteNoticeAPI,
  uploadNoticeImgAPI
} from '@/api/noticeAPI.js'
import { convertBackendTimestampToLocalTime } from '@/utils/convert.js'

export const useNoticeConfigStore = defineStore('noticeConfig', () => {
  const noticeTypeList = ref({
    0: '管理员公告',
    1: '维护人员公告',
    2: '全体公告'
  })

  function showList() {
    return noticeTypeList.value
  }

  function getType(id) {
    return noticeTypeList.value[id]
  }

  return { showList, getType }
})

// 通知消息
export const useNoticeStore = defineStore('noticeList', () => {
  const defaultImg = ref('http://39.101.75.20/media/images/notice_img/default.png')
  const noticeConfigStore = useNoticeConfigStore()

  const dataList = ref([])

  const constConditions = ref({})
  const getConditions = ref()
  const uploadConditions = ref({})

  const pageInfo = ref(createPageInfo())

  const getDefaultImg = () => {
    return defaultImg.value
  }

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
    return getNoticeAPI(id)
      .then((res) => {
        res.data.type_name = noticeConfigStore.getType(res.data.type)
        res.data.create_time = convertBackendTimestampToLocalTime(res.data.create_time)
        res.data.update_time = convertBackendTimestampToLocalTime(res.data.update_time)
        return res
      })
      .catch(handleApiError)
  }

  async function getList(page = getPageInfo().currentPage, conditions = getConditions.value) {
    uploadConditions.value = { ...conditions, ...constConditions.value }
    pageInfo.value.currentPage = page
    return getNoticeListAPI(page, uploadConditions.value)
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
    return createNoticeAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function updateInfo(id, data) {
    return updateNoticeAPI(id, {}, data)
      .then((res) => {
        handleApiSuccess(res, true)
        res.data.type = res.data.type.toString()
        res.data.create_time = convertBackendTimestampToLocalTime(res.data.create_time)
        res.data.update_time = convertBackendTimestampToLocalTime(res.data.update_time)
        return res
      })
      .catch(handleApiError)
  }

  async function deleteInfo(id) {
    return deleteNoticeAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  async function uploadImg(fileData) {
    return uploadNoticeImgAPI(fileData)
      .then((res) => res)
      .catch(handleApiError)
  }

  function extraOperation(data) {
    if (data && data.length) {
      data.forEach((item) => {
        item.type_name = noticeConfigStore.getType(item.type)
        item.create_time = convertBackendTimestampToLocalTime(item.create_time)
        item.update_time = convertBackendTimestampToLocalTime(item.update_time)
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
    getDefaultImg,
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
