import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useIdentityStore = defineStore('Identity', () => {
  // const SuperAdmin = 0
  const Admin = 1
  const Maintainer = 10
  const User = 11
  const Anon = 100

  const identityCodeList = ref({
    超级管理员: 0,
    管理员: 1,
    运维人员: 10,
    普通用户: 11
    // 匿名用户: 100
  })

  const identityList = ref({
    0: '超级管理员',
    1: '管理员',
    10: '运维人员',
    11: '普通用户'
    // 100: '匿名用户'
  })

  const canModifyIdentityList = ref({
    1: '管理员',
    10: '运维人员',
    11: '普通用户'
  })

  function getIdentityList() {
    return identityList.value
  }

  function getCanModifyIdentityList() {
    return canModifyIdentityList.value
  }

  const getIdentity = (identityId) => {
    if (identityList.value[identityId] === undefined) return '未知身份'
    return identityList.value[identityId]
  }

  const getIdentityCode = (identityId) => {
    if (identityCodeList.value[identityId] === undefined) return '-1'
    return identityCodeList.value[identityId]
  }

  return {
    // SuperAdmin,
    Admin,
    Maintainer,
    User,
    // Anon,
    getIdentity,
    getCanModifyIdentityList,
    getIdentityCode,
    getIdentityList
  }
})

export const useJwtTokenStore = defineStore('JwtTokenStudio', () => {
  const identityStore = useIdentityStore()
  const jwtToken = ref(null)

  const getJwtToken = () => {
    return jwtToken.value
  }

  const setJwtToken = (token) => {
    jwtToken.value = token
    localStorage.setItem('jwtToken', token)
  }

  const clearJwtToken = () => {
    jwtToken.value = null
    localStorage.removeItem('jwtToken')
  }

  const jwtDataToJson = () => {
    try {
      const encodedPayload = jwtToken.value.split('.')[1]
      const decodedPayload = atob(encodedPayload)
      const payloadAsJson = JSON.parse(decodedPayload)

      return payloadAsJson
    } catch (error) {
      return null
    }
  }

  const getIdentity = () => {
    if (jwtToken.value === null) return null

    return identityStore.getIdentity(jwtDataToJson().identity)
  }

  const initJwtToken = () => {
    if (jwtToken.value === null) jwtToken.value = localStorage.getItem('jwtToken')
  }

  initJwtToken()

  return {
    getJwtToken,
    setJwtToken,
    clearJwtToken,
    getIdentity
  }
})
