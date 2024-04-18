/*
密码相关函数：
	1.RSAEncode()：RSA加密，用于密码

*/

import JSEncrypt from 'jsencrypt'

// 公钥
var publicKey = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwSbE5jE8D7KwDizStHWy
gGbTIWMMF41jGYoYBqVg5gXy94M4XkT2H9Ielwez5U5xO/ntygzvjO+rJ2kE/mf2
ET2i2kptBWxoZiEJ3Nbxv9gKBWhqDdYDmHP8/oLo0Sm/cm5ocw+24Yvccog4mP6J
74WLe6ikFPD+U9GwSWsG9fC+dauSoeusq1Zc5cApEFYYDimPJSJgCf85VPeEw+Bs
MnKKslUbIKUPLp2BtyBwJ/bME6ivq5Dj76AXfatWKX760toa1M324k+wfzdAgjuh
h00WqT24UM9wB1WwwwM/xZAoN9mcWvABHFuLGluPD643XqPN5g5y+l1j+zCvAGK7
hQIDAQAB
-----END PUBLIC KEY-----`

// 加密函数
export const RSAEncode = (data) => {
  let jse = new JSEncrypt()
  jse.setPublicKey(publicKey)
  var encryptedData = jse.encrypt(data)
  return encryptedData
}
