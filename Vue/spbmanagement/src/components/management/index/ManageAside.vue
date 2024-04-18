<template>
  <el-col>
    <el-menu
      active-text-color="#ffd04b"
      :background-color="changeThemeColor.getCurrentColor()"
      class="el-menu-vertical-demo"
      :unique-opened="uniqueOpenedValue"
      :default-active="AdminHeader"
      text-color="#fff"
      router
    >
      <template v-for="item in menuItems">
        <el-sub-menu v-if="item.subMenu" :index="item.router" :key="item.id">
          <template #title>
            <el-icon><component :is="item.iconName"></component> </el-icon>
            <span>{{ item.text }}</span>
          </template>
          <el-menu-item-group v-for="group in item.subMenu" :key="group.id">
            <el-menu-item :index="group.router">
              <el-icon><component :is="group.iconName"></component> </el-icon>
              <span>{{ group.text }}</span>
            </el-menu-item>
          </el-menu-item-group>
        </el-sub-menu>
        <el-menu-item v-else :index="item.router" :key="item.router">
          <el-icon><component :is="item.iconName"></component> </el-icon>
          <span>{{ item.text }}</span>
        </el-menu-item>
      </template>
    </el-menu>
  </el-col>
</template>

<script setup>
import { onBeforeMount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useChangeThemeColorStore } from '@/stores/themeColor.js'
import { useManageMainStore } from '@/stores/manageStore.js'

const changeThemeColor = useChangeThemeColorStore()
const manageMainStore = useManageMainStore()

const menuItems = ref()
const AdminHeader = ref('/management/manage-home')
const uniqueOpenedValue = ref(true)
const route = useRoute()

watch(
  () => route.path,
  (currentPath) => {
    AdminHeader.value = currentPath
  }
)

onBeforeMount(() => {
  menuItems.value = manageMainStore.getItems().value
})
</script>

<style scoped></style>
