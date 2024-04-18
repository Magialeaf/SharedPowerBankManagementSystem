<template>
  <div class="manage-main">
    <HeaderTip :title="titleValue" />
    <router-view></router-view>
  </div>
</template>

<script setup>
import HeaderTip from '@/components/management/utils/HeaderTip.vue'
import { useManageMainStore } from '@/stores/manageStore'
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const manageMainStore = useManageMainStore()
const route = useRoute()

const titleValue = ref(
  computed(() => {
    const routeName = '/management/' + route.name
    const items = manageMainStore.getItems().value
    for (let i = 0; i < items.length; i++) {
      if (items[i].subMenu !== null) {
        for (let j = 0; j < items[i].subMenu.length; j++) {
          if (items[i].subMenu[j].router === routeName) {
            return items[i].subMenu[j].text
          }
        }
      } else {
        if (items[i].router === routeName) {
          return items[i].text
        }
      }
    }
    return '未知路由'
  })
)
</script>

<style scoped>
.manage-main {
  margin-left: 2%;
  height: 80%;
  width: 96%;
}
</style>
