/*
后端的路径：
	
*/
export const v1 = '/v1'
export const v2 = '/v2'
export const v3 = '/v3'

// DRF: areas
export const areaURL = v1 + '/area/'

// DRF: merchants
export const merchantURL = v1 + '/merchant/'
export const merchantImgURL = v1 + '/merchant/img/'

// DRF: orders

// DRF: power_bank

// DRF: system_administration

// DRF：users
export const enterURL = v1 + '/enter/'
export const captchaURL = v1 + '/captcha/'
export const myInfoURL = v1 + '/myInfo/'
export const oneInfoURL = v1 + '/oneInfo/'
export const userURL = v1 + '/user/'
export const accountURL = v1 + '/account/'
export const userAvatarURL = v1 + '/user/avatar/'

// Operation
export function switchVersion(url, targetVersion) {
  const urlArray = url.split('/')

  var newUrl = ''
  for (let i = 2; i < urlArray.length - 1; i++) newUrl = newUrl + '/' + urlArray[i]

  return targetVersion + newUrl + '/'
}