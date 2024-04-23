import { $get, $post, $upload } from '@/utils/request.js'
import router from '@/router/index.js'

const HttpMethod = Object.freeze({
  GET: 'get',
  POST: 'post'
})

// 创建一个处理账户服务的基类或工厂函数
class APIBaseService {
  constructor(url, action, method = HttpMethod.GET) {
    this.url = url
    this.action = action
    this.method = method
  }

  async execute(conditions = {}, data = {}) {
    let response
    if (this.method === HttpMethod.GET) {
      // 根据action判断是GET还是POST请求
      response = await $get(this.url, {
        action: this.action,
        conditions
      })
    } else if (this.method === HttpMethod.POST) {
      response = await $post(this.url, {
        action: this.action,
        conditions: conditions,
        data: data
      })
    } else {
      throw new Error('请求方法不支持')
    }

    if (response && response.code) {
      if (response.code === 20000) {
        return response
      } else if (response.code === 40000) {
        const errorMessage = response.message ? response.message : '服务器返回错误'
        throw new Error(errorMessage)
      } else if (response.code === 40003) {
        throw new Error('权限不足！')
      } else if (response.code === 40004) {
        router.push('/404')
        throw new Error('页面不存在')
      } else {
        throw new Error(response.error)
      }
    }
  }

  async executeWithParams(conditions = {}, data = {}) {
    return this.execute(conditions, data)
  }
}

// 上传基类
class UploadBaseService {
  constructor(url, type = 'image', method = HttpMethod.POST) {
    this.url = url
    this.type = type
    this.method = method
  }

  async execute(fileData = {}) {
    let response
    if (this.method === HttpMethod.POST) {
      response = await $upload(this.url, fileData)
    } else {
      throw new Error('请求方法不支持')
    }

    if (response && response.code) {
      if (response.code === 20000) {
        return response
      } else if (response.code === 40000) {
        const errorMessage = response.message ? response.message : '服务器返回错误'
        throw new Error(errorMessage)
      } else if (response.code === 40003) {
        throw new Error('权限不足！')
      } else if (response.code === 40004) {
        router.push('/404')
        throw new Error('页面不存在')
      } else {
        throw new Error(response.error)
      }
    }
  }

  async executeWithParams(fileData = {}) {
    return this.execute(fileData)
  }
}

// 多条件与获得用户数据
// condition: {'uid': uid, ... , 'cookie': 'cookie',  'method': 'and / or'  } （判断数据、判断方法）
// data: ['uid', 'name', ... ] / ['all'] （获得的数据）
export const getAPI = (url, conditions = {}, data = ['all'], action = 'get') =>
  new (class extends APIBaseService {})(url, action, HttpMethod.Get).executeWithParams(
    conditions,
    data
  )

// 创建账户
// data:  {'uid': uid, ...  } （新数据）
export const createAPI = (url, data = {}, action = 'create') =>
  new (class extends APIBaseService {})(url, action, HttpMethod.POST).executeWithParams({}, data)

// 更新账户
// condition: {'uid': uid, ... ,  'cookie': 'cookie', 'method': 'and / or'  } （判断数据、判断方法）
// data: {'uid': uid, ... } / ['all'] （新数据）
export const updateAPI = (url, conditions = {}, data = {}, action = 'update') =>
  new (class extends APIBaseService {})(url, action, HttpMethod.POST).executeWithParams(
    conditions,
    data
  )

// 删除账户
// condition: {'uid': uid, ... ,  'cookie': 'cookie', 'method': 'and / or'  } （判断数据、判断方法）
export const deleteAPI = (url, conditions = {}, action = 'delete') =>
  new (class extends APIBaseService {})(url, action, HttpMethod.POST).executeWithParams(conditions)

// 上传图片
export const uploadImageAPI = (url, fileData = {}) =>
  new (class extends UploadBaseService {})(url, 'image', HttpMethod.POST).executeWithParams(
    fileData
  )

// 获得账户（Pk是主数据）
export const getByPkAPI = (url, pk, conditions = {}, data = ['all'], action = 'get') =>
  new (class extends APIBaseService {})(url + pk + '/', action, HttpMethod.Get).executeWithParams(
    conditions,
    data
  )

// 创建账户（Pk是主数据）
export const createByPkAPI = (url, pk, data = {}, action = 'create') =>
  new (class extends APIBaseService {})(url + pk + '/', action, HttpMethod.POST).executeWithParams(
    {},
    data
  )

// 更新账户（Pk是主数据）
export const updateByPkAPI = (url, pk, conditions = {}, data = {}, action = 'update') =>
  new (class extends APIBaseService {})(url + pk + '/', action, HttpMethod.POST).executeWithParams(
    conditions,
    data
  )

// 删除账户（Pk是主数据）
export const deleteByPkAPI = (url, pk, conditions = {}, action = 'delete') =>
  new (class extends APIBaseService {})(url + pk + '/', action, HttpMethod.POST).executeWithParams(
    conditions
  )
