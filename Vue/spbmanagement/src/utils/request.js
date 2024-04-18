/*
网络请求：
	1.$get(url, params = {})：get请求
	2.$post(url, params = {})：post请求

*/

import axios from 'axios'
import qs from 'qs'
import { BASE_URL } from '@/config/conster.js'

import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

import { useJwtTokenStore } from '@/stores/authenticationStore.js'
import router from '@/router/index.js'
import { $errorMsg } from './msg'

// 超时设置
const instance = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
  withCredentials: true
})

// 常用场景：拦截器
// 发送拦截
instance.interceptors.request.use(
  (config) => {
    NProgress.start()
    const JwtTokenStore = useJwtTokenStore()
    config.headers['Authorization'] = JwtTokenStore.getJwtToken()

    // 根据 isUpload 参数区分普通 POST 请求和文件上传请求
    if (config.method === 'post') {
      if (config.isUpload) {
        config.headers['Content-Type'] = 'multipart/form-data'
      } else {
        config.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        config.headers['X-Requested-With'] = 'XMLHttpRequest'

        config.data = qs.stringify(config.data)
      }
    }

    return config
  },
  (error) => {
    NProgress.done()
    return Promise.reject(error)
  }
)

// 详细错误显示
const errorHandle = (error) => {
  const { response } = error
  const jwtTokenStore = useJwtTokenStore()

  if (response) {
    switch (response.status) {
      case 400:
        throw Error('请先登录')
      /* console.log("语义有误"); $errorMsg("语义有误"); break; */
      case 401:
        throw Error('请先登录')
      /* console.log("服务器认证失败"); $errorMsg("服务器认证失败");  break; */
      case 403:
        jwtTokenStore.clearJwtToken()
        router.push('/enter/')
        throw Error(response.data.message)
      /* console.log("服务器拒绝访问"); $errorMsg("服务器拒绝访问"); break; */
      case 404:
        throw Error('地址错误')
      /* console.log("地址错误"); $errorMsg("地址错误"); break; */
      case 429:
        throw Error(response.data.message)
      /* console.log("访问太多次了"); $errorMsg("访问太多次了"); break; */
      case 500:
        throw Error('服务器遇到意外')
      /* console.log("服务器遇到意外"); $errorMsg("服务器遇到意外"); break; */
      case 502:
        throw Error('服务器无响应')
      /* console.log("服务器无响应"); $errorMsg("服务器无响应"); break; */
      default:
        throw Error('未知错误！')
      /* console.log(response.info); $errorMsg("未知错误！"); break; */
    }
  } else {
    /* console.log(error); */
    throw Error('未知错误！')
  }
}

// 获取拦截
instance.interceptors.response.use(
  (response) => {
    NProgress.done()
    // 检查并存储 JWT Token
    const jwtTokenStore = useJwtTokenStore()
    if (response.data.data && response.data.data.jwt_token) {
      jwtTokenStore.setJwtToken(response.data.data.jwt_token)
    }
    return response.status === 200 ? Promise.resolve(response) : Promise.reject(response)
  },
  (error) => {
    NProgress.done()
    errorHandle(error)
  }
)

export let $get = async (url, params = {}) => {
  let result = await instance.get(url, { params })

  if (result !== undefined) {
    return result.data
  }

  return {}
}

export let $post = async (url, params = {}) => {
  let result = await instance.post(url, params)

  if (result !== undefined) {
    return result.data
  }

  return {}
}

// 上传文件，避免与 $post 使用参数冲突
export let $upload = async (url, fileData = {}) => {
  let result = await instance.post(url, fileData, {
    isUpload: true // 传递给拦截器，标识为文件上传请求
  })

  if (result !== undefined) {
    return result.data
  }

  return {}
}
