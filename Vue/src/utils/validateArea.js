// 限定区域名长度
export const areaLen = 30

// 限定区域简介长度
export const areaDescLen = 100

// const minLongitude = -180
// const maxLongitude = 180
// const minLatitude = -90
// const maxLatitude = 90
const minLongitude = 72
const maxLongitude = 136
const minLatitude = 2
const maxLatitude = 54

// 验证纬度
export function validate_longitude(longitude, len) {
  let num = parseFloat(longitude)
  if (!isNaN(num)) {
    if (num > maxLongitude) {
      num = maxLongitude
    } else if (num < minLongitude) {
      num = minLongitude
    }
    num = num.toFixed(len)
  } else {
    num = 0
  }
  return num
}

// 验证经度
export function validate_latitude(latitude, len) {
  let num = parseFloat(latitude)
  if (!isNaN(num)) {
    if (num > maxLatitude) {
      num = maxLatitude
    } else if (num < minLatitude) {
      num = minLatitude
    }
    num = num.toFixed(len)
  } else {
    num = 0
  }
  return num
}
