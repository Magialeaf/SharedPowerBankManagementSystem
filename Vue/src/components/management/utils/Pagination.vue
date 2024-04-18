<template>
  <el-config-provider :locale="zhCn">
    <el-pagination
      :current-page="prop.pageInfo.currentPage"
      :page-size="prop.pageInfo.pageSize"
      :total="prop.pageInfo.total"
      :page-count="prop.pageInfo.pageCount"
      :pager-count="prop.pageInfo.pagerCount"
      layout="jumper, prev, pager, next, total"
      @current-change="handlePageChange"
    />
  </el-config-provider>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
// ElConfigProvider 组件
import { ElConfigProvider } from 'element-plus'
// 引入中文包
import zhCn from 'element-plus/es/locale/lang/zh-cn'
// 更改分页文字
zhCn.el.pagination.total = '共 {total} 条'
zhCn.el.pagination.goto = '跳至'
zhCn.el.pagination.pagesize = '条/页'
zhCn.el.pagination.pageClassifier = '页'

const prop = defineProps({
  pageInfo: {
    type: Object,
    required: true,
    validator: (value) => {
      const requiredProps = ['currentPage', 'pageSize', 'total', 'pageCount', 'pagerCount']
      return requiredProps.every((propName) => {
        return Object.prototype.hasOwnProperty.call(value, propName)
      })
    }
  }
})

const emit = defineEmits(['page-change'])
const handlePageChange = (page) => {
  emit('page-change', page)
}
</script>

<style scoped></style>
