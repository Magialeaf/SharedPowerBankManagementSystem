<template>
  <div class="box">
    <div class="pre-box" ref="preRef">
      <h2>欢迎使用{{ studioStore.studioName }}</h2>
      <p>{{ ifLogin ? '登录系统！' : '加入我们！' }}</p>
      <div class="img-box">
        <img v-if="ifLogin" src="@/assets/img/enter/waoku.jpg" alt="" />
        <img v-else src="@/assets/img/enter/wuwu.jpg" alt="" />
      </div>
    </div>
    <div class="form-box">
      <div class="enter-data-box">
        <Register
          :confirmRegister="confirmRegister"
          @register="
            (value) => {
              confirmRegister = value
            }
          "
        />
      </div>
      <div class="btn-box">
        <el-button type="primary" @click="confirmRegister = true">注册</el-button>
        <p @click="switchPage()">已有账号?去登录</p>
      </div>
    </div>
    <div class="form-box">
      <div class="enter-data-box">
        <Login
          :confirmLogin="confirmLogin"
          @login="
            (value) => {
              confirmLogin = value
            }
          "
        />
      </div>
      <div class="btn-box">
        <el-button type="primary" @click="confirmLogin = true">登录</el-button>
        <p @click="switchPage()">没有账号?去注册</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStudioStore } from '@/stores/index.js'

const studioStore = useStudioStore()
const preRef = ref(null)
const ifLogin = ref(true)
const confirmLogin = ref(false)
const confirmRegister = ref(false)

const switchPage = () => {
  if (ifLogin.value) {
    preRef.value.style.background = '#c9e0ed'
    preRef.value.style.transform = 'translateX(100%)'
  } else {
    preRef.value.style.background = '#edd4dc'
    preRef.value.style.transform = 'translateX(0%)'
  }
  ifLogin.value = !ifLogin.value
}
</script>

<style scoped>
/* 最外层的大盒子 */
.box {
  width: 100%;
  height: 100%;
  display: flex;
  position: relative;
  z-index: 2;
  margin: auto;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 2px 1px 19px rgba(0, 0, 0, 0.1);
}

/* 移动盒子 */
.pre-box {
  width: 50%;
  height: 100%;
  position: absolute;
  left: 0;
  top: 0;
  z-index: 99;
  border-radius: 4px;
  background-color: #edd4dc;
  box-shadow: 2px 1px 19px rgba(0, 0, 0, 0.1);
  transition: 0.5s ease-in-out;
}

/* 滑动盒子的标题 */
.pre-box h2 {
  margin-top: 150px;
  text-align: center;
  letter-spacing: 5px;
  color: black;
  user-select: none;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 滑动盒子的文字 */
.pre-box p {
  height: 30px;
  line-height: 30px;
  text-align: center;
  margin: 20px 0;
  user-select: none;
  font-weight: bold;
  color: black;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 图片盒子 */
.img-box {
  width: 200px;
  height: 200px;
  margin: 20px auto;
  border-radius: 50%;
  user-select: none;
  overflow: hidden;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 图片 */
.img-box img {
  width: 100%;
  transition: 0.5s;
}

/* 登录和注册盒子 */
.form-box {
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}

.enter-data-box {
  width: 80%;
  height: 60%;
}

/* 按钮盒子 */
.btn-box {
  width: 60%;
  display: flex;
  justify-content: space-evenly;
}

/* 按钮文字 */
.btn-box p {
  height: 30px;
  line-height: 30px;
  /* 禁止选中 */
  user-select: none;
  font-size: 14px;
  color: black;
}

.btn-box p:hover {
  cursor: pointer;
  border-bottom: 1px solid black;
}
</style>
