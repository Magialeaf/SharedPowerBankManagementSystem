import { defineStore } from 'pinia'
import { reactive, ref } from 'vue'

export const useChangeThemeColorStore = defineStore('changeColor', () => {
  const themeColors = reactive([
    {
      name: '普通灰色',
      color: '#545c64'
    },
    {
      name: '月季红色',
      color: '#ce5777'
    },
    {
      name: '槿紫主题',
      color: '#806d9e'
    },
    {
      name: '品蓝主题',
      color: '#2b73af'
    },
    {
      name: '薄荷绿色',
      color: '#207f4c'
    }
  ])

  const initCurrentColor = () => {
    if (localStorage.getItem('colorIdx'))
      return ref(themeColors[localStorage.getItem('colorIdx')].color)
    else return ref(themeColors[0].color)
  }

  const currentColor = initCurrentColor()

  const getColorList = () => {
    return themeColors
  }

  const getCurrentColor = () => {
    return currentColor.value
  }

  const setCurrentColor = (index) => {
    currentColor.value = themeColors[index].color
    localStorage.setItem('colorIdx', index)
  }

  return { getColorList, getCurrentColor, setCurrentColor }
})
