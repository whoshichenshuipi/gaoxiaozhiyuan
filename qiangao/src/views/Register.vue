<template>
  <div class="reg-container">
    <div class="reg-card card">
      <div class="reg-header">
        <h1>高校入驻申请</h1>
        <p class="subtitle">共两步，完成后等待系统审核</p>
      </div>

      <div class="steps-indicator">
        <div :class="['step', { active: currentStep === 1, completed: currentStep > 1 }]">
          <span class="step-num">1</span>
          <span class="step-text">账号设置</span>
        </div>
        <div class="step-line"></div>
        <div :class="['step', { active: currentStep === 2, completed: currentStep > 2 }]">
          <span class="step-num">2</span>
          <span class="step-text">高校认证</span>
        </div>
      </div>

      <form @submit.prevent="handleNext" class="reg-form">
        <!-- Step 1: Base Info -->
        <div v-if="currentStep === 1" class="step-content">
          <div class="form-group">
            <label class="form-label">用户名 (登录账号)</label>
            <input v-model="form.username" type="text" class="form-control" placeholder="建议使用官方邮箱或手机号" required>
          </div>
          <div class="form-group">
            <label class="form-label">设置密码</label>
            <input v-model="form.password" type="password" class="form-control" placeholder="至少8位，含字母与数字" required>
          </div>
          <div class="form-group">
            <label class="form-label">确认密码</label>
            <input v-model="form.confirmPassword" type="password" class="form-control" placeholder="请再次输入密码" required>
          </div>
          <div class="actions">
            <button type="submit" class="btn btn-primary full-width">下一步</button>
          </div>
        </div>

        <!-- Step 2: University Details -->
        <div v-else-if="currentStep === 2" class="step-content">
          <div class="form-group">
            <label class="form-label">入驻高校名称</label>
            <select v-model="form.university_name" class="form-control" required>
              <option value="" disabled>请选择院校</option>
              <option v-for="u in universityList" :key="u" :value="u">{{ u }}</option>
            </select>
            <p class="tip">仅限系统预设的高校入驻</p>
          </div>
          <div class="form-group">
            <label class="form-label">联系人姓名</label>
            <input v-model="form.contact" type="text" class="form-control" placeholder="负责对接的老师姓名" required>
          </div>
          <div class="form-group">
            <label class="form-label">授权文件预览 (PDF)</label>
            <div class="upload-area" @click="triggerFile">
              <span v-if="!form.file">点击或拖拽 PDF 证明文件至此</span>
              <span v-else class="success-text">{{ form.file.name }}</span>
              <input ref="fileInput" type="file" hidden @change="onFile" accept=".pdf">
            </div>
          </div>
          <div class="actions dual">
            <button type="button" @click="currentStep = 1" class="btn btn-outline">上一步</button>
            <button :disabled="loading" type="submit" class="btn btn-primary">提交申请</button>
          </div>
        </div>
      </form>
      
      <div class="footer-links">
        已有账号? <router-link to="/login">返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'

const router = useRouter()
const currentStep = ref(1)
const loading = ref(false)
const fileInput = ref(null)

const form = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  university_name: '',
  contact: '',
  file: null
})

const universityList = ['中山大学', '华南理工大学', '暨南大学', '深圳大学'] // Mock

const triggerFile = () => fileInput.value.click()
const onFile = (e) => {
  const file = e.target.files[0]
  if (file && file.type === 'application/pdf') {
    form.file = file
  } else {
    alert('请上传 PDF 格式文件')
  }
}

const handleNext = () => {
  if (currentStep.value === 1) {
    if (form.password !== form.confirmPassword) {
      alert('密码不一致')
      return
    }
    currentStep.value = 2
  } else {
    handleSubmit()
  }
}

const handleSubmit = async () => {
  loading.value = true
  try {
    const res = await request.post('/register', {
      username: form.username,
      password: form.password,
      role: 'university',
      university_name: form.university_name
    })
    if (res.code === 200) {
      alert('注册申请已提交，请等待审核')
      router.push('/login')
    }
  } catch (err) {
    alert(err.message || '提交失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reg-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--bg-color);
  padding: 20px;
}

.reg-card {
  width: 520px;
  padding: 40px;
}

.reg-header { text-align: center; margin-bottom: 32px; }
.reg-header h1 { font-size: 24px; color: #1a237e; margin-bottom: 8px; }

.steps-indicator { display: flex; align-items: center; justify-content: center; margin-bottom: 40px; }
.step { display: flex; flex-direction: column; align-items: center; gap: 8px; opacity: 0.3; }
.step.active { opacity: 1; }
.step-num { width: 32px; height: 32px; background: #eee; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; }
.step.active .step-num { background: var(--primary-color); color: white; }
.step-line { flex: 1; height: 1px; background: #ddd; margin: 0 16px; margin-bottom: 24px; }

.upload-area {
  border: 2px dashed #ddd;
  padding: 40px;
  text-align: center;
  border-radius: var(--radius-md);
  cursor: pointer;
}

.upload-area:hover { border-color: var(--primary-color); background: #f8fafc; }

.actions.dual { display: flex; gap: 16px; }
.actions.dual button { flex: 1; }
.full-width { width: 100%; }

.footer-links { text-align: center; margin-top: 24px; font-size: 14px; }
.tip { font-size: 12px; color: #999; margin-top: 4px; }
</style>
