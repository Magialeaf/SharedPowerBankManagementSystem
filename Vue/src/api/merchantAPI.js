import {
  getByPkAPI,
  createByPkAPI,
  updateByPkAPI,
  deleteByPkAPI,
  uploadImageAPI
} from './APIBase.js'
import { merchantURL, merchantImgURL } from '@/api/path.js'

// 查询当前商户信息
export const getMerchantAPI = (id) => getByPkAPI(merchantURL, id)

// 获得当前页面商户信息
export const getMerchantListAPI = (page, conditions) =>
  getByPkAPI(merchantURL, page, conditions, [], 'getList')

// 新增商户
export const createMerchantAPI = (data = {}) => createByPkAPI(merchantURL, 0, data)

// 修改商户
export const updateMerchantAPI = (id, data = {}) => updateByPkAPI(merchantURL, id, {}, data)

// 删除商户
export const deleteMerchantAPI = (id) => deleteByPkAPI(merchantURL, id)

// 上传商户图片
export const uploadMerchantImgAPI = (fileData) => uploadImageAPI(merchantImgURL, fileData)
