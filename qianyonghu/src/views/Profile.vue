<template>
  <div class="profile-page">
    <div class="profile-header">
      <h2>精准画像采集</h2>
      <p>填写完整信息，我们将为您提供更精准的志愿推荐。</p>
    </div>

    <div class="profile-container">
      <!-- Image / Profile Card -->
      <aside class="profile-card card">
        <div class="avatar-header">
          <div class="avatar">🎓</div>
          <h3>张同学</h3>
          <p class="school-tag">2024届 毕业生</p>
        </div>
        <div class="stat-list">
          <div class="stat-item">
            <span class="s-label">预估位次</span>
            <span class="s-value">{{ form.rank ? '约 ' + form.rank + ' 名' : '未输入' }}</span>
          </div>
        </div>
      </aside>

      <!-- Form Area -->
      <main class="profile-main card">
        <div class="tabs">
          <button 
            v-for="t in tabs" 
            :key="t.value" 
            class="tab-link" 
            :class="{ active: currentTab === t.value }"
            @click="currentTab = t.value"
          >
            {{ t.label }}
          </button>
        </div>

        <div v-if="currentTab === 'basic'" class="tab-pane">
          <div class="form-row">
            <div class="form-item">
              <label>高考总分 (必填)</label>
              <input type="number" v-model="form.score" placeholder="请输入分数">
            </div>
            <div class="form-item">
              <label>全省位次</label>
              <input type="number" v-model="form.rank" placeholder="请输入您的全省排名">
            </div>
          </div>
          <div class="form-row">
            <div class="form-item">
              <label>所在省份 (必填)</label>
              <select v-model="form.province">
                <option value="广东">广东</option>
                <option value="北京">北京</option>
                <option value="浙江">浙江</option>
              </select>
            </div>
            <div class="form-item">
              <label>科类/首选科目</label>
              <select v-model="form.subject_selection">
                <option value="物理类">物理类</option>
                <option value="历史类">历史类</option>
                <option value="综合">综合 (老高考)</option>
              </select>
            </div>
          </div>
        </div>

        <div v-else class="tab-pane">
          <div class="form-item">
            <label>兴趣爱好 / 理想专业</label>
            <textarea v-model="form.hobbies" placeholder="例如：喜欢人工智能，想从事科研工作..."></textarea>
          </div>
          <div class="form-item">
            <label>地域偏好</label>
            <input type="text" v-model="form.region_preference" placeholder="例如：珠三角、长三角">
          </div>
          <div class="form-item">
            <label>特长说明</label>
            <input type="text" v-model="form.specialty" placeholder="例如：奥赛省奖、艺术特长">
          </div>
        </div>

        <div class="form-footer">
          <button class="btn btn-primary save-btn" @click="handleSave">保存画像</button>
          <span class="save-status" v-if="saved">✅ 已保存，推荐算法已更新</span>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import request from '../api/request'

const currentTab = ref('basic')
const saved = ref(false)
const tabs = [
  { label: '基础信息', value: 'basic' },
  { label: '兴趣偏好', value: 'pref' }
]

const subjects = ['物理', '化学', '生物', '政治', '历史', '地理']
const allTags = ['人工智能', '金融科技', '临床医学', '法学', '土木工程', '基础科学', '艺术设计']

const form = reactive({
  score: null,
  rank: null,
  province: '广东',
  subject_selection: '',
  hobbies: '',
  region_preference: '',
  specialty: ''
})

const fetchProfile = async () => {
  try {
    const res = await request.get('/student/profile')
    if (res.code === 200) {
      Object.assign(form, res.data)
    }
  } catch (err) {
    console.warn('Profile not found')
  }
}

const handleSave = async () => {
  if (!form.score) return alert('请先填写高考分数！')
  try {
    const res = await request.post('/student/profile', form)
    if (res.code === 200) {
      saved.value = true
      setTimeout(() => { saved.value = false }, 3000)
    }
  } catch (err) {
    alert('保存失败')
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.profile-header {
  margin-bottom: 32px;
}

.profile-header h2 {
  color: var(--primary-color);
  margin-bottom: 8px;
}

.profile-container {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
}

.avatar-header {
  text-align: center;
  padding-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.avatar {
  font-size: 64px;
  margin-bottom: 12px;
}

.school-tag {
  color: #999;
  font-size: 14px;
}

.stat-list {
  padding-top: 24px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}

.s-label { color: #666; }
.s-value { font-weight: bold; color: var(--primary-color); }

.tabs {
  margin-bottom: 32px;
  border-bottom: 1px solid #eee;
}

.tab-link {
  background: none;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  color: #666;
  cursor: pointer;
  position: relative;
}

.tab-link.active {
  color: var(--primary-color);
  font-weight: bold;
}

.tab-link.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary-color);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.form-item {
  margin-bottom: 24px;
}

.form-item label {
  display: block;
  font-weight: 500;
  margin-bottom: 12px;
}

input[type="number"], select, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

textarea {
  height: 100px;
  resize: vertical;
}

.subjects, .checks {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.tags-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag-item {
  padding: 6px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
}

.tag-item:hover, .tag-item.active {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background: #E3F2FD;
}

.form-footer {
  margin-top: 40px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.save-btn {
  padding: 12px 40px;
}

.save-status {
  font-size: 14px;
  color: var(--risk-safe-text);
}
</style>
