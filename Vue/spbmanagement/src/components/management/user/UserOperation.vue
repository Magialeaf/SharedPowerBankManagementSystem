<template>
  <el-form label-position="left" label-width="20%" :model="userInfo" style="max-width: 600px">
    <el-form-item v-if="userInfo.id" label="uid">
      <el-input v-model="userInfo.id" disabled />
    </el-form-item>
    <el-form-item v-if="userInfo.id" label="用户名">
      <el-input v-model="userInfo.username" />
    </el-form-item>
    <el-form-item v-if="userInfo.id" label="性别">
      <el-select v-model="userInfo.sex" placeholder="请选择">
        <el-option label="男" value="男" />
        <el-option label="女" value="女" />
        <el-option label="保密" value="保密" />
      </el-select>
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
    <el-form-item v-if="userInfo.id" label="简介">
      <el-input v-model="userInfo.profile" />
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
    <el-form-item v-if="userInfo">
      <el-button type="success" @click="updateUserInfo">保存更改</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue'
import { convertSexNameToCode } from '@/utils/convert'
import { useUserStore } from '@/stores/userStore'
import { lockFunction } from '@/utils/myLock'
import UploadImg from '@/components/management/utils/UploadImg.vue'

const prop = defineProps({
  userData: { type: Object },
  ifMyself: { type: Boolean }
})

const userStore = useUserStore()
const ifUploadValue = ref(false)
const userInfo = computed(() => prop.userData)
const ifMyself = computed(() => prop.ifMyself)

const emits = defineEmits(['updateUserInfo'])

function updateImgUrl(value) {
  emits('updateUserInfo', { avatar: value })
}

function updateIfUpload(value) {
  ifUploadValue.value = value
}

const updateUserInfo = lockFunction()(() => {
  ifUploadValue.value = true
})

function afterUploadImgSuccess(value) {
  userInfo.value.avatar = value.data.avatar
  userInfo.value.sex = convertSexNameToCode(userInfo.value.sex)
  if (ifMyself.value) {
    userStore
      .updateMyInfo(userInfo.value)
      .then((res) => {
        emits('updateUserInfo', res.data)
      })
      .catch((e) => {})
  } else {
    userStore
      .updateOneInfo(userInfo.value['id'], userInfo.value)
      .then((res) => {
        emits('updateUserInfo', res.data)
      })
      .catch((e) => {})
  }
}
</script>

<style scoped>
.avatar-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
</style>
