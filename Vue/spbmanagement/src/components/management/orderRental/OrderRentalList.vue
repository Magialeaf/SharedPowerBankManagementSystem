<template>
  <el-table :data="orderRentalList" stripe border>
    <el-table-column class="table-column" min-width="5%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="5%" prop="power_bank" label="充电宝id" />
    <el-table-column
      class="table-column"
      min-width="10%"
      prop="power_bank_name"
      label="充电宝名称"
    />
    <el-table-column class="table-column" min-width="5%" prop="user" label="用户id" />
    <el-table-column class="table-column" min-width="10%" prop="user_name" label="用户名称" />
    <el-table-column class="table-column" min-width="5%" prop="returned" label="是否归还" />
    <el-table-column class="table-column" min-width="10%" prop="rental_date" label="起始日期" />

    <el-table-column min-width="15%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <OrderOperation v-if="drawer" :id="selectedId" :ifNew="false"
  /></el-drawer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
import { useOrderRentalStore } from '@/stores/orderStore'
import OrderOperation from '@/components/management/orderRental/OrderRentalOperation.vue'

const orderRentalStore = useOrderRentalStore()

const orderRentalList = computed(() => prop.orderRentalData)

const drawer = ref(false)
const selectedId = ref(undefined)

const prop = defineProps({
  orderRentalData: {
    type: Array
  }
})

function showDetails(row) {
  selectedId.value = row.id
  drawer.value = true // 打开抽屉
}

function deleteRow(row) {
  $confirmDeleteMsg('确定删除充电宝吗?')
    .then(() => {
      orderRentalStore.deleteInfo(row.id)
    })
    .catch(() => {
      $errorMsg('取消删除')
    })
}
</script>

<style scoped></style>
