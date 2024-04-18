import { $errorMsg } from '@/utils/msg.js'

// 验证账号
export function validate_account(accountValue) {
  if (!accountValue.match(/^[a-zA-Z]\w{2,14}$/)) {
    $errorMsg('账号必须以字母开头且是3-15位')
    return false
  }
  return true
}

// 验证密码
export function validate_password(passwordValue) {
  if (!passwordValue.match(/^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{6,18}$/)) {
    $errorMsg('密码必须是6-18位且包含字母和数字')
    return false
  }
  return true
}

// 验证确认密码
export function validate_confirmPassword(passwordValue, confirmPasswordValue) {
  if (confirmPasswordValue !== passwordValue) {
    $errorMsg('两次密码不一样')
    return false
  }
  return true
}

// 验证邮箱
export function validate_email(emailValue) {
  if (!emailValue.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/)) {
    $errorMsg('邮箱格式错误')
    return false
  }
  return true
}

// 验证验证码
export function validate_captcha(captchaValue) {
  if (!captchaValue.match(/^\d{6}$/)) {
    $errorMsg('验证码是六位数字')
    return false
  }
  return true
}
