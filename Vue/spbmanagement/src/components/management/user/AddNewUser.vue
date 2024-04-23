<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="userInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="userInfo.id" label="名称">
      <el-input v-model="userInfo.username"></el-input>
    </el-form-item>
    <el-form-item v-if="userInfo.id" label="头像">
      <UploadImg
        :imgUrl="userInfo.avatar"
        :ifUpload="ifUploadValue"
        :uploadFunc="userStore.uploadAvatar"
        @updateIfUpload="updateIfUpload"
        @updateImgUrl="updateImgUrl"
        @uploadSuccess="afterUploadImgSuccess"
      />
    </el-form-item>
    <el-form-item v-if="userInfo.id" label="性别">
      <el-select v-model="userInfo.sex" placeholder="请选择">
        <el-option label="男" value="男" />
        <el-option label="女" value="女" />
        <el-option label="保密" value="保密" /> </el-select
    ></el-form-item>
    <el-form-item v-if="userInfo.id" label="简介">
      <el-input v-model="userInfo.profile" :max-length="100"></el-input>
    </el-form-item>
    <el-form-item v-if="userInfo.id" label="生日">
      <el-date-picker
        v-model="userInfo.birthday"
        type="date"
        placeholder="生日"
        format="YYYY/MM/DD"
        value-format="YYYY-MM-DD"
      />
    </el-form-item>
  </el-form>

  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="accountInfo.id" label="账号">
      <el-input v-model="accountInfo.account"></el-input>
    </el-form-item>
    <el-form-item v-if="accountInfo.id" label="密码">
      <el-input type="password" v-model="accountInfo.password" show-password></el-input>
    </el-form-item>
    <el-form-item v-if="accountInfo.id" label="邮箱">
      <el-input v-model="accountInfo.email"></el-input>
    </el-form-item>

    <el-form-item v-if="accountInfo.id" label="身份">
      <el-input :value="accountInfo.identity" disabled></el-input>
    </el-form-item>
  </el-form>

  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountInfo"
    style="max-width: 600px"
  >
    <el-form-item>
      <el-button type="success" @click="createUser">新建用户</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useIdentityStore } from '@/stores/authenticationStore'
import { lockFunction } from '@/utils/myLock'
import { convertSexNameToCode } from '@/utils/convert'
import { validate_account, validate_email, validate_password } from '@/utils/validateUser'
import { RSAEncode } from '@/utils/myCrypto'
import UploadImg from '@/components/management/utils/UploadImg.vue'

const userStore = useUserStore()
const identityStore = useIdentityStore()

const props = defineProps({
  identityCode: { type: Number, default: -1 }
})

const userInfo = ref({
  id: -1,
  username: '',
  sex: '保密',
  avatar: userStore.defaultAvatarURL,
  profile: '',
  birthday: '2001-01-01'
})

const accountInfo = ref({
  id: -1,
  account: '',
  email: '',
  identity: identityStore.getIdentity(props.identityCode),
  create_time: '',
  last_login_time: ''
})

const ifUploadValue = ref(false)

function updateImgUrl(value) {
  userInfo.value.avatar = value
}

const updateIfUpload = (value) => {
  ifUploadValue.value = value
}

const createUser = lockFunction()(() => {
  ifUploadValue.value = true
})

function afterUploadImgSuccess(value) {
  if (!validate_account(accountInfo.value.account)) return false
  if (!validate_email(accountInfo.value.email)) return false
  if (!validate_password(accountInfo.value.password)) return false

  const inputData = { ...userInfo.value, ...accountInfo.value }
  inputData.sex = convertSexNameToCode(inputData.sex)
  inputData.avatar = value.data.avatar
  inputData.password = RSAEncode(inputData.password)

  userStore
    .createOneInfo(inputData)
    .then((res) => {
      // console.log(res)
    })
    .catch((e) => {})
}
</script>

<style scoped>
.form-item {
  padding: 5px;
  margin-bottom: 20px;
}
</style>
