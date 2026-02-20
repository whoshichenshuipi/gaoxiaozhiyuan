<template>
  <div class="login-container">
    <div class="login-card">
      <h1>高考服务系统</h1>
      <p class="subtitle">管理后台登录</p>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="form.username" 
            type="text" 
            placeholder="请输入管理员账号" 
            required
          >
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码" 
            required
          >
        </div>
        <div class="form-group captcha-group">
          <label>验证码</label>
          <div class="captcha-input-wrapper">
            <input 
              v-model="form.captcha" 
              type="text" 
              placeholder="4位验证码" 
              required
            >
            <div class="captcha-img">M F 2 K</div>
          </div>
        </div>
        <button :disabled="loading" type="submit" class="login-btn">
          {{ loading ? '登录中...' : '立即登录' }}
        </button>
      </form>
      <p class="footer-tip">密码错误 3 次将锁定 10 分钟</p>
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
  captcha: 'MF2K' // Mocked captcha for now
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
      localStorage.setItem('role', res.data.user.role)
      localStorage.setItem('username', res.data.user.username)
      if (res.data.user.role !== 'admin') {
        alert('抱歉，该账号没有管理后台访问权限')
        localStorage.clear()
        return
      }
      alert('登录成功')
      router.push('/')
    }
  } catch (err) {
    alert(err.response?.data?.msg || '登录失败，请检查账号密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--sidebar-bg);
}

.login-card {
  width: 400px;
  background: white;
  padding: 48px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  text-align: center;
}

.login-card h1 {
  font-size: 28px;
  margin-bottom: 8px;
  color: var(--primary-color);
}

.subtitle {
  color: #666;
  margin-bottom: 40px;
}

.login-form {
  text-align: left;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
}

.captcha-input-wrapper {
  display: flex;
  gap: 12px;
}

.captcha-img {
  flex: 1;
  background: #eee;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  letter-spacing: 4px;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
}

.login-btn {
  width: 100%;
  background: var(--primary-color);
  color: white;
  padding: 14px;
  border-radius: 4px;
  font-weight: 600;
  margin-top: 12px;
}

.footer-tip {
  margin-top: 24px;
  font-size: 12px;
  color: #999;
}
</style>
