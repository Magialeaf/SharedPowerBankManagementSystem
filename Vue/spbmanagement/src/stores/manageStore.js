import { defineStore } from 'pinia'
import { ref, markRaw, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useJwtTokenStore } from './authenticationStore'
import { useChangeThemeColorStore } from '@/stores/themeColor.js'
import IconHome from '@/components/icons/IconHome.vue'
import IconCommunity from '@/components/icons/IconCommunity.vue'
import IconArea from '@/components/icons/IconArea.vue'
import IconAreaInfo from '@/components/icons/IconAreaInfo.vue'
import IconColor from '@/components/icons/IconColor.vue'
import IconIdentity from '@/components/icons/IconIdentity.vue'
import IconPerson from '@/components/icons/IconPerson.vue'
import IconMyInfo from '@/components/icons/IconMyInfo.vue'

export const useManageMainStore = defineStore('manageMainStore', () => {
  const jwtTokenStore = useJwtTokenStore()
  const identity = computed(() => {
    return jwtTokenStore.identity
  })

  const items = ref([
    {
      id: '1',
      text: '首页',
      iconName: markRaw(IconHome),
      router: '/management/manage-home',
      subMenu: null
    },
    {
      id: '2',
      text: '个人中心',
      iconName: markRaw(IconPerson),
      router: '2',
      subMenu: [
        {
          id: '2-1',
          text: '我的信息',
          iconName: markRaw(IconMyInfo),
          router: '/management/my-info',
          subMenu: null
        }
      ]
    },
    {
      id: '3',
      text: '用户管理',
      iconName: markRaw(IconCommunity),
      router: '3',
      subMenu: [
        // {
        //   id: '3-1',
        //   text: '管理员管理',
        //   iconName: markRaw(IconCommunity),
        //   router: '/management/manage-admin',
        //   subMenu: null
        // },
        {
          id: '3-2',
          text: '维护人员管理',
          iconName: markRaw(IconCommunity),
          router: '/management/manage-maintainer',
          subMenu: null
        },
        {
          id: '3-3',
          text: '用户管理',
          iconName: markRaw(IconCommunity),
          router: '/management/manage-user',
          subMenu: null
        }
      ]
    },
    {
      id: '4',
      text: '区域管理',
      iconName: markRaw(IconArea),
      router: '4',
      subMenu: [
        {
          id: '4-1',
          text: '区域信息',
          iconName: markRaw(IconAreaInfo),
          router: '/management/manage-area',
          subMenu: null
        }
      ]
    },
    {
      id: '5',
      text: '商户管理',
      iconName: markRaw(IconCommunity),
      router: '5',
      subMenu: [
        {
          id: '5-1',
          text: '合作商户',
          iconName: markRaw(IconCommunity),
          router: '/management/manage-merchant',
          subMenu: null
        }
      ]
    },
    {
      id: '6',
      text: '充电宝管理',
      iconName: markRaw(IconCommunity),
      router: '6',
      subMenu: [
        {
          id: '6-1',
          text: '充电宝投放管理',
          iconName: markRaw(IconCommunity),
          router: '/management/power-bank-release',
          subMenu: null
        },
        {
          id: '6-2',
          text: '充电宝维护管理',
          iconName: markRaw(IconCommunity),
          router: '/management/power-bank-maintenance',
          subMenu: null
        }
      ]
    },
    {
      id: '7',
      text: '订单管理',
      iconName: markRaw(IconCommunity),
      router: '7',
      subMenu: [
        {
          id: '7-1',
          text: '租赁订单',
          iconName: markRaw(IconCommunity),
          router: '/management/rental-order',
          subMenu: null
        },
        {
          id: '7-2',
          text: '归还订单',
          iconName: markRaw(IconCommunity),
          router: '/management/return-order',
          subMenu: null
        },
        {
          id: '7-3',
          text: '费用订单',
          iconName: markRaw(IconCommunity),
          router: '/management/fee-order',
          subMenu: null
        }
      ]
    },
    {
      id: '8',
      text: '系统管理',
      iconName: markRaw(IconCommunity),
      router: '8',
      subMenu: [
        {
          id: '8-1',
          text: '公告栏',
          iconName: markRaw(IconCommunity),
          router: '/management/manage-notice',
          subMenu: null
        }
      ]
    }
  ])

  const getItems = () => {
    return items
  }

  return { getItems }
})

export const useManageHeaderStore = defineStore('manageHeaderStore', () => {
  const jwtTokenStore = useJwtTokenStore()
  const identity = computed(() => {
    return jwtTokenStore.getIdentity()
  })

  const changeThemeColor = useChangeThemeColorStore()
  const router = useRouter()
  const colorMenu = []

  const items = ref([
    {
      id: '1',
      name: '首页',
      router: '/management/manage-home',
      iconName: markRaw(IconHome),
      function: () => {
        router.push('/management/manage-home')
      },
      subMenu: null
    },
    {
      id: '2',
      name: '切换皮肤',
      router: '2',
      iconName: markRaw(IconColor),
      subMenu: colorMenu
    },
    {
      id: '3',
      name: identity,
      router: '3',
      iconName: markRaw(IconIdentity),
      subMenu: [
        {
          id: '3-1',
          name: '返回首页',
          function: () => home()
        },
        {
          id: '3-2',
          name: '退出登录',
          function: () => exit()
        }
      ]
    }
  ])

  const colorList = changeThemeColor.getColorList()
  for (let i = 0; i < colorList.length; i++) {
    const { name, color } = colorList[i]
    colorMenu.push({
      id: '2-' + String(i + 1),
      name,
      function: () => changeThemeColor.setCurrentColor(i)
    })
  }

  function home() {
    router.push('/')
  }

  function exit() {
    sessionStorage.clear()
    localStorage.clear()
    // clearAllCookie()
    router.push('/enter/')
  }

  //   function clearAllCookie() {
  //     console.log(1)
  //     var keys = document.cookie.match(/[^ =;]+(?=\=)/g)
  //     console.log(keys)
  //     if (keys) {
  //       for (var i = keys.length; i--; )
  //         document.cookie = keys[i] + '=0;expires=' + new Date(0).toUTCString()
  //     }
  //   }

  const getItems = () => {
    return items
  }

  return { getItems }
})
