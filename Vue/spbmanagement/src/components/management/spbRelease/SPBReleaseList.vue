<template>
  <el-table
    :data="powerBankList"
    stripe
    border
    @filter-change="handleFilter"
    @sort-change="handleSortChange"
  >
    <el-table-column class="table-column" min-width="7%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="10%" prop="name" label="充电宝名称" />
    <el-table-column class="table-column" min-width="10%" label="充电宝图片">
      <template v-slot="scope">
        <img :src="scope.row.img" alt="图片" style="width: 100px; height: 100px" />
      </template>
    </el-table-column>
    <el-table-column
      class="table-column"
      :filters="statusList"
      :filter-multiple="false"
      column-key="status"
      min-width="10%"
      prop="status_name"
      label="充电宝状态"
    />
    <el-table-column class="table-column" min-width="11%" prop="areaName" label="所属地址" />
    <el-table-column class="table-column" min-width="13%" prop="merchantName" label="所属商户" />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="10%"
      prop="hourly_fee"
      label="每小时费用"
    />
    <el-table-column
      class="table-column"
      sortable="custom"
      min-width="10%"
      prop="electricity_percentage"
      label="电量百分比"
    >
      <template v-slot:default="{ row }"> {{ row.electricity_percentage }}% </template>
    </el-table-column>

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
import { useSPBStore, useSPBConfigStore } from '@/stores/SPBStore'
import SPBReleaseOperation from '@/components/management/spbRelease/SPBReleaseOperation.vue'

const powerBankStore = useSPBStore()
const powerBankConfigStore = useSPBConfigStore()

const statusList = computed(() =>
  Object.entries(powerBankConfigStore.getPowerBankStatusChoices()).map(([value, text]) => ({
    text,
    value: parseInt(value)
  }))
)

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

const emits = defineEmits(['filter-status', 'sort-by'])

function handleFilter(filters) {
  emits('filter-status', filters.status[0])
}

function handleSortChange(value) {
  const { prop, order } = value
  if (order === 'ascending') {
    emits('sort-by', `${prop}`)
  } else {
    emits('sort-by', `-${prop}`)
  }
}
</script>

<style scoped></style>
