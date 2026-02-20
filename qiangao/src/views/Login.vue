<template>
  <div class="login-page">
    <div class="login-card card">
      <div class="login-header">
        <div class="logo-circle">U</div>
        <h2>院校端业务中台</h2>
        <p>专业 · 高效 · 数字化</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label class="form-label">用户名</label>
          <input v-model="form.username" type="text" class="form-control" placeholder="请输入管理员账号" required>
        </div>
        <div class="form-group">
          <label class="form-label">密码</label>
          <input v-model="form.password" type="password" class="form-control" placeholder="请输入密码" required>
        </div>
        
        <div class="extra-actions">
          <label class="remember-me">
            <input type="checkbox" v-model="form.remember"> 记住我
          </label>
          <router-link to="/register" class="reg-link">提交入驻申请</router-link>
        </div>

        <button :disabled="loading" type="submit" class="btn btn-primary login-btn">
          {{ loading ? '登录中...' : '立即登录' }}
        </button>
      </form>

      <div class="login-footer">
        <p>© 2024 高考志愿填报服务系统 · 院校中心</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await request.post('/login', {
      username: form.username,
      password: form.password
    })
    
    if (res.code === 200) {
      localStorage.setItem('token', res.data.access_token)
      localStorage.setItem('username', res.data.user.username)
      localStorage.setItem('role', res.data.user.role)
      
      if (res.data.user.role !== 'university') {
        alert('该账号不是高校管理员账号')
        localStorage.clear()
        return
      }
      
      router.push('/')
    }
  } catch (err) {
    alert(err.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #F5F7FA 0%, #E4E7EB 100%);
}

.login-card {
  width: 420px;
  padding: 40px;
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-circle {
  width: 48px;
  height: 48px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: 800;
  margin: 0 auto 16px;
}

.login-header h2 {
  font-size: 22px;
  color: #1a237e;
  margin-bottom: 4px;
}

.login-header p {
  font-size: 13px;
  color: #64748b;
  letter-spacing: 2px;
}

.extra-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  margin-bottom: 24px;
}

.reg-link {
  font-weight: 600;
  color: var(--primary-color);
}

.login-btn {
  width: 100%;
  padding: 12px;
  font-size: 15px;
}

.login-footer {
  margin-top: 40px;
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
}
</style>
