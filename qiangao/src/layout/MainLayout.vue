<template>
  <div class="layout-wrapper">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <div class="logo-area">
          <div class="logo-box">U</div>
          <h1 v-if="!isCollapsed">高校中台</h1>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <router-link v-for="item in menuItems" :key="item.path" :to="item.path" class="nav-item">
          <component :is="item.icon" class="icon" />
          <span v-if="!isCollapsed">{{ item.title }}</span>
          <div v-if="item.badge" class="badge-dot"></div>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="isCollapsed = !isCollapsed" class="collapse-btn">
          <ChevronLeft v-if="!isCollapsed" />
          <ChevronRight v-else />
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="main-container">
      <header class="top-header">
        <div class="breadcrumb">
          <span>当前页面 / </span>
          <span class="active">{{ currentRouteName }}</span>
        </div>
        
        <div class="header-actions">
          <div class="msg-bell">
            <Bell class="icon" />
            <span class="badge">3</span>
          </div>
          <div class="user-profile">
            <span class="username">{{ username }}</span>
            <div class="avatar">Admin</div>
            <button @click="handleLogout" class="logout-btn">
              <LogOut class="icon-sm" />
            </button>
          </div>
        </div>
      </header>

      <main class="content-view">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  LayoutDashboard, 
  School, 
  FileText, 
  BarChart3, 
  MessageSquare, 
  HelpCircle, 
  Megaphone, 
  AlertCircle,
  ChevronLeft,
  ChevronRight,
  Bell,
  LogOut
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const isCollapsed = ref(false)
const username = localStorage.getItem('username') || '高校管理员'

const menuItems = [
  { title: '仪表盘', path: '/', icon: LayoutDashboard },
  { title: '院校信息', path: '/info', icon: School },
  { title: '招生管理', path: '/admission', icon: FileText },
  { title: '生源看板', path: '/source', icon: BarChart3 },
  { title: '互动咨询', path: '/consultation', icon: MessageSquare, badge: true },
  { title: '问答库', path: '/faq', icon: HelpCircle },
  { title: '校园资讯', path: '/news', icon: Megaphone },
  { title: '问题反馈', path: '/feedback', icon: AlertCircle }
]

const currentRouteName = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item ? item.title : '仪表盘'
})

const handleLogout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.layout-wrapper {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  background: var(--sidebar-bg);
  color: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar.collapsed {
  width: 64px;
}

.sidebar-header {
  padding: 24px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-box {
  width: 32px;
  height: 32px;
  background: white;
  color: var(--sidebar-bg);
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 800;
  flex-shrink: 0;
}

.logo-area h1 {
  font-size: 18px;
  font-weight: 700;
  white-space: nowrap;
}

.sidebar-nav {
  flex: 1;
  padding: 16px 8px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: rgba(255,255,255,0.6);
  border-radius: 8px;
  margin-bottom: 4px;
  transition: all 0.2s;
  position: relative;
}

.nav-item:hover, .nav-item.router-link-active {
  color: white;
  background: rgba(255,255,255,0.1);
}

.nav-item.router-link-active .icon {
  color: white;
}

.nav-item span {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.badge-dot {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 8px;
  height: 8px;
  background: #f44336;
  border-radius: 50%;
  border: 2px solid var(--sidebar-bg);
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255,255,255,0.05);
}

.collapse-btn {
  width: 100%;
  background: transparent;
  border: none;
  color: rgba(255,255,255,0.5);
  cursor: pointer;
  display: flex;
  justify-content: center;
  padding: 8px;
}

.collapse-btn:hover { color: white; }

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-color);
  overflow: hidden;
}

.top-header {
  height: 64px;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
  z-index: 10;
}

.breadcrumb {
  font-size: 14px;
  color: #64748b;
}

.breadcrumb .active {
  color: #1e293b;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.msg-bell {
  position: relative;
  cursor: pointer;
  color: #64748b;
}

.msg-bell .badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #f44336;
  color: white;
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 10px;
  border: 2px solid white;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.avatar {
  width: 36px;
  height: 36px;
  background: #e2e8f0;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 10px;
  font-weight: bold;
  color: #64748b;
}

.logout-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
}

.logout-btn:hover { color: #f44336; }

.content-view {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* Transitions */
.fade-transform-enter-active, .fade-transform-leave-active {
  transition: all 0.3s;
}
.fade-transform-enter-from { opacity: 0; transform: translateX(-10px); }
.fade-transform-leave-to { opacity: 0; transform: translateX(10px); }
</style>
