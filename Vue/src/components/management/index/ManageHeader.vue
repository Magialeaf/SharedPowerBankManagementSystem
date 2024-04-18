<template>
  <div class="admin-header">
    <div class="admin-menu">
      <el-menu
        :default-active="AdminHeader"
        class="el-menu-demo"
        mode="horizontal"
        :background-color="changeThemeColor.getCurrentColor()"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <template v-for="item in menuItems">
          <el-sub-menu v-if="item.subMenu" :index="item.router" :key="item.id">
            <template #title>
              <el-icon><component :is="item.iconName"></component> </el-icon>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item
              v-for="subItem in item.subMenu"
              :index="subItem.id"
              :key="subItem.id"
              @click="subItem.function"
            >
              {{ subItem.name }}
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else :index="item.router" :key="item.router" @click="item.function">
            <el-icon><component :is="item.iconName"></component> </el-icon>
            <span>{{ item.name }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useChangeThemeColorStore } from '@/stores/themeColor.js'
import { useManageHeaderStore } from '@/stores/manageStore.js'
const changeThemeColor = useChangeThemeColorStore()
const manageHeaderStore = useManageHeaderStore()
const AdminHeader = ref('/management/manage-home')
const menuItems = ref()
const route = useRoute()

watch(
  () => route.path,
  (currentPath) => {
    AdminHeader.value = currentPath
  }
)

onBeforeMount(() => {
  menuItems.value = manageHeaderStore.getItems().value
})
</script>

<style scoped>
.admin-header {
  height: 100%;
  display: flex;
  flex-direction: row-reverse;
}

.admin-menu {
  height: 100%;
  min-width: 100%;
}

.el-menu--horizontal {
  height: 100%;
  justify-content: end;
}
</style>
