<template>
  <div class="title-box">
    <h2 class="title">注册账号</h2>
  </div>
  <el-form class="form-item" label-position="left" label-width="20%" :model="registerValue">
    <el-form-item label="用户名">
      <el-input v-model="registerValue.account"></el-input>
    </el-form-item>
    <el-form-item label="密码">
      <el-input type="password" v-model="registerValue.password" show-password></el-input>
    </el-form-item>
    <el-form-item label="确认密码">
      <el-input type="password" v-model="registerValue.confirmPassword" show-password></el-input>
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="registerValue.email"></el-input>
    </el-form-item>
    <el-form-item label="验证码">
      <CaptchaInput
        :email="registerValue.email"
        @captcha-value="
          (value) => {
            registerValue.captcha = value
          }
        "
      />
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits, computed } from 'vue'
import { useEnterStore } from '@/stores/enterStore'
import CaptchaInput from '@/components/enter/CaptchaInput.vue'
import { useRouter } from 'vue-router'

const enterStore = useEnterStore()
const router = useRouter()

const confirmRegister = computed(() => props.confirmRegister)

const props = defineProps({
  confirmRegister: {
    type: Boolean,
    required: true
  }
})
const emits = defineEmits(['Register'])

const registerValue = ref({
  account: '',
  password: '',
  confirmPassword: '',
  email: '',
  captcha: ''
})

watch(confirmRegister, (newValue) => {
  if (newValue) {
    register()
    emits('register', false)
  }
})

function register() {
  enterStore
    .register(registerValue.value)
    .then((res) => {
      router.push('/')
    })
    .catch((e) => {
      // console.log(registerValue.value)
    })
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
</style>
