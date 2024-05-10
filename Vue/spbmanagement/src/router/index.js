import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/Home.vue'

const routes = [
  {
    path: '/',
    name: '/',
    redirect: '/home',
    meta: { requiresAuth: true },
    component: HomeView,
    children: [
      {
        path: '/home',
        name: 'home',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/header/Home.vue')
      },
      {
        path: '/partner',
        name: 'partner',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/header/Partner.vue')
      },
      {
        path: '/partner/:id', // 动态路由参数
        name: 'partner-id',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/partner/PartnerHome.vue')
      },
      {
        path: '/product',
        name: 'product',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/header/Product.vue')
      },
      {
        path: '/product/:id',
        name: 'product-id',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/product/ProductHome.vue')
      },
      {
        path: '/notice',
        name: 'notice',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/header/Notice.vue')
      },
      {
        path: '/notice/:id',
        name: 'notice-id',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/notice/NoticeHome.vue')
      },
      {
        path: '/user',
        name: 'user',
        meta: { requiresAuth: true },
        component: () => import('@/components/home/header/User.vue')
      }
    ]
  },
  {
    path: '/enter',
    name: 'enter',
    meta: { requiresAuth: false },
    component: () => import('@/views/Enter.vue')
  },
  {
    path: '/management',
    name: 'management',
    redirect: '/management/manage-home',
    meta: { requiresAuth: true },
    component: () => import('@/views/Management.vue'),
    children: [
      {
        path: 'manage-home',
        name: 'manage-home',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageHome.vue')
      },
      {
        path: 'my-info',
        name: 'my-info',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageMyInfo.vue')
      },
      {
        path: 'manage-admin',
        name: 'manage-admin',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageAdmin.vue')
      },
      {
        path: 'manage-maintainer',
        name: 'manage-maintainer',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageMaintainer.vue')
      },
      {
        path: 'manage-user',
        name: 'manage-user',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageUser.vue')
      },
      {
        path: 'manage-area',
        name: 'manage-area',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageArea.vue')
      },
      {
        path: 'manage-merchant',
        name: 'manage-merchant',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ManageMerchant.vue')
      },
      {
        path: 'power-bank-release',
        name: 'power-bank-release',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/PowerBankRelease.vue')
      },
      {
        path: 'power-bank-maintenance',
        name: 'power-bank-maintenance',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/PowerBankMaintenance.vue')
      },
      {
        path: 'rental-order',
        name: 'rental-order',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/RentalOrder.vue')
      },
      {
        path: 'return-order',
        name: 'return-order',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/ReturnOrder.vue')
      },
      {
        path: 'fee-order',
        name: 'fee-order',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/FeeOrder.vue')
      },
      {
        path: 'manage-notice',
        name: 'manage-notice',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/Notice.vue')
      },
      {
        path: 'manage-carousel-chart',
        name: 'manage-carousel-chart',
        meta: { requiresAuth: true },
        component: () => import('@/components/management/aside/CarouselChart.vue')
      }
    ]
  },
  {
    path: '/404',
    name: 'notFound',
    meta: { requiresAuth: true },
    component: () => import('@/views/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 顶端加载条
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

router.beforeEach((to, from, next) => {
  // 检查目标路由是否存在
  const matchedRoutes = to.matched
  if (matchedRoutes.length <= 0) {
    next('/404')
  }
  // 不需要权限校验的路由，直接放行
  else next()
})

router.afterEach((to, from) => {
  NProgress.done()
})

export default router
