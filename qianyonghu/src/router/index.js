import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/login',
        name: '登录',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/register',
        name: '注册',
        component: () => import('../views/Register.vue')
    },
    {
        path: '/',
        component: () => import('../layout/UserLayout.vue'),
        children: [
            {
                path: '',
                name: '首页',
                component: () => import('../views/Home.vue')
            },
            {
                path: 'profile',
                name: '个人画像',
                component: () => import('../views/Profile.vue')
            },
            {
                path: 'search',
                name: '院校查询',
                component: () => import('../views/Search.vue')
            },
            {
                path: 'uni/:id',
                name: '院校详情',
                component: () => import('../views/UniDetail.vue')
            },
            {
                path: 'recommend',
                name: '志愿推荐',
                component: () => import('../views/Recommend.vue')
            },
            {
                path: 'volunteer',
                name: '方案管理',
                component: () => import('../views/Volunteer.vue')
            },
            {
                path: 'community',
                name: '交流社区',
                component: () => import('../views/Community.vue')
            },
            {
                path: 'chat',
                name: '智能咨询',
                component: () => import('../views/Chat.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Basic Auth Guard Simulation
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (to.path !== '/login' && to.path !== '/register' && !token) {
        next('/login')
    } else {
        next()
    }
})

export default router
