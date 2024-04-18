<template>
    <div class="container">
      <div class="left" :style="{ background: changeThemeColor.getCurrentColor() }">
        <div class="logo">
          {{ studioStore.studioName }}
        </div>
        <ManageAside />
      </div>
      <div class="right">
        <div class="top" :style="{ background: changeThemeColor.getCurrentColor() }">
          <ManageHeader />
        </div>
        <div class="bottom">
          <ManageMain />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import ManageHeader from '@/components/management/index/ManageHeader.vue'
  import ManageAside from '@/components/management/index/ManageAside.vue'
  import ManageMain from '@/components/management/index/ManageMain.vue'
  import { $errorMsg } from '@/utils/msg'
  import { onBeforeMount } from 'vue'
  import { useRouter } from 'vue-router'
  const router = useRouter()
  
  import { useJwtTokenStore } from '@/stores/authenticationStore'
  const jwtTokenStudio = useJwtTokenStore()
  
  import { useStudioStore } from '@/stores/index.js'
  const studioStore = useStudioStore()
  
  import { useChangeThemeColorStore } from '@/stores/themeColor.js'
  
  const changeThemeColor = useChangeThemeColorStore()
  
  onBeforeMount(() => {
    if (jwtTokenStudio.getIdentity() === null) {
      $errorMsg('请先登录')
      router.push('/enter/')
    }
  })
  </script>
  
  <style scoped>
  .container {
    max-width: 100%;
    min-height: 98.5vh;
    padding: 0px 0px 0px 0px;
    margin: -5px 0px 0px -5px;
    display: flex;
  }
  
  .left {
    width: 18%;
  }
  
  .logo {
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 22px;
    border: 1px solid #eee;
    padding: 10px 5px;
    border-radius: 4px;
  }
  
  .right {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  .top {
    max-height: 54px;
  }
  
  .bottom {
    flex: 1;
  }
  </style>
  