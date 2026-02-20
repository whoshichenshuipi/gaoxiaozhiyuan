<template>
  <div class="login-page">
    <div class="login-card card">
      <div class="login-header">
        <h2>登录</h2>
        <p class="subtitle">欢迎回到高考志愿服务系统</p>
      </div>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>手机号 / 用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入您的账号" required>
        </div>
        <div class="form-group">
          <label>密码</label>
          <div class="password-box">
            <input v-model="form.password" :type="showPwd ? 'text' : 'password'" placeholder="请输入登录密码" required>
            <span class="pwd-eye" @click="showPwd = !showPwd">{{ showPwd ? '👁️' : '🙈' }}</span>
          </div>
        </div>
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="form.remember"> 记住我
          </label>
          <a href="#" class="forgot-pwd">忘记密码？</a>
        </div>
        <button type="submit" class="btn btn-primary login-btn">立即登录</button>
      </form>
      <div class="login-footer">
        还没有账号？ <a href="#" @click.prevent="goToRegister">立即注册</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'

const router = useRouter()
const showPwd = ref(false)
const form = reactive({
  username: '',
  password: '',
  remember: false
})

const handleLogin = async () => {
  try {
    const res = await request.post('/login', {
      username: form.username,
      password: form.password
    })
    if (res.code === 200) {
      localStorage.setItem('token', res.data.access_token)
      localStorage.setItem('role', res.data.user.role)
      localStorage.setItem('username', res.data.user.username)
      alert('登录成功')
      router.push('/')
    }
  } catch (err) {
    alert(err.response?.data?.msg || '登录失败，请检查账号密码')
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 440px;
  padding: 48px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h2 {
  color: var(--primary-color);
  font-size: 24px;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
}

.form-group input[type="text"],
.form-group input[type="password"] {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  outline: none;
}

.password-box {
  position: relative;
}

.pwd-eye {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.remember-me {
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.forgot-pwd {
  font-size: 13px;
  color: #666;
}

.login-btn {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
}

.login-footer {
  margin-top: 32px;
  text-align: center;
  color: #666;
}
</style>
