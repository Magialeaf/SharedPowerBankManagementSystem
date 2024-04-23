<template>
  <el-table :data="merchantList" stripe border>
    <el-table-column class="table-column" min-width="10%" prop="id" label="id" />
    <el-table-column class="table-column" min-width="10%" prop="shop_name" label="商户名称" />
    <el-table-column class="table-column" min-width="15%" prop="areaName" label="所述区域" />
    <el-table-column class="table-column" min-width="15%" prop="address" label="详细地址" />
    <el-table-column class="table-column" min-width="10%" prop="liaison" label="联系人" />
    <el-table-column class="table-column" min-width="15%" prop="phone" label="联系电话" />
    <el-table-column class="table-column" min-width="10%" label="商户图片">
      <template v-slot="scope">
        <img :src="scope.row.shop_img" alt="图片" style="width: 100px; height: 100px" />
      </template>
    </el-table-column>

    <el-table-column min-width="15%" label="操作">
      <template v-slot="scope">
        <el-button type="info" @click="showDetails(scope.row)">详细</el-button>
        <el-button type="warning" @click="deleteRow(scope.row)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer v-model="drawer" size="50%" :with-header="false">
    <MerchantOperation v-if="drawer" :id="selectedId" :ifNew="false"
  /></el-drawer>
</template>

<script setup>
import { ref, computed } from 'vue'
import { $confirmDeleteMsg, $errorMsg } from '@/utils/msg'
import { useMerchantStore } from '@/stores/merchantStore'
import MerchantOperation from '@/components/management/merchant/MerchantOperation.vue'

const merchantStore = useMerchantStore()

const merchantList = computed(() => prop.merchantData)

const drawer = ref(false)
const selectedId = ref(undefined)

const prop = defineProps({
  merchantData: {
    type: Array
  }
})

function showDetails(row) {
  selectedId.value = row.id
  drawer.value = true // 打开抽屉
}

function deleteRow(row) {
  $confirmDeleteMsg('确定删除商户吗?')
    .then(() => {
      merchantStore.deleteMerchant(row.id)
    })
    .catch(() => {
      $errorMsg('取消删除')
    })
}
</script>

<style scoped></style>
