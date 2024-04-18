<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="accountInfo.id" label="aid">
      <el-input v-model="accountInfo.id" disabled />
    </el-form-item>
    <el-form-item v-if="accountInfo.id" label="创建时间">
      <el-input v-model="accountInfo.create_time" disabled />
    </el-form-item>
    <el-form-item v-if="accountInfo.id" label="最后登录时间">
      <el-input v-model="accountInfo.last_login_time" disabled />
    </el-form-item>
  </el-form>

  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="accountInfo.id" label="账户名">
      <el-input v-model="accountInfo.account" />
    </el-form-item>
    <el-form-item v-if="accountInfo.id">
      <el-button type="success" @click="updateAccountInfo">保存更改</el-button>
    </el-form-item>
  </el-form>

  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="accountInfo.id" label="新密码">
      <el-input type="password" v-model="password" show-password />
    </el-form-item>
    <el-form-item v-if="accountInfo.id" label="确认密码">
      <el-input type="password" v-model="passwordConfirm" show-password />
    </el-form-item>
    <el-form-item v-if="accountInfo.id">
      <el-button type="success" @click="updatePasswordInfo()">保存更改</el-button>
    </el-form-item>
  </el-form>

  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="accountInfo.id" label="邮箱">
      <el-input v-model="accountInfo.email" />
    </el-form-item>
    <el-form-item v-if="accountInfo.id" label="验证码">
      <CaptchaInput :email="accountInfo.email" @captcha-value="handleCaptchaUpdated"
    /></el-form-item>
    <el-form-item v-if="accountInfo.id">
      <el-button type="success" @click="updateEmailInfo()">保存更改</el-button>
    </el-form-item>
  </el-form>

  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <div
      v-if="
        jwtTokenStore.getIdentity() === '超级管理员' || jwtTokenStore.getIdentity() === '管理员'
      "
    >
      <el-form-item v-if="accountInfo.id" label="身份">
        <el-select v-model="accountInfo.identity" placeholder="请选择身份">
          <el-option
            v-for="item in identityStore.getIdentityList()"
            :key="item"
            :label="item"
            :value="item"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item v-if="accountInfo.id">
        <el-button type="success" @click="updateIdentityInfo()">保存更改</el-button>
      </el-form-item>
    </div>
    <div v-else>
      <el-form-item v-if="accountInfo.id" label="身份">
        <el-input v-model="accountInfo.identity" disabled></el-input>
      </el-form-item>
    </div>
  </el-form>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useIdentityStore, useJwtTokenStore } from '@/stores/authenticationStore'
import { useAccountStore } from '@/stores/userStore'
import { lockFunction } from '@/utils/myLock'
import { RSAEncode } from '@/utils/myCrypto'
import {
  validate_account,
  validate_confirmPassword,
  validate_password,
  validate_email
} from '@/utils/validateUser'
import CaptchaInput from '@/components/enter/CaptchaInput.vue'

const identityStore = useIdentityStore()
const jwtTokenStore = useJwtTokenStore()
const accountStore = useAccountStore()

const ifMyself = computed(() => prop.ifMyself)
const accountInfo = computed(() => prop.accountData)
const captchaValue = ref()
const password = ref()
const passwordConfirm = ref()

const prop = defineProps({
  accountData: { type: Object },
  ifMyself: { type: Boolean }
})

function handleCaptchaUpdated(value) {
  captchaValue.value = value
}

const updateAccountInfo = lockFunction()(() => {
  if (!validate_account(accountInfo.value.account)) return false
  if (ifMyself.value) {
    accountStore
      .updateMyAccount(accountInfo.value.account)
      .then((res) => {
        accountInfo.value.account = res.data.account
      })
      .catch((err) => {})
  } else {
    accountStore
      .updateAccount(accountInfo.value.id, accountInfo.value.account)
      .then((res) => {
        accountInfo.value.account = res.data.account
      })
      .catch((err) => {})
  }
})

const updatePasswordInfo = lockFunction()(() => {
  if (
    !validate_password(password.value) ||
    !validate_confirmPassword(password.value, passwordConfirm.value)
  )
    return false
  const pwd = RSAEncode(password.value)
  if (ifMyself.value) {
    accountStore
      .updateMyPassword(pwd)
      .then((res) => {
        password.value = ''
        passwordConfirm.value = ''
      })
      .catch((err) => {})
  } else {
    accountStore
      .updatePassword(accountInfo.value.id, password.value)
      .then((res) => {
        password.value = ''
        passwordConfirm.value = ''
      })
      .catch((err) => {})
  }
})

const updateEmailInfo = lockFunction()(() => {
  if (!validate_email(accountInfo.value.email)) return false
  if (ifMyself.value) {
    accountStore
      .updateMyEmail(accountInfo.value.email, captchaValue.value)
      .then((res) => {
        accountInfo.value.email = res.data.email
      })
      .catch((err) => {})
  } else {
    accountStore
      .updateEmail(accountInfo.value.id, accountInfo.value.email, captchaValue.value)
      .then((res) => {
        accountInfo.value.email = res.data.email
      })
      .catch((err) => {})
  }
})

const updateIdentityInfo = lockFunction()(() => {
  accountStore
    .updateIdentity(accountInfo.value.id, accountInfo.value.identity)
    .then((res) => {})
    .catch((err) => {})
})
</script>

<style scoped>
.form-item {
  border: 1px solid #9fabc8;
  padding: 5px;
  margin-bottom: 20px;
}
</style>
