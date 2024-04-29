<template>
  <el-table :data="powerBankList" stripe border>
    <el-table-column class="table-column" min-width="5%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="5%" prop="power_bank" label="充电宝id" />
    <el-table-column
      class="table-column"
      min-width="10%"
      prop="power_bank_name"
      label="充电宝名称"
    />
    <el-table-column class="table-column" min-width="7%" prop="status" label="维护状态" />
    <el-table-column
      class="table-column"
      min-width="5%"
      prop="maintainer_account"
      label="维护人id"
    />
    <el-table-column
      class="table-column"
      min-width="10%"
      prop="maintainer_account_name"
      label="维护人名称"
    />
    <el-table-column
      class="table-column"
      min-width="14%"
      prop="question_description"
      label="问题描述"
    />
    <el-table-column class="table-column" min-width="5%" prop="finished" label="是否处理" />
    <el-table-column class="table-column" min-width="10%" prop="date" label="处理日期" />
    <el-table-column
      class="table-column"
      min-width="14%"
      prop="maintenance_result"
      label="处理结果"
    />

    <el-table-column min-width="15%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <SPBMaintenanceOperation v-if="drawer" :id="selectedId" :ifNew="false"
  /></el-drawer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
import { useSPBMaintenanceStore } from '@/stores/SPBStore'
import SPBMaintenanceOperation from '@/components/management/spbMaintenance/SPBMaintenanceOperation.vue'

const powerBankStore = useSPBMaintenanceStore()

const powerBankList = computed(() => prop.powerBankData)

const drawer = ref(false)
const selectedId = ref(undefined)

const prop = defineProps({
  powerBankData: {
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
      powerBankStore.deleteInfo(row.id)
    })
    .catch(() => {
      $errorMsg('取消删除')
    })
}
</script>

<style scoped></style>
