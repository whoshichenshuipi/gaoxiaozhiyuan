import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/login',
        name: '登录',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/',
        component: () => import('../layout/MainLayout.vue'),
        children: [
            {
                path: '',
                name: '仪表盘',
                component: () => import('../views/Dashboard.vue')
            },
            {
                path: 'users',
                name: '用户管理',
                component: () => import('../views/UserManagement.vue')
            },
            {
                path: 'data',
                name: '数据中心',
                component: () => import('../views/DataManagement.vue')
            },
            {
                path: 'community',
                name: '社区审核',
                component: () => import('../views/CommunityManagement.vue')
            },
            {
                path: 'rag',
                name: 'RAG 审核',
                component: () => import('../views/RAGAudit.vue')
            },
            {
                path: 'feedback',
                name: '反馈处理',
                component: () => import('../views/FeedbackManagement.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (to.path !== '/login' && !token) {
        // 演示环境下暂不强制拦截，方便预览
        // next('/login')
        next()
    } else {
        next()
    }
})

export default router
