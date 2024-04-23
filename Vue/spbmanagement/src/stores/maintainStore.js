import { defineStore } from 'pinia'
import { getMaintainAPI, updateMaintainAPI } from '@/api/maintainAPI'
import { $errorMsg, $successMsg } from '@/utils/msg'

export const useMaintainStore = defineStore('maintain', () => {
  async function getMaintain(id) {
    return getMaintainAPI(id)
      .then((res) => res)
      .catch((e) => {
        $errorMsg(e.message)
        throw e
      })
  }

  async function updateMaintain(id, conditions, data) {
    return updateMaintainAPI(id, conditions, data)
      .then((res) => {
        $successMsg(res.message)
        return res
      })
      .catch((e) => {
        $errorMsg(e.message)
        throw e
      })
  }

  return { getMaintain, updateMaintain }
})
