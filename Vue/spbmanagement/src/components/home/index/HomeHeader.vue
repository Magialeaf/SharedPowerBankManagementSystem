<template>
  <nav class="navbar">
    <ul class="navbar-list extern-header-card">
      <li class="navbar-item">
        <a class="navbar-item-a navbar-title" href="/">{{ studioStore.studioName }}</a>
      </li>
      <li :class="{ active: $route.path === '/home' }" class="navbar-item">
        <router-link :to="{ path: '/home' }" class="navbar-item-a navbar-page">首页</router-link>
      </li>
      <li :class="{ active: $route.path.startsWith('/partner') }" class="navbar-item">
        <router-link :to="{ path: '/partner' }" class="navbar-item-a navbar-page"
          >合作商户</router-link
        >
      </li>
      <li :class="{ active: $route.path.startsWith('/product') }" class="navbar-item">
        <router-link :to="{ path: '/product' }" class="navbar-item-a navbar-page"
          >充电宝投放</router-link
        >
      </li>
      <li :class="{ active: $route.path.startsWith('/notice') }" class="navbar-item">
        <router-link :to="{ path: '/notice' }" class="navbar-item-a navbar-page"
          >公告栏</router-link
        >
      </li>
      <li :class="{ active: $route.path.startsWith('/user') }" class="navbar-item">
        <router-link :to="{ path: '/user' }" class="navbar-item-a navbar-page"
          >个人中心</router-link
        >
      </li>
      <li :class="{ active: $route.path === '/management' }" class="navbar-item">
        <router-link :to="{ path: '/management' }" class="navbar-item-a navbar-page"
          >后台管理</router-link
        >
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
  height: 100%;
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
