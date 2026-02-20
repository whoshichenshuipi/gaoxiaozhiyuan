<template>
  <div class="user-layout">
    <!-- Navbar: White Clean Style -->
    <header class="navbar container-full">
      <div class="nav-brand">
        <div class="brand-icon">高</div>
        <span class="brand-name">高考志愿规划师</span>
      </div>
      
      <nav class="nav-links">
        <router-link to="/" class="nav-link" exact-active-class="active">首页</router-link>
        <router-link to="/search" class="nav-link" active-class="active">查院校</router-link>
        <router-link to="/recommend" class="nav-link" active-class="active">智能推荐</router-link>
        <router-link to="/community" class="nav-link" active-class="active">社区</router-link>
      </nav>

      <div class="nav-actions">
        <div class="user-profile" @click="toggleMenu">
          <span class="username">{{ username }}</span>
          <div class="avatar">👤</div>
          <div v-if="showMenu" class="dropdown-menu">
            <div class="dropdown-item" @click="$router.push('/profile')">🔗 个人画像</div>
            <div class="dropdown-item" @click="$router.push('/volunteer')">📋 志愿表管理</div>
            <div class="divider"></div>
            <div class="dropdown-item logout" @click="logout">🚪 退出登录</div>
          </div>
        </div>
      </div>
    </header>

    <main class="page-content container-full">
      <router-view></router-view>
    </main>

    <footer class="footer">
      <div class="container-full">
        <p>© 2024 高考志愿规划师 / 专业、信任、透明的决策支持系统</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showMenu = ref(false)
const username = ref('用户')

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const logout = () => {
  if (confirm('确定退出登录吗？')) {
    localStorage.clear()
    router.push('/login')
  }
}

onMounted(() => {
  username.value = localStorage.getItem('username') || '张同学'
})
</script>

<style scoped>
.user-layout {
  min-height: 100vh;
  background-color: var(--bg-color);
  display: flex;
  flex-direction: column;
}

.navbar {
  height: 80px;
  background: white;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 40px;
  height: 40px;
  background: var(--primary-color);
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
}

.brand-name {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--text-color);
}

.nav-links {
  display: flex;
  gap: 32px;
}

.nav-link {
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all 0.3s;
  padding: 8px 0;
  position: relative;
}

.nav-link:hover, .nav-link.active {
  color: var(--primary-color);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary-color);
}

.nav-actions {
  display: flex;
  align-items: center;
}

.user-profile {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 12px;
  transition: background 0.2s;
}

.user-profile:hover {
  background: #f1f5f9;
}

.username {
  font-weight: 600;
  font-size: 14px;
}

.avatar {
  width: 36px;
  height: 36px;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
}

.dropdown-menu {
  position: absolute;
  top: 50px;
  right: 0;
  width: 180px;
  background: white;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  padding: 8px;
  z-index: 1100;
}

.dropdown-item {
  padding: 10px 16px;
  font-size: 14px;
  color: var(--text-color);
  border-radius: 8px;
  transition: background 0.2s;
}

.dropdown-item:hover {
  background: #f1f5f9;
}

.divider {
  height: 1px;
  background: var(--border-color);
  margin: 8px;
}

.logout {
  color: #ef4444;
}

.page-content {
  flex: 1;
  padding-top: 48px;
  padding-bottom: 80px;
}

.footer {
  padding: 40px 0;
  background: white;
  border-top: 1px solid var(--border-color);
  text-align: center;
  font-size: 13px;
  color: var(--text-secondary);
}
</style>
