<template>
  <div class="left-and-right">
    <el-input v-model="captchaValue" />
    <el-button
      class="get-captcha-btn"
      :disabled="getCaptchaDisable"
      type="primary"
      @click="getCaptcha()"
      >{{ getCaptchaBtnText }}</el-button
    >
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps, onBeforeMount, computed } from 'vue'
import { $errorMsg, $successMsg } from '@/utils/msg'
import { getCaptchaCacheByEmailAPI, getCaptchaByEmailAPI } from '@/api/enterAPI'
import { validate_email } from '@/utils/validateUser'

const captchaValue = ref('')
const getCaptchaDisable = ref(false)
const getCaptchaBtnText = ref('获取验证码')
const globalCountdown = ref(0)

const emits = defineEmits(['captcha-value'])

// 监听 captchaValue 变化并触发事件
watch(captchaValue, (newValue) => {
  emits('captcha-value', newValue)
})

const props = defineProps({
  email: {
    type: String,
    default: ''
  }
})

const email = computed(() => props.email)

// 获得用户刷新前的验证码
onBeforeMount(() => {
  getCaptchaCacheByEmailAPI()
    .then((res) => {
      blockButton(res.data.cooling_time)
    })
    .catch((e) => {
      $errorMsg(e.message)
    })
})

function blockButton(countdown = globalCountdown.value) {
  getCaptchaDisable.value = true

  let interval = setInterval(() => {
    if (countdown > 0) {
      getCaptchaBtnText.value = `${countdown} 秒后重新发送`
      countdown--
    } else {
      getCaptchaDisable.value = false
      getCaptchaBtnText.value = '获取验证码'
      clearInterval(interval)
    }
  }, 1000)
}

function getCaptcha() {
  const emailValue = email.value

  if (!validate_email(emailValue)) {
    return false
  }

  getCaptchaByEmailAPI(emailValue)
    .then((response) => {
      blockButton(response.data.cooling_time)
      $successMsg(response.message)
    })
    .catch((e) => {
      $errorMsg(e.message)
    })
}
</script>

<style scoped>
.left-and-right {
  width: 100%;
  display: flex;
  justify-content: space-between;
}
</style>
