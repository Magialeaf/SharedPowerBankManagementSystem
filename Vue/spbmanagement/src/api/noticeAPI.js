import { noticeURL, noticeImgURL } from '@/api/path'
import {
  getByPkAPI,
  createByPkAPI,
  updateByPkAPI,
  deleteByPkAPI,
  uploadImageAPI
} from '@/api/APIBase'

export const getNoticeAPI = (id) => getByPkAPI(noticeURL, id)

export const getNoticeListAPI = (page, conditions) =>
  getByPkAPI(noticeURL, page, conditions, [], 'getList')

export const createNoticeAPI = (data = {}) => createByPkAPI(noticeURL, 0, data)

export const updateNoticeAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(noticeURL, id, conditions, data)

export const deleteNoticeAPI = (id) => deleteByPkAPI(noticeURL, id)

export const uploadNoticeImgAPI = (fileData) => uploadImageAPI(noticeImgURL, fileData)
