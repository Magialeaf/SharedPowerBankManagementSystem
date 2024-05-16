import { myInfoURL, userURL, userAvatarURL, oneInfoURL } from '@/api/path.js'
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

// 获得个人信息
export const getMyInfoAPI = () => getAPI(myInfoURL)

// 修改个人信息
export const updateMyInfoAPI = (conditions = {}, data = {}) =>
  updateAPI(myInfoURL, conditions, data)

// 删除个人信息
export const deleteMyInfoAPI = (conditions = {}) => deleteAPI(myInfoURL, conditions)

// 获取单个用户和账户信息
export const getOneInfoAPI = (id) => getByPkAPI(oneInfoURL, id)

// 新增单个用户和账户信息
export const createOneInfoAPI = (data = {}) => createByPkAPI(oneInfoURL, 0, data)

// 修改单个用户和账户信息
export const updateOneInfoAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(oneInfoURL, id, conditions, data)

// 删除单个用户和账户信息
export const deleteOneInfoAPI = (id) => deleteByPkAPI(oneInfoURL, id)

// 获取用户列表
export const getUserListAPI = (page, conditions) =>
  getByPkAPI(userURL, page, conditions, [], 'getList')

// 获得全部用户名字
export const getUserNameListAPI = () => getByPkAPI(userURL, 0, {}, [], 'getNameList')

// 获得维护人员名字
export const getMaintainNameListAPI = (conditions) =>
  getByPkAPI(userURL, 0, conditions, [], 'getMaintainNameList')

// 上传头像
export const uploadAvatarAPI = (fileData) => uploadImageAPI(userAvatarURL, fileData)

// 更新用户身份
export const updateUserIdentityAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(oneInfoURL, id, conditions, data)
