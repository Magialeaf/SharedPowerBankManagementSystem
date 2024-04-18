import { getByPkAPI, createByPkAPI, updateByPkAPI, deleteByPkAPI } from './APIBase.js'
import { areaURL } from '@/api/path.js'

// 查询当前区域信息
export const getAreaAPI = (id) => getByPkAPI(areaURL, id)

// 查询当前经纬度对应的区域信息
export const getAreaByLatAndLonAPI = (latitude, longitude) =>
  getByPkAPI(areaURL, 0, { latitude: latitude, longitude: longitude }, [], 'getByLL')

// 获得当前页面区域信息
export const getAreaListAPI = (page, conditions) =>
  getByPkAPI(areaURL, page, conditions, [], 'getList')

// 新增区域
export const createAreaAPI = (data = {}) => createByPkAPI(areaURL, 0, data)

// 修改区域
export const updateAreaAPI = (id, data = {}) => updateByPkAPI(areaURL, id, {}, data)

// 删除区域
export const deleteAreaAPI = (id) => deleteByPkAPI(areaURL, id)
