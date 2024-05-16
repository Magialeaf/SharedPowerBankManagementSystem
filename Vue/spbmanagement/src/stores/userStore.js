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
import { useAddressStore } from '@/stores/areaStore.js'
import { createPageInfo } from '@/stores/pageInfo.js'
import { useIdentityStore } from './authenticationStore'
import { convertBackendTimestampToLocalTime } from '@/utils/convert'

export const useUserStore = defineStore('userList', () => {
  const defaultAvatarURL = ref('http://39.101.75.20/media/images/user_avatars/default.png')
  const userList = ref()
  const constConditions = ref({
    table: 'user',
    identity: -1
  })
  const inputConditions = ref({})
  const getConditions = ref()

  const pageInfo = ref(createPageInfo())

  const addressStore = useAddressStore()
  const identityStore = useIdentityStore()

  const getList = () => {
    return userList.value
  }
  const getPageInfo = () => {
    return pageInfo.value
  }

  // 初始化数据
  const initUserList = (identity) => {
    constConditions.value.identity = identity
    return getUserList(pageInfo.value.currentPage, {})
  }

  // 获得个人信息
  function getMyInfo() {
    return getMyInfoAPI()
      .then((res) => {
        res.data[0].identity = res.data[0].identity.toString()
        if (res.data[0].identity === '0') {
          res.data[0].identity = '超级管理员'
        }
        res.data[0].create_time = convertBackendTimestampToLocalTime(res.data[0].create_time)
        res.data[0].last_login_time = convertBackendTimestampToLocalTime(
          res.data[0].last_login_time
        )
        return res
      })
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
      .then((res) => {
        res.data[0].identity = res.data[0].identity.toString()
        if (res.data[0].identity === '0') {
          res.data[0].identity = '超级管理员'
        }
        res.data[0].create_time = convertBackendTimestampToLocalTime(res.data[0].create_time)
        res.data[0].last_login_time = convertBackendTimestampToLocalTime(
          res.data[0].last_login_time
        )
        return res
      })
      .catch((error) => {
        throw error
      })
  }

  // 创建单个用户和账户信息
  function createOneInfo(data = {}) {
    data.identity = identityStore.getIdentityCode(data.identity)
    return createOneInfoAPI(data)
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
  function getUserList(page = pageInfo.value.currentPage, conditions = inputConditions.value) {
    pageInfo.value.currentPage = page
    inputConditions.value = conditions
    getConditions.value = { ...inputConditions.value, ...constConditions.value }
    return getUserListAPI(page, getConditions.value)
      .then((res) => {
        userList.value = res.data
        pageInfo.value.total = res.extra.total
        pageInfo.value.pageSize = res.extra.pageSize
        pageInfo.value.pageCount = Math.ceil(pageInfo.value.total / pageInfo.value.pageSize)
        if (constConditions.value.identity === identityStore.Maintainer) {
          maintainOptions()
        }
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

  function maintainOptions() {
    userList.value.forEach((user) => {
      user.maintain_areas = ''
      for (let i = 0; i < user.areas.length; i++) {
        if (user.areas[i].slice(0, 6) === '000000') continue
        const codeList = [
          user.areas[i].slice(0, 2),
          user.areas[i].slice(0, 4),
          user.areas[i].slice(0, 6)
        ]
        const name = user.areas[i].slice(7)
        const addressList = addressStore.codeListToAddrList(codeList)
        const area = addressList.reduce((pre, cur) => pre + cur) + name
        user.maintain_areas += area + '，'
      }
      user.maintain_areas = user.maintain_areas.slice(0, -1)
    })
  }

  const handleApiSuccess = (res, ifRefresh = false) => {
    $successMsg(res.message)
    if (ifRefresh) {
      getUserList(pageInfo.value.currentPage, inputConditions.value)
    }
    return res
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return {
    defaultAvatarURL,
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
