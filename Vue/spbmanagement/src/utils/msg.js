/*
消息显示函数：
	closeMessage：保证消息窗口只有一个
	1.$errorMsg()：失败消息函数
	2.$successMsg()：成功消息函数
*/
import { ElMessage, ElMessageBox } from 'element-plus'

let currentMessage = null

const closeMessage = () => {
  if (currentMessage) {
    currentMessage.close()
    currentMessage = null
  }
}

export const $errorMsg = (message, duration = 3000) => {
  closeMessage()

  currentMessage = ElMessage({
    showClose: true,
    message,
    duration,
    type: 'error'
  })
}

export const $successMsg = (message, duration = 3000) => {
  closeMessage()

  currentMessage = ElMessage({
    showClose: true,
    message,
    duration,
    type: 'success'
  })
}

export const $confirmDeleteMsg = (message) => {
  return ElMessageBox.confirm(message, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
}
