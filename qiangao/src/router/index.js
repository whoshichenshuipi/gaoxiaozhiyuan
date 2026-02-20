import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue'),
        meta: { public: true }
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue'),
        meta: { public: true }
    },
    {
        path: '/',
        component: () => import('../layout/MainLayout.vue'),
        children: [
            {
                path: '',
                name: 'Dashboard',
                component: () => import('../views/Dashboard.vue')
            },
            {
                path: 'info',
                name: 'UniInfo',
                component: () => import('../views/InfoManagement.vue')
            },
            {
                path: 'admission',
                name: 'Admission',
                component: () => import('../views/AdmissionManagement.vue')
            },
            {
                path: 'source',
                name: 'SourceAnalysis',
                component: () => import('../views/SourceAnalysis.vue')
            },
            {
                path: 'consultation',
                name: 'Consultation',
                component: () => import('../views/Consultation.vue')
            },
            {
                path: 'faq',
                name: 'FAQ',
                component: () => import('../views/FAQManagement.vue')
            },
            {
                path: 'news',
                name: 'News',
                component: () => import('../views/NewsManagement.vue')
            },
            {
                path: 'feedback',
                name: 'Feedback',
                component: () => import('../views/Feedback.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    if (!to.meta.public && !token) {
        next('/login')
    } else {
        next()
    }
})

export default router
