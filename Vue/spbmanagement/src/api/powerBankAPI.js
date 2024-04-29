import { powerBankURL, powerBankImgURL, powerBankMaintenanceURL } from '@/api/path.js'
import {
  getAPI,
  getByPkAPI,
  updateByPkAPI,
  deleteByPkAPI,
  deleteAPI,
  updateAPI,
  createByPkAPI,
  uploadImageAPI
} from '@/api/APIBase.js'

/* 充电宝投放管理 */

// 获取单个充电宝
export const getPowerBankAPI = (id) => getByPkAPI(powerBankURL, id)

// 获取充电宝列表
export const getPowerBankListAPI = (page, conditions) =>
  getByPkAPI(powerBankURL, page, conditions, [], 'getList')

// 获得全部充电宝id和name
export const getPowerBankNameListAPI = () => getByPkAPI(powerBankURL, 0, {}, [], 'getNameList')

// 新增充电宝
export const createPowerBankAPI = (data = {}) => createByPkAPI(powerBankURL, 0, data)

// 更新充电宝
export const updatePowerBankAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(powerBankURL, id, conditions, data)

// 删除充电宝
export const deletePowerBankAPI = (id) => deleteByPkAPI(powerBankURL, id)

// 上传充电宝图片
export const uploadPowerBankImgAPI = (fileData) => uploadImageAPI(powerBankImgURL, fileData)

/* 充电宝维护管理 */

// 获取单个充电宝维护记录
export const getPowerBankMaintenanceAPI = (id) => getByPkAPI(powerBankMaintenanceURL, id)

// 获取充电宝维护记录列表
export const getPowerBankMaintenanceListAPI = (page, conditions) =>
  getByPkAPI(powerBankMaintenanceURL, page, conditions, [], 'getList')

// 新增充电宝维护记录
export const createPowerBankMaintenanceAPI = (data = {}) =>
  createByPkAPI(powerBankMaintenanceURL, 0, data)

// 更新充电宝维护记录
export const updatePowerBankMaintenanceAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(powerBankMaintenanceURL, id, conditions, data)

// 删除充电宝维护记录
export const deletePowerBankMaintenanceAPI = (id) => deleteByPkAPI(powerBankMaintenanceURL, id)
