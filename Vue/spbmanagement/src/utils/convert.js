// 性别名称转换为性别代码
export function convertSexNameToCode(sexName) {
  if (sexName === '男') return 0
  else if (sexName === '女') return 1
  else if (sexName === '保密') return 2
}

// 将后端返回的时间戳转换为本地时间
export function convertBackendTimestampToLocalTime(isoTimestampWithTimeZone) {
  if (!isoTimestampWithTimeZone) return null

  const date = new Date(isoTimestampWithTimeZone)
  const formatter = new Intl.DateTimeFormat(undefined, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
    // fractionalSecondDigits: 3, // 添加这一行以包含毫秒
  })

  return formatter.format(date)
}
