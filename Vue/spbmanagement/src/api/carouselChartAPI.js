import { carouselChartURL, carouselChartImgURL } from '@/api/path'
import {
  getByPkAPI,
  createByPkAPI,
  updateByPkAPI,
  deleteByPkAPI,
  uploadImageAPI
} from '@/api/APIBase'

// 获得单个轮播图信息
export const getCarouselChartAPI = (id) => getByPkAPI(carouselChartURL, id)

// 获得轮播图列表（用户）
export const showCarouselChartAPI = (number) =>
  getByPkAPI(carouselChartURL, number, {}, [], 'showList')

// 获得轮播图列表（管理员）
export const getCarouselChartListAPI = (page, conditions) =>
  getByPkAPI(carouselChartURL, page, conditions, [], 'getList')

// 新建轮播图
export const createCarouselChartAPI = (data = {}) => createByPkAPI(carouselChartURL, 0, data)

// 上传轮播图
export const uploadCarouselChartImgAPI = (fileData) => uploadImageAPI(carouselChartImgURL, fileData)

// 更新轮播图
export const updateCarouselChartAPI = (id, data = {}) =>
  updateByPkAPI(carouselChartURL, id, {}, data)

// 删除轮播图
export const deleteCarouselChartAPI = (id) => deleteByPkAPI(carouselChartURL, id)
