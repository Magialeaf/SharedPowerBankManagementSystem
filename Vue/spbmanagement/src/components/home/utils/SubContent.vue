<template>
  <div class="sub-content">
    <div class="img-box">
      <img class="img avatar" :src="avatarUrl" alt="" />
    </div>
    <div class="text-box">
      <el-form class="form-item" label-position="left" label-width="25%" style="margin-left: 20px">
        <el-form-item v-for="(value, key) in mergedData" :key="key" :label="key">
          <p class="text">{{ value }}</p>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue'
import { useAddressStore } from '@/stores/areaStore'
import { useSPBConfigStore } from '@/stores/SPBStore'

const addressStore = useAddressStore()
const powerBankConfigStore = useSPBConfigStore()

const props = defineProps({
  data: { type: Object },
  tips: { type: Object }
})

const data = computed(() => props.data)
const tips = ref(props.tips)

const avatarUrl = computed(() => {
  return data.value?.avatar ?? data.value?.shop_img ?? data.value?.img ?? ''
})

// 合并数据
const mergedData = computed(() => {
  if (!data.value || !tips.value) return {} // 如果data或tips未定义，则返回空对象

  const result = {}
  for (const key in tips.value) {
    const value = data.value[key]
    if (key === 'area') {
      if (data.value.areaCodeList) {
        const codeList = data.value.areaCodeList
        const nameList = addressStore.codeListToAddrList(codeList)
        const address = nameList.reduce((pre, cur) => pre + cur) + data.value.area_data.slice(7)
        result[tips.value[key] + '：'] = address
      } else {
        result[tips.value[key] + '：'] = ''
      }
    } else if (key == 'electricity_percentage') {
      result[tips.value[key] + '：'] = value + '%' ?? ''
    } else {
      result[tips.value[key] + '：'] = value ?? '' // 使用空值合并运算符处理可能的undefined
    }
  }
  return result
})
</script>

<style coped>
.sub-content {
  width: 100%;
  min-height: 400px;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: flex-start;
}

.img-box {
  width: 35%;
  height: 299px;
  border: 2px solid #ccc;
  border-radius: 10px;

  /* 添加以下代码以实现蓝色泛光边框效果 */
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.5);
}

.img-box .img {
  width: 100%;
  height: 100%;
  border-radius: 10px;
}

.text-box {
  width: 60%;
  height: 100%;
}

.text {
  width: 100%;
  white-space: normal;
  overflow-wrap: break-word;
}
</style>
