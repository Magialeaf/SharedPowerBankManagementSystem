<template>
  <div class="title-box">
    <h2 class="title">{{ accountLogin ? '账号登录' : '邮箱登录' }}</h2>
  </div>

  <el-form
    v-if="accountLogin"
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="accountLoginValue"
  >
    <el-form-item label="用户名">
      <el-input v-model="accountLoginValue.account"></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input type="password" v-model="accountLoginValue.password" show-password></el-input>
    </el-form-item>
  </el-form>

  <el-form
    v-else
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="emailLoginValue"
  >
    <el-form-item label="邮箱">
      <el-input v-model="emailLoginValue.email"></el-input>
    </el-form-item>
    <el-form-item label="验证码">
      <CaptchaInput
        :email="emailLoginValue.email"
        @captcha-value="
          (value) => {
            emailLoginValue.captcha = value
          }
        "
      />
    </el-form-item>
  </el-form>

  <div class="switch-login">
    <el-button @click="accountLogin = !accountLogin"
      >切换到{{ accountLogin ? '邮箱登录' : '账号登录' }}</el-button
    >
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, computed } from 'vue'
import { useEnterStore } from '@/stores/enterStore'
import CaptchaInput from '@/components/enter/CaptchaInput.vue'
import { useRouter } from 'vue-router'

const enterStore = useEnterStore()
const router = useRouter()

const accountLogin = ref(true)
const confirmLogin = computed(() => props.confirmLogin)

const props = defineProps({
  confirmLogin: {
    type: Boolean,
    required: true
  }
})
const emits = defineEmits(['login'])

const accountLoginValue = ref({
  account: '',
  password: ''
})

const emailLoginValue = ref({
  email: '',
  captcha: ''
})

watch(confirmLogin, (newValue) => {
  if (newValue) {
    login()
    emits('login', false)
  }
})

function login() {
  if (accountLogin.value) {
    enterStore
      .accountLogin(accountLoginValue.value)
      .then((res) => {
        router.push('/')
      })
      .catch((e) => {})
  } else {
    enterStore
      .emailLogin(emailLoginValue.value)
      .then((res) => {
        router.push('/')
      })
      .catch((e) => {})
  }
}
</script>

<style scoped>
.title {
  text-align: center;
  color: black;
  user-select: none;
  letter-spacing: 5px;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 50px;
}

.switch-login {
  display: flex;
  justify-content: center;
  text-align: center;
}
</style>
