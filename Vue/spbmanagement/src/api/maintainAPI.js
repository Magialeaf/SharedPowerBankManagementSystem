import { getByPkAPI, updateByPkAPI } from '@/api/APIBase'
import { maintainURL } from '@/api/path'

export const getMaintainAPI = (id) => getByPkAPI(maintainURL, id, {}, [])

export const updateMaintainAPI = (id, conditions, data) =>
  updateByPkAPI(maintainURL, id, conditions, data)
