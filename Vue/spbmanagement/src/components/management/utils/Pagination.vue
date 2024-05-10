<template>
  <div class="pagination-container">
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
  </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, ref, nextTick } from 'vue'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// 初始化滚动行为的ref
const scrollContainerRef = ref(null)

// 修改分页文字
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
  },
  ifGoTop: {
    type: Boolean,
    default: true
  }
})

const emits = defineEmits(['page-change'])

// 处理页面变更事件，并滚动到顶部
const handlePageChange = async (page) => {
  emits('page-change', page)
  if (prop.ifGoTop) {
    scrollContainerRef.value.scrollTop = 0
  }
}

// 挂载时设置滚动容器的引用
onMounted(() => {
  scrollContainerRef.value = document.documentElement // 或者是特定的滚动容器选择器
})
</script>

<style scoped>
.pagination-container {
  margin-bottom: 10px;
}
</style>
