import { createRouter, createWebHistory } from 'vue-router'

import MemoListPage from '../pages/MemoListPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/memos',
  },
  {
    path: '/memos',
    name: 'MemoListPage',
    component: MemoListPage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
