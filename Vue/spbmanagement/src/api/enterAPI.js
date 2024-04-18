import { enterURL, captchaURL } from '@/api/path.js'
import { getByPkAPI, createAPI, updateAPI } from '@/api/APIBase.js'

// 获得验证码
export const getCaptchaByEmailAPI = (email) => getByPkAPI(captchaURL, email, {}, [], 'getCaptcha')

// 获得验证码缓存
export const getCaptchaCacheByEmailAPI = (email) =>
  getByPkAPI(captchaURL, email, {}, [], 'getCaptchaCache')

// 注册
export const registerAPI = (data = {}) => createAPI(enterURL, data, 'register')

// 登录
export const loginAPI = (conditions = {}, data = {}) =>
  updateAPI(enterURL, conditions, data, 'login')
