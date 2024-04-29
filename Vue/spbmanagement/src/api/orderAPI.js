import { getByPkAPI, createByPkAPI, updateByPkAPI, deleteByPkAPI } from '@/api/APIBase'
import { powerBankFeeURL, powerBankRentalURL, powerBankReturnURL } from '@/api/path'

/* 租赁的CRUD */
export const getOrderRentalAPI = (id) => getByPkAPI(powerBankRentalURL, id)

export const getOrderRentalListAPI = (page, conditions) =>
  getByPkAPI(powerBankRentalURL, page, conditions, [], 'getList')

export const createOrderRentalAPI = (data = {}) => createByPkAPI(powerBankRentalURL, 0, data)

export const updateOrderRentalAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(powerBankRentalURL, id, conditions, data)

export const deleteOrderRentalAPI = (id) => deleteByPkAPI(powerBankRentalURL, id)

/* 归还的CRUD */
export const getOrderReturnAPI = (id) => getByPkAPI(powerBankReturnURL, id)

export const getOrderReturnListAPI = (page, conditions) =>
  getByPkAPI(powerBankReturnURL, page, conditions, [], 'getList')

export const createOrderReturnAPI = (data = {}) => createByPkAPI(powerBankReturnURL, 0, data)

export const updateOrderReturnAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(powerBankReturnURL, id, conditions, data)

export const deleteOrderReturnAPI = (id) => deleteByPkAPI(powerBankReturnURL, id)

/* 缴费的CRUD */
export const getOrderFeeAPI = (id) => getByPkAPI(powerBankFeeURL, id)

export const getOrderFeeListAPI = (page, conditions) =>
  getByPkAPI(powerBankFeeURL, page, conditions, [], 'getList')

export const createOrderFeeAPI = (data = {}) => createByPkAPI(powerBankFeeURL, 0, data)

export const updateOrderFeeAPI = (id, conditions = {}, data = {}) =>
  updateByPkAPI(powerBankFeeURL, id, conditions, data)

export const deleteOrderFeeAPI = (id) => deleteByPkAPI(powerBankFeeURL, id)
