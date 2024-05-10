import {
  getAPI,
  getByPkAPI,
  createByPkAPI,
  updateByPkAPI,
  deleteByPkAPI,
  uploadImageAPI
} from './APIBase.js'
import { merchantURL, merchantImgURL, hotMerchantURL } from '@/api/path.js'

// 查询当前商户信息
export const getMerchantAPI = (id) => getByPkAPI(merchantURL, id)

// 获得当前页面商户信息
export const getMerchantListAPI = (page, conditions) =>
  getByPkAPI(merchantURL, page, conditions, [], 'getList')

// 通过area id 获得id和name
export const getMerchantIdNameAPI = (id) => getByPkAPI(merchantURL, id, {}, [], 'getIdList')

// 新增商户
export const createMerchantAPI = (data = {}) => createByPkAPI(merchantURL, 0, data)

// 修改商户
export const updateMerchantAPI = (id, data = {}) => updateByPkAPI(merchantURL, id, {}, data)

// 删除商户
export const deleteMerchantAPI = (id) => deleteByPkAPI(merchantURL, id)

// 上传商户图片
export const uploadMerchantImgAPI = (fileData) => uploadImageAPI(merchantImgURL, fileData)

/* 热门商户 */
export const getHotMerchantListAPI = (conditions) =>
  getAPI(hotMerchantURL, conditions, [], 'getList')
