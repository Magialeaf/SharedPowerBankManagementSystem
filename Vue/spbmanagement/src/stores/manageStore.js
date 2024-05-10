import { defineStore } from 'pinia'
import { ref, markRaw, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useJwtTokenStore, useIdentityStore } from './authenticationStore'
import { useChangeThemeColorStore } from '@/stores/themeColor.js'
import { icons } from '@/components/icons/iconsLoader'

export const useManageMainStore = defineStore('manageMainStore', () => {
  const jwtTokenStore = useJwtTokenStore()
  const identityStore = useIdentityStore()
  const identityCode = computed(() => jwtTokenStore.getIdentityCode())

  const items = ref([
    {
      id: '1',
      text: '首页',
      iconName: markRaw(icons.IconHome),
      router: '/management/manage-home',
      subMenu: null
    },
    {
      id: '2',
      text: '个人中心',
      iconName: markRaw(icons.IconPerson),
      router: '2',
      subMenu: [
        {
          id: '2-1',
          text: '我的信息',
          iconName: markRaw(icons.IconMyInfo),
          router: '/management/my-info',
          subMenu: null
        }
      ]
    },
    {
      id: '3',
      text: '用户管理',
      iconName: markRaw(icons.IconManageUser),
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
          iconName: markRaw(icons.IconMaintenance),
          router: '/management/manage-maintainer',
          subMenu: null
        },
        {
          id: '3-3',
          text: '用户管理',
          iconName: markRaw(icons.IconUser),
          router: '/management/manage-user',
          subMenu: null
        }
      ]
    },
    {
      id: '4',
      text: '区域管理',
      iconName: markRaw(icons.IconArea),
      router: '4',
      subMenu: [
        {
          id: '4-1',
          text: '区域信息',
          iconName: markRaw(icons.IconAreaInfo),
          router: '/management/manage-area',
          subMenu: null
        }
      ]
    },
    {
      id: '5',
      text: '商户管理',
      iconName: markRaw(icons.IconMerchant),
      router: '5',
      subMenu: [
        {
          id: '5-1',
          text: '合作商户',
          iconName: markRaw(icons.IconMerchantInfo),
          router: '/management/manage-merchant',
          subMenu: null
        }
      ]
    },
    {
      id: '6',
      text: '充电宝管理',
      iconName: markRaw(icons.IconPowerBank),
      router: '6',
      subMenu: [
        {
          id: '6-1',
          text: '充电宝投放管理',
          iconName: markRaw(icons.IconSPBRelease),
          router: '/management/power-bank-release',
          subMenu: null
        },
        {
          id: '6-2',
          text: '充电宝维护管理',
          iconName: markRaw(icons.IconSPBMaintenance),
          router: '/management/power-bank-maintenance',
          subMenu: null
        }
      ]
    },
    {
      id: '7',
      text: '订单管理',
      iconName: markRaw(icons.IconOrder),
      router: '7',
      subMenu: [
        {
          id: '7-1',
          text: '租赁订单',
          iconName: markRaw(icons.IconOrderRental),
          router: '/management/rental-order',
          subMenu: null
        },
        {
          id: '7-2',
          text: '归还订单',
          iconName: markRaw(icons.IconOrderReturn),
          router: '/management/return-order',
          subMenu: null
        },
        {
          id: '7-3',
          text: '费用订单',
          iconName: markRaw(icons.IconOrderFee),
          router: '/management/fee-order',
          subMenu: null
        }
      ]
    },
    {
      id: '8',
      text: '系统管理',
      iconName: markRaw(icons.IconSystem),
      router: '8',
      subMenu: [
        {
          id: '8-1',
          text: '公告栏',
          iconName: markRaw(icons.IconNotice),
          router: '/management/manage-notice',
          subMenu: null
        },
        {
          id: '8-2',
          text: '轮播图',
          iconName: markRaw(icons.IconCarouselChart),
          router: '/management/manage-carousel-chart',
          subMenu: null
        }
      ]
    }
  ])

  const filteredItems = computed(() => {
    switch (identityCode.value) {
      case identityStore.SuperAdmin:
        return items.value
      case identityStore.Admin:
        return items.value
      case identityStore.User:
        return items.value.filter((item) => item.id === '1' || item.id === '2' || item.id === '7')
      case identityStore.Maintainer:
        return items.value.filter(
          (item) => item.id === '1' || item.id === '2' || item.id === '6' || item.id === '7'
        )
      default:
        return []
    }
  })

  const getItems = () => {
    return filteredItems
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
      iconName: markRaw(icons.IconHome),
      function: () => {
        router.push('/management/manage-home')
      },
      subMenu: null
    },
    {
      id: '2',
      name: '切换皮肤',
      router: '2',
      iconName: markRaw(icons.IconColor),
      subMenu: colorMenu
    },
    {
      id: '3',
      name: identity,
      router: '3',
      iconName: markRaw(icons.IconIdentity),
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
