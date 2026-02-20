<template>
  <div class="register-page">
    <div class="register-card card">
      <div class="register-header">
        <h2>注册新账号</h2>
        <p class="subtitle">加入高考志愿规划师，开启名校之旅</p>
      </div>
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请设置您的用户名" required>
        </div>
        <div class="form-group">
          <label>设置密码</label>
          <input v-model="form.password" type="password" placeholder="请输入 6-18 位密码" required>
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" required>
        </div>
        <button type="submit" class="btn btn-primary register-btn" :disabled="loading">
          {{ loading ? '注册中...' : '立即注册' }}
        </button>
      </form>
      <div class="register-footer">
        已有账号？ <a href="#" @click.prevent="$router.push('/login')">立即登录</a>
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
  confirmPassword: ''
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    return alert('两次输入的密码不一致')
  }
  if (form.password.length < 6) {
    return alert('密码长度不能少于 6 位')
  }

  loading.value = true
  try {
    const res = await request.post('/register', {
      username: form.username,
      password: form.password,
      role: 'student'
    })
    if (res.code === 200) {
      alert('注册成功，请使用新账号登录')
      router.push('/login')
    }
  } catch (err) {
    alert(err.response?.data?.msg || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  height: 100vh;
  background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 440px;
  padding: 48px;
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-header h2 {
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

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  outline: none;
}

.register-btn {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
}

.register-footer {
  margin-top: 32px;
  text-align: center;
  color: #666;
}
</style>
