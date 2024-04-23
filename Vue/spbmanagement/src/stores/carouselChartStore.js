import { defineStore } from 'pinia'
import {
  getCarouselChartAPI,
  showCarouselChartAPI,
  getCarouselChartListAPI,
  createCarouselChartAPI,
  updateCarouselChartAPI,
  deleteCarouselChartAPI,
  uploadCarouselChartImgAPI
} from '@/api/carouselChartAPI'
import { convertBackendTimestampToLocalTime } from '@/utils/convert'
import { createPageInfo } from '@/stores/pageInfo'
import { $successMsg, $errorMsg } from '@/utils/msg'
import { ref } from 'vue'

export const useCarouselChartStore = defineStore('carouselChart', () => {
  const carouselChartList = ref([])
  const getConditions = ref({})
  const currentNumber = ref(5)

  const pageInfo = ref(createPageInfo())

  function getPageInfo() {
    return pageInfo.value
  }

  function getList() {
    return carouselChartList.value
  }

  async function initCarouselChartList() {
    return getCarouselChartList(1, {})
  }

  async function getCarouselChart(id) {
    return getCarouselChartAPI(id)
      .then((res) => {
        convertTime(res.data)
        return res
      })
      .catch((err) => {
        console.log(err)
      })
  }

  async function showCarouselChart(number = currentNumber.value) {
    currentNumber.value = number
    return showCarouselChartAPI(currentNumber.value)
      .then((res) => res)
      .catch((e) => handleApiError(e))
  }

  async function getCarouselChartList(page, conditions) {
    pageInfo.value.currentPage = page
    getConditions.value = { ...conditions }
    return getCarouselChartListAPI(page, conditions)
      .then((res) => {
        carouselChartList.value = res.data
        extraOperateList()
        pageInfo.value.total = res.extra.total
        pageInfo.value.pageSize = res.extra.pageSize
        pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        return res
      })
      .catch((e) => handleApiError(e))
  }

  async function createCarouselChart(data = {}) {
    return createCarouselChartAPI(data)
      .then((res) => handleApiSuccess(res, true))
      .catch((e) => handleApiError(e))
  }

  async function updateCarouselChart(id, data = {}) {
    return updateCarouselChartAPI(id, data)
      .then((res) => {
        convertTime(res.data)
        return handleApiSuccess(res, true)
      })
      .catch((e) => handleApiError(e))
  }

  async function deleteCarouselChart(id) {
    return deleteCarouselChartAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch((e) => handleApiError(e))
  }

  // 上传头像
  async function uploadImg(fileData) {
    return uploadCarouselChartImgAPI(fileData)
      .then((res) => res)
      .catch(handleApiError)
  }

  const handleApiSuccess = (res, ifRefresh = false) => {
    $successMsg(res.message)
    if (ifRefresh) {
      getCarouselChartList(pageInfo.value.currentPage, getConditions.value)
    }
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  function extraOperateList() {
    for (let i = 0; i < carouselChartList.value.length; i++) {
      convertTime(carouselChartList.value[i])
    }
  }

  function convertTime(data) {
    data.create_time = convertBackendTimestampToLocalTime(data.create_time)
    data.update_time = convertBackendTimestampToLocalTime(data.update_time)
  }

  return {
    getList,
    getPageInfo,
    initCarouselChartList,
    getCarouselChart,
    showCarouselChart,
    getCarouselChartList,
    createCarouselChart,
    updateCarouselChart,
    deleteCarouselChart,
    uploadImg
  }
})
