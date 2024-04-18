import { $errorMsg } from '@/utils/msg.js'

// 长度
export const shopNameLen = 20
export const addressLen = 30
export const liaisonLen = 20
export const phoneLen = 11

// 验证商户名称
export function validate_shop_name(merchantNameValue) {
  if (!merchantNameValue || merchantNameValue.trim().length === 0) {
    $errorMsg('商户名称不能为空')
    return false
  }

  if (merchantNameValue.length > shopNameLen) {
    $errorMsg(`商户名称不能超过${shopNameLen}个字符`)
    return false
  }
  return true
}

// 验证详细地址
export function validate_address(addressValue) {
  if (!addressValue || addressValue.trim().length === 0) {
    $errorMsg('详细地址不能为空')
    return false
  }

  if (addressValue.length > addressLen) {
    $errorMsg(`详细地址不能超过${addressLen}个字符`)
    return false
  }
  return true
}

// 验证联系人
export function validate_liaison(liaisonValue) {
  if (!liaisonValue || liaisonValue.trim().length === 0) {
    $errorMsg('联系人不能为空')
    return false
  }

  if (liaisonValue.length > liaisonLen) {
    $errorMsg(`联系人不能超过${liaisonLen}个字符`)
    return false
  }

  return true
}

// 验证联系电话
export function validate_phone(phoneValue) {
  // 判断联系电话是否为空
  if (!phoneValue || phoneValue.trim().length === 0) {
    $errorMsg('联系电话不能为空')
    return false
  }

  // 判断联系电话是否为纯数字且长度不超过11位
  const numericRegex = /^\d{1,11}$/
  if (!numericRegex.test(phoneValue)) {
    $errorMsg(`联系电话是纯数字且不能超过${phoneLen}位`)
    return false
  }

  return true
}
