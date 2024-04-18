import { defineStore } from 'pinia'
import { loginAPI, registerAPI } from '@/api/enterAPI'
import {
  validate_account,
  validate_captcha,
  validate_email,
  validate_password,
  validate_confirmPassword
} from '@/utils/validateUser'
import { $errorMsg } from '@/utils/msg'
import { RSAEncode } from '@/utils/myCrypto'

export const useEnterStore = defineStore('enter', () => {
  const register = (data) => {
    if (!validate_account(data.account || '')) return Promise.reject()
    if (!validate_password(data.password || '')) return Promise.reject()
    if (!validate_confirmPassword(data.password || '', data.confirmPassword || ''))
      return Promise.reject()
    if (!validate_email(data.email || '')) return Promise.reject()
    if (!validate_captcha(data.captcha || '')) return Promise.reject()

    const encryptedData = { ...data }
    encryptedData.password = RSAEncode(data.password)
    return registerAPI(encryptedData)
      .then((res) => res)
      .catch((e) => handleApiError(e))
  }

  const accountLogin = (data) => {
    if (!validate_account(data.account || '')) return Promise.reject()
    if (!validate_password(data.password || '')) return Promise.reject()

    const encryptedData = { ...data }
    encryptedData.password = RSAEncode(data.password)
    return loginAPI({ login: 'account' }, encryptedData)
      .then((res) => res)
      .catch((e) => handleApiError(e))
  }

  const emailLogin = (data) => {
    if (!validate_email(data.email || '')) return Promise.reject()
    if (!validate_captcha(data.captcha || '')) return Promise.reject()

    return loginAPI({ login: 'email' }, data)
      .then((res) => res)
      .catch((e) => handleApiError(e))
  }

  const handleApiError = (error) => {
    $errorMsg(error.message)
    throw error
  }

  return {
    register,
    accountLogin,
    emailLogin
  }
})
