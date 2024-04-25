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
export const powerBankFeeURL = v1 + '/power-bank-fee/'
export const powerBankRentalURL = v1 + '/power-bank-rental/'
export const powerBankReturnURL = v1 + '/power-bank-return/'

// DRF: power_bank
export const powerBankURL = v1 + '/power-bank/'
export const powerBankImgURL = v1 + '/power-bank/img/'
export const powerBankMaintenance = v1 + '/power-bank/maintenance/'

// DRF: system_administration
export const carouselChartURL = v1 + '/system-administration/carousel-chart/'
export const carouselChartImgURL = v1 + '/system-administration/carousel-chart/img/'
export const noticeURL = v1 + '/system-administration/notice/'

// DRF：users
export const enterURL = v1 + '/enter/'
export const captchaURL = v1 + '/captcha/'
export const myInfoURL = v1 + '/my-info/'
export const oneInfoURL = v1 + '/one-info/'
export const userURL = v1 + '/user/'
export const accountURL = v1 + '/account/'
export const userAvatarURL = v1 + '/user/avatar/'
export const maintainURL = v1 + '/maintain/'

// Operation
export function switchVersion(url, targetVersion) {
  const urlArray = url.split('/')

  var newUrl = ''
  for (let i = 2; i < urlArray.length - 1; i++) newUrl = newUrl + '/' + urlArray[i]

  return targetVersion + newUrl + '/'
}
