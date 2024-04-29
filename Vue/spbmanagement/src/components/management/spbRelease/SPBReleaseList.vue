<template>
  <el-table :data="powerBankList" stripe border>
    <el-table-column class="table-column" min-width="7%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="10%" prop="name" label="充电宝名称" />
    <el-table-column class="table-column" min-width="10%" label="充电宝图片">
      <template v-slot="scope">
        <img :src="scope.row.img" alt="图片" style="width: 100px; height: 100px" />
      </template>
    </el-table-column>
    <el-table-column class="table-column" min-width="8%" prop="status" label="充电宝状态" />
    <el-table-column class="table-column" min-width="13%" prop="areaName" label="所属地址" />
    <el-table-column class="table-column" min-width="13%" prop="merchantName" label="所属商户" />
    <el-table-column class="table-column" min-width="10%" prop="hourly_fee" label="每小时费用" />
    <el-table-column
      class="table-column"
      min-width="10%"
      prop="electricity_percentage"
      label="电量百分比"
    />

    <el-table-column min-width="14%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <SPBReleaseOperation v-if="drawer" :id="selectedId" :ifNew="false"
  /></el-drawer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
import { useSPBStore } from '@/stores/SPBStore'
import SPBReleaseOperation from '@/components/management/spbRelease/SPBReleaseOperation.vue'

const powerBankStore = useSPBStore()

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
