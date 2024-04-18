<template>
  <nav class="navbar">
    <ul class="navbar-list extern-header-card">
      <li class="navbar-item">
        <a class="navbar-item-a navbar-title" href="/">{{ studioStore.studioName }}</a>
      </li>
      <li :class="{ active: $route.path === '/home' }" class="navbar-item">
        <a class="navbar-item-a navbar-page" href="/home">首页</a>
      </li>
      <li :class="{ active: $route.path === '/partner' }" class="navbar-item">
        <a class="navbar-item-a navbar-page" href="/partner">合作商户</a>
      </li>
      <li :class="{ active: $route.path === '/product' }" class="navbar-item">
        <a class="navbar-item-a navbar-page" href="/product">充电宝投放</a>
      </li>
      <li :class="{ active: $route.path === '/notice' }" class="navbar-item">
        <a class="navbar-item-a navbar-page" href="/notice">公告栏</a>
      </li>
      <li :class="{ active: $route.path === '/user' }" class="navbar-item">
        <a class="navbar-item-a navbar-page" href="/user">个人中心</a>
      </li>
      <li :class="{ active: $route.path === '/management' }" class="navbar-item">
        <a class="navbar-item-a navbar-page" href="/management">后台管理</a>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { useStudioStore } from '@/stores/index.js'
const studioStore = useStudioStore()
</script>

<style scoped>
.navbar {
  height: 60%;
  width: 100%;
}

.navbar-list {
  height: 100%;
  width: 101%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #21272f;
}

.navbar-title {
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  color: white;
}

.navbar-page {
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  color: white;
}

li {
  list-style: none;
  padding: 16px;
  height: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.active {
  padding-top: 13px;
  padding-bottom: 11px;
  background: #009cce;
}
</style>
