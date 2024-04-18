import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getAreaAPI,
  getAreaByLatAndLonAPI,
  createAreaAPI,
  updateAreaAPI,
  deleteAreaAPI,
  getAreaListAPI
} from '@/api/areaAPI'
import { createPageInfo } from '@/stores/pageInfo.js'
import { $errorMsg, $successMsg } from '@/utils/msg.js'
import { regionData } from 'element-china-area-data'
import { lockFunction } from '@/utils/myLock.js'
import { jsonp } from 'vue-jsonp'

export const useAreaStore = defineStore('areaList', () => {
  const addressStore = useAddressStore()

  const areaList = ref()
  const getConditions = ref()
  const LatAndLonLen = ref(2)
  const center = ref({ lat: 28.717904, lng: 115.826242 })

  const pageInfo = ref(createPageInfo())

  const getList = () => {
    return areaList.value
  }
  const getPageInfo = () => {
    return pageInfo.value
  }
  const getLatAndLonLen = () => {
    return LatAndLonLen.value
  }
  const getCenter = () => {
    return center.value
  }

  // 初始化数据
  const initAreaList = () => {
    return getAreaList(pageInfo.value.currentPage)
  }

  // 通过ID获得区域
  const getArea = (id) => {
    return getAreaAPI(id)
      .then((res) => res)
      .catch((error) => {
        throw error
      })
  }

  // 通过经纬度获得区域
  const getAreaByLatAndLon = (latitude, longitude) => {
    return getAreaByLatAndLonAPI(latitude, longitude)
      .then((res) => res)
      .catch((error) => {
        throw error
      })
  }

  // 获得区域列表
  const getAreaList = (page, conditions = {}) => {
    pageInfo.value.currentPage = page
    getConditions.value = conditions
    return getAreaListAPI(page, conditions)
      .then((res) => {
        areaList.value = res.data
        extraOperateList()
        pageInfo.value.total = res.extra.total
        pageInfo.value.pageSize = res.extra.pageSize
        pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        return res
      })
      .catch(handleApiError)
  }

  // 创建区域
  const createArea = (data = {}, ifRefresh = true) => {
    return createAreaAPI(data)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 修改区域
  const updateArea = (id, data = {}, ifRefresh = true) => {
    return updateAreaAPI(id, data)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  // 删除区域
  const deleteArea = (id, ifRefresh = true) => {
    return deleteAreaAPI(id)
      .then((res) => handleApiSuccess(res, ifRefresh))
      .catch(handleApiError)
  }

  const handleApiSuccess = (res, ifRefresh) => {
    $successMsg(res.message)
    if (ifRefresh) {
      getAreaList(pageInfo.value.currentPage, getConditions.value)
    }
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  const extraOperateList = () => {
    for (let i = 0; i < areaList.value.length; i++) {
      const codeList = [
        areaList.value[i].code.slice(0, 2),
        areaList.value[i].code.slice(0, 4),
        areaList.value[i].code
      ]
      const addrList = addressStore.codeListToAddrList(codeList)
      areaList.value[i].codeName = addrList.reduce((pre, cur) => pre + cur)
    }
  }

  return {
    getList,
    getPageInfo,
    initAreaList,
    getArea,
    getAreaByLatAndLon,
    getAreaList,
    createArea,
    updateArea,
    deleteArea,
    getLatAndLonLen,
    getCenter
  }
})

export const useAddressStore = defineStore('address', () => {
  const addrToCodeList = ref({})
  const codeToArrList = ref({})

  // 地址解析
  const geocode = async (address) => {
    // 确保返回一个Promise
    return jsonp('https://apis.map.qq.com/ws/geocoder/v1/', {
      key: '6V3BZ-BZL6F-SAAJ6-JUS4K-ZCBNZ-6ZFGH',
      output: 'jsonp',
      address: address
    })
      .then((res) => {
        if (res.status === 0) {
          return res
        } else {
          // 如果状态不为0，抛出错误以便外部通过catch处理
          throw new Error('错误: ' + res.message)
        }
      })
      .catch((e) => {
        $errorMsg(e.message)
      })
  }

  // 逆地址解析
  const reverseGeocode = async (lat, lng) => {
    // 确保返回一个Promise
    return jsonp('https://apis.map.qq.com/ws/geocoder/v1/', {
      key: '6V3BZ-BZL6F-SAAJ6-JUS4K-ZCBNZ-6ZFGH',
      output: 'jsonp',
      location: lat + ',' + lng
    })
      .then((res) => {
        if (res.status === 0) {
          return res
        } else {
          // 如果状态不为0，抛出错误以便外部通过catch处理
          throw new Error('错误: ' + res.message)
        }
      })
      .catch((e) => {
        $errorMsg(e.message)
        throw e // 将错误向上抛出，使外部能感知到
      })
  }

  // 地址转代码
  function addrListToCodeList(address) {
    let code = ['00', '0000', '000000']
    let provinceIdx = 0
    let cityIdx = 0
    for (let i = 0; i < regionData.length; i++) {
      if (address[0] === regionData[i].label) {
        provinceIdx = i
        code[0] = regionData[i].value
      }
    }
    for (let i = 0; i < regionData[provinceIdx].children.length; i++) {
      if (address[1] === regionData[provinceIdx].children[i].label) {
        cityIdx = i
        code[1] = regionData[provinceIdx].children[i].value
      }
    }
    for (let i = 0; i < regionData[provinceIdx].children[cityIdx].children.length; i++) {
      if (address[2] === regionData[provinceIdx].children[cityIdx].children[i].label) {
        code.push[2] = regionData[provinceIdx].children[cityIdx].children[i].value
      }
    }
    return code
  }

  // 代码转地址
  function codeListToAddrList(codeList) {
    let address = ['', '', '']
    let provinceIdx = 0
    let cityIdx = 0
    for (let i = 0; i < regionData.length; i++) {
      if (codeList[0] === regionData[i].value) {
        provinceIdx = i
        address[0] = regionData[i].label
      }
    }
    for (let i = 0; i < regionData[provinceIdx].children.length; i++) {
      if (codeList[1] === regionData[provinceIdx].children[i].value) {
        cityIdx = i
        address[1] = regionData[provinceIdx].children[i].label
      }
    }
    for (let i = 0; i < regionData[provinceIdx].children[cityIdx].children.length; i++) {
      if (codeList[2] === regionData[provinceIdx].children[cityIdx].children[i].value) {
        address[2] = regionData[provinceIdx].children[cityIdx].children[i].label
      }
    }
    return address
  }

  return {
    addrListToCodeList,
    codeListToAddrList,
    geocode,
    reverseGeocode
  }
})
