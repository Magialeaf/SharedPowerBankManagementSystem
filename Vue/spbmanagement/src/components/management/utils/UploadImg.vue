<template>
  <el-upload
    ref="uploadImg"
    class="img-uploader"
    :http-request="uploadImgFunc"
    :show-file-list="false"
    :auto-upload="false"
    v-model:file-list="fileList"
    :action="null"
    :on-change="handleImgChange"
  >
    <img v-if="url !== ''" :src="url" class="img" />
    <el-icon v-else class="img-uploader-icon"><Plus /></el-icon>
  </el-upload>
</template>
<script setup>
import { computed, ref, watch, onBeforeMount } from 'vue'
import { $errorMsg } from '@/utils/msg'
import { Plus } from '@element-plus/icons-vue'

const uploadImg = ref()
const fileList = ref([])

const props = defineProps({
  imgUrl: {
    type: String,
    required: true
  },
  ifUpload: {
    type: Boolean,
    required: true
  },
  uploadFunc: {
    type: Function,
    required: true
  }
})

const url = computed(() => props.imgUrl)
const ifUploadValue = computed(() => props.ifUpload)

const emits = defineEmits(['updateImgUrl', 'updateIfUpload', 'uploadSuccess'])

const handleImgChange = (rawFile, rawFileList) => {
  if (!/\.(jpg|jpeg|png|gif|bmp)$/i.test(rawFile.name)) {
    $errorMsg('上传图片只能是 JPG, JPEG, PNG, GIF 或 BMP 格式!')
    emits('updateImgUrl', '')
    fileList.value = []
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    $errorMsg('上传图片大小不能超过 2MB!')
    emits('updateImgUrl', '')
    fileList.value = []
    return false
  } else {
    if (rawFile.raw instanceof File) {
      // 添加类型判断
      emits('updateImgUrl', URL.createObjectURL(rawFile.raw))
    }
    return false
  }
}

// 部署流程定义（点击按钮，上传bpmn文件，上传成功后部署，然后重新加载列表）
function uploadImgFunc(param) {
  const formData = new FormData()
  formData.append('file', param.file)
  props
    .uploadFunc(formData)
    .then((res) => {
      emits('uploadSuccess', res)
    })
    .catch((e) => {})
}

watch(fileList, (newValue, oldValue) => {
  if (fileList.value.length > 1) fileList.value.splice(0, fileList.value.length - 1)
})

watch(ifUploadValue, (newValue, oldValue) => {
  if (newValue) {
    emits('updateIfUpload', false)
    if (url.value && fileList.value.length == 0) {
      emits('uploadSuccess', { data: {} })
    } else if (fileList.value.length == 0) $errorMsg('请上传图片')
    else uploadImg.value.submit()
  }
})
</script>

<style scoped>
.img-uploader .img {
  width: 180px;
  height: 180px;
  display: block;
}
</style>

<style>
.img-uploader .el-upload {
  border: 2px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.img-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.img-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
