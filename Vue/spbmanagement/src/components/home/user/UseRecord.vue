<template>
  <el-table :data="orderList" stripe border @sort-change="handleSortChange">
    <el-table-column class="table-column" min-width="20%" prop="number" label="订单编号" />
    <el-table-column class="table-column" min-width="16%" label="充电宝名称">
      <template #default="{ row }">
        <el-button link type="primary" @click="showDetail(row)">
          {{ row.power_bank_name }}
        </el-button>
      </template>
    </el-table-column>
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="15%"
      prop="fee"
      label="费用（元）"
    />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="13%"
      prop="rental_date"
      label="租用时间"
    />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="13%"
      prop="return_date"
      label="归还时间"
    />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="13%"
      prop="pay_date"
      label="支付时间"
    />
    <el-table-column class="table-column" min-width="10%" label="操作">
      <template #default="{ row }">
        <el-button v-if="row.returned === false" type="success" @click="operation(row)"
          >归还</el-button
        >
        <el-button v-if="row.paid === false" type="success" @click="operation(row)">支付</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
import { useOrderUserStore } from '@/stores/orderStore'
import { lockFunction } from '@/utils/myLock'
import { useRouter } from 'vue-router'
import { ref, computed, defineProps } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
})

const searchKey = ref({
  order_by: []
})

const orderUserStore = useOrderUserStore()
const orderList = computed(() => props.data)

const router = useRouter()

const operation = lockFunction(1000)((row) => {
  orderUserStore
    .updateInfo(row.rental, {}, row.now_type)
    .then((res) => {})
    .catch((e) => {})
})

const showDetail = (row) => {
  router.push({ path: `/product/${row.power_bank}` })
}

function handleSortChange(val) {
  const { prop, order } = val

  if (order === 'ascending') {
    searchKey.value.order_by = [prop]
  } else {
    searchKey.value.order_by = [`-${prop}`]
  }

  orderUserStore
    .getList(orderUserStore.getPageInfo().currentPage, searchKey.value)
    .then((res) => {})
    .catch((e) => {})
}
</script>

<style scoped></style>
