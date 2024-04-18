import { defineStore } from 'pinia'
import { ref } from 'vue'
import { $successMsg, $errorMsg } from '@/utils/msg'
import {
  getUserListAPI,
  getMyInfoAPI,
  updateMyInfoAPI,
  deleteMyInfoAPI,
  getOneInfoAPI,
  createOneInfoAPI,
  updateOneInfoAPI,
  deleteOneInfoAPI,
  uploadAvatarAPI,
  updateUserIdentityAPI
} from '@/api/userAPI.js'
import { createPageInfo } from '@/stores/pageInfo.js'
import { useIdentityStore } from './authenticationStore'

export const useUserStore = defineStore('userList', () => {
  const userList = ref()
  const constConditions = ref({
    table: 'user',
    identity: -1
  })
  const getConditions = ref()

  const pageInfo = ref(createPageInfo())

  const getList = () => {
    return userList.value
  }
  const getPageInfo = () => {
    return pageInfo.value
  }

  // 初始化数据
  const initUserList = (identity) => {
    constConditions.value.identity = identity
    return getUserList(pageInfo.value.currentPage)
  }

  // 获得个人信息
  function getMyInfo() {
    return getMyInfoAPI()
      .then((res) => res)
      .catch((error) => {
        throw error
      })
  }
  // 修改个人信息
  function updateMyInfo(data = {}) {
    return updateMyInfoAPI(constConditions.value, data)
      .then((res) => handleApiSuccess(res, false))
      .catch(handleApiError)
  }
  //

  // 删除个人信息
  function deleteMyInfo() {
    return deleteMyInfoAPI()
      .then((res) => handleApiSuccess(res, false))
      .catch(handleApiError)
  }

  // 获取单个用户和账户信息
  function getOneInfo(id) {
    return getOneInfoAPI(id)
      .then((res) => res)
      .catch((error) => {
        throw error
      })
  }

  // 创建单个用户和账户信息
  function createOneInfo(id, data = {}) {
    return createOneInfoAPI(id, data)
      .then((res) => handleApiSuccess(res, false))
      .catch(handleApiError)
  }

  // 更新单个用户和账户信息
  function updateOneInfo(id, data = {}) {
    return updateOneInfoAPI(id, constConditions.value, data)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  // 删除单个用户和账户信息
  function deleteOneInfo(id) {
    return deleteOneInfoAPI(id)
      .then((res) => handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  // 获取用户列表
  function getUserList(page, conditions = {}) {
    pageInfo.value.currentPage = page
    getConditions.value = { ...conditions, ...constConditions.value }
    return getUserListAPI(page, getConditions.value)
      .then((res) => {
        userList.value = res.data
        // pageInfo.value.total = res.extra.total
        // pageInfo.value.pageSize = res.extra.pageSize
        // pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        return res
      })
      .catch(handleApiError)
  }

  // 上传头像
  function uploadAvatar(fileData) {
    return uploadAvatarAPI(fileData)
      .then((res) => res)
      .catch(handleApiError)
  }

  const handleApiSuccess = (res, ifRefresh = false) => {
    $successMsg(res.message)
    if (ifRefresh) {
      getUserList(pageInfo.value.currentPage, getConditions.value)
    }
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return {
    getList,
    getPageInfo,
    initUserList,
    getUserList,
    getMyInfo,
    updateMyInfo,
    deleteMyInfo,
    getOneInfo,
    createOneInfo,
    updateOneInfo,
    deleteOneInfo,
    uploadAvatar,
    handleApiSuccess
  }
})

export const useAccountStore = defineStore('accountStore', () => {
  const userStore = useUserStore()
  const identityStore = useIdentityStore()

  const constConditions = ref({
    table: 'account'
  })
  // 修改自己的账户名
  function updateMyAccount(account) {
    const data = { account: account }
    return updateMyInfoAPI(constConditions.value, data)
      .then((res) => handleApiSuccess(res))
      .catch(handleApiError)
  }

  // 修改自己的密码
  function updateMyPassword(password) {
    const data = { password: password }
    return updateMyInfoAPI(constConditions.value, data)
      .then((res) => handleApiSuccess(res))
      .catch(handleApiError)
  }

  // 修改自己的邮箱
  function updateMyEmail(email, captcha) {
    const data = { email: email, captcha: captcha }
    return updateMyInfoAPI(constConditions.value, data)
      .then((res) => handleApiSuccess(res))
      .catch(handleApiError)
  }

  // 修改别人的账户名
  function updateAccount(id, account) {
    const data = { account: account }
    return updateOneInfoAPI(id, constConditions.value, data)
      .then((res) => userStore.handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  // 修改别人的密码
  function updatePassword(id, password) {
    const data = { password: password }
    return updateOneInfoAPI(id, constConditions.value, data)
      .then((res) => userStore.handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  // 修改别人的邮箱
  function updateEmail(id, email, captcha) {
    const data = { email: email, captcha: captcha }
    return updateOneInfoAPI(id, constConditions.value, data)
      .then((res) => userStore.handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  // 修改身份
  function updateIdentity(id, identity) {
    const code = identityStore.getIdentityCode(identity)
    const data = { identity: code }
    return updateUserIdentityAPI(id, constConditions.value, data)
      .then((res) => userStore.handleApiSuccess(res, true))
      .catch(handleApiError)
  }

  const handleApiSuccess = (res) => {
    $successMsg(res.message)
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return {
    updateMyAccount,
    updateMyPassword,
    updateMyEmail,
    updateAccount,
    updatePassword,
    updateEmail,
    updateIdentity
  }
})
