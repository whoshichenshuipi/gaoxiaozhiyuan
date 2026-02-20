<template>
  <div class="admin-layout">
    <!-- Sidebar: Premium Dark Style -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed }">
      <div class="sidebar-header">
        <div class="logo">G</div>
        <span v-if="!isCollapsed" class="brand-name">GK ADMIN</span>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <span class="icon">📊</span>
          <span v-if="!isCollapsed">控制面板</span>
        </router-link>
        <router-link to="/users" class="nav-item" active-class="active">
          <span class="icon">👥</span>
          <span v-if="!isCollapsed">用户审计</span>
        </router-link>
        <router-link to="/data" class="nav-item" active-class="active">
          <span class="icon">🏫</span>
          <span v-if="!isCollapsed">院校数据</span>
        </router-link>
        <div class="divider" v-if="!isCollapsed">AUDIT SYSTEM</div>
        <router-link to="/rag" class="nav-item" active-class="active">
          <span class="icon">🤖</span>
          <span v-if="!isCollapsed">RAG 审核</span>
        </router-link>
        <router-link to="/community" class="nav-item" active-class="active">
          <span class="icon">🗨️</span>
          <span v-if="!isCollapsed">社区管理</span>
        </router-link>
        <router-link to="/feedback" class="nav-item" active-class="active">
          <span class="icon">📝</span>
          <span v-if="!isCollapsed">用户反馈</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="version-tag" v-if="!isCollapsed">V2.1.0 Stable</div>
        <button class="collapse-btn" @click="isCollapsed = !isCollapsed">
          {{ isCollapsed ? '▶' : '◀' }}
        </button>
      </div>
    </aside>

    <div class="main-wrapper">
      <header class="top-nav">
        <div class="breadcrumb">
          <span>Admin</span> / <span class="active">{{ $route.name || 'Dashboard' }}</span>
        </div>
        <div class="user-actions">
          <div class="notif">🔔</div>
          <div class="user-badge">
            <div class="avatar-sm">AD</div>
            <span class="role">Super Admin</span>
          </div>
        </div>
      </header>

      <main class="content-area">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isCollapsed = ref(false)
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  background: var(--bg-dark);
}

.sidebar {
  width: 280px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.sidebar.collapsed {
  width: 80px;
}

.sidebar-header {
  padding: 32px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  box-shadow: var(--glow-blue);
  flex-shrink: 0;
}

.brand-name {
  font-size: 18px;
  font-weight: 800;
  letter-spacing: 1px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
  color: var(--text-muted);
  text-decoration: none;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s;
}

.nav-item:hover {
  background: rgba(255,255,255,0.03);
  color: white;
}

.nav-item.active {
  background: rgba(37, 99, 235, 0.1);
  color: var(--primary-color);
  border: 1px solid rgba(37, 99, 235, 0.2);
}

.divider {
  font-size: 10px;
  color: #475569;
  letter-spacing: 0.2em;
  font-weight: 800;
  margin: 24px 20px 8px;
}

.sidebar-footer {
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
}

.version-tag {
  font-size: 10px;
  color: #334155;
  font-weight: bold;
}

.collapse-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 10px;
}

.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-nav {
  height: 80px;
  padding: 0 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.breadcrumb {
  font-size: 14px;
  color: var(--text-muted);
  font-weight: 500;
}

.breadcrumb .active {
  color: white;
  font-weight: 700;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.notif {
  font-size: 18px;
  color: var(--text-muted);
  cursor: pointer;
}

.user-badge {
  background: rgba(255,255,255,0.03);
  padding: 6px 16px 6px 6px;
  border-radius: 14px;
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-sm {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 10px;
  font-weight: bold;
}

.role {
  font-size: 12px;
  font-weight: 600;
}

.content-area {
  flex: 1;
  padding: 0 40px 40px;
  overflow-y: auto;
}
</style>
