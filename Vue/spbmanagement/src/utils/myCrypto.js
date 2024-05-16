/*
密码相关函数：
	1.RSAEncode()：RSA加密，用于密码

*/

import JSEncrypt from 'jsencrypt'

// 公钥
var publicKey = ``

// 加密函数
export const RSAEncode = (data) => {
  let jse = new JSEncrypt()
  jse.setPublicKey(publicKey)
  var encryptedData = jse.encrypt(data)
  return encryptedData
}
