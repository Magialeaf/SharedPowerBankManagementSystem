<template>
  <el-form
    class="form-item"
    label-position="left"
    label-width="20%"
    :model="noticeInfo"
    style="max-width: 600px"
  >
    <el-form-item v-if="!ifNew" label="id">
      <el-input v-model="noticeInfo.id" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item label="标题">
      <el-input v-model="noticeInfo.title" :maxlength="20"></el-input>
    </el-form-item>
    <el-form-item label="内容">
      <el-input
        type="textarea"
        :rows="5"
        placeholder="请输入内容"
        v-model="noticeInfo.content"
        resize="none"
        :maxlength="100"
      ></el-input>
    </el-form-item>
    <el-form-item label="类型">
      <el-select v-model="noticeInfo.type" placeholder="请选择">
        <el-option
          v-for="(label, value) in noticeConfigStore.showList()"
          :key="value"
          :label="label"
          :value="value"
        ></el-option>
      </el-select>
    </el-form-item>
    <el-form-item v-if="!ifNew" label="创建时间">
      <el-input v-model="noticeInfo.create_time" disabled></el-input>
    </el-form-item>
    <el-form-item v-if="!ifNew" label="更新时间">
      <el-input v-model="noticeInfo.update_time" disabled></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="success" @click="onSubmit">{{ ifNew ? '新增日志' : '更新日志' }}</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { onBeforeMount, ref, defineProps, computed } from 'vue'
import { useNoticeConfigStore, useNoticeStore } from '@/stores/noticeStore'
import { lockFunction } from '@/utils/myLock'

const noticeConfigStore = useNoticeConfigStore()
const noticeStore = useNoticeStore()

const noticeInfo = ref({
  id: -1,
  title: '',
  content: '',
  type: '0',
  create_time: null,
  update_time: null
})

const props = defineProps({
  id: {
    type: Number,
    default: -1
  },
  ifNew: {
    type: Boolean,
    default: false
  }
})
const ifNew = ref(props.ifNew)

const onSubmit = lockFunction()(() => {
  let inputData = { ...noticeInfo.value }
  delete inputData.power_bank_name
  delete inputData.user_name
  if (ifNew.value) {
    noticeStore
      .createInfo(inputData)
      .then((res) => {
        // console.log(res)
      })
      .catch((err) => {})
  } else {
    noticeStore
      .updateInfo(props.id, inputData)
      .then((res) => {
        noticeInfo.value = res.data
      })
      .catch((err) => {})
  }
})

onBeforeMount(() => {
  if (!ifNew.value) {
    noticeStore.getInfo(props.id).then((res) => {
      noticeInfo.value = res.data
    })
  }
})
</script>

<style scoped></style>
