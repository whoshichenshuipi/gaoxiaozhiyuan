<template>
  <div class="recommend-page">
    <div class="recommend-header card">
      <div class="header-main">
        <h2>智能志愿推荐</h2>
        <p v-if="profile">基于您的画像：<strong>{{ profile.province }} {{ profile.subject_selection }} {{ profile.score }}分</strong> 位次 {{ profile.rank || '未知' }}</p>
        <p v-else>正在加载画像数据...</p>
        <p v-if="summary" class="summary">{{ summary }}</p>
      </div>
      <button class="btn btn-primary" :disabled="loading" @click="generate">
        {{ loading ? '推荐生成中...' : '重新生成推荐' }}
      </button>
    </div>

    <!-- Recommendations Grid -->
    <div class="recommend-grid">
      <!-- 冲刺类 -->
      <section class="risk-col">
        <div class="col-header risk-high">🍎 冲刺（高风险）</div>
        <div v-for="item in items.sprint" :key="item.id" class="card uni-card">
          <div class="card-body">
            <h5>{{ item.university_name }}</h5>
            <p class="major-name">{{ item.major_name }}</p>
            <div class="meta">
              <span class="prob">最低录分: {{ item.last_min_score }}</span>
              <span class="reason">最低位次: {{ item.last_min_rank }}</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="btn btn-outline-sm" @click="add(item)">加入计划</button>
          </div>
        </div>
      </section>

      <!-- 稳妥类 -->
      <section class="risk-col">
        <div class="col-header risk-medium">📒 稳妥（中风险）</div>
        <div v-for="item in items.stable" :key="item.id" class="card uni-card">
          <div class="card-body">
            <h5>{{ item.university_name }}</h5>
            <p class="major-name">{{ item.major_name }}</p>
            <div class="meta">
              <span class="prob">最低录分: {{ item.last_min_score }}</span>
              <span class="reason">最低位次: {{ item.last_min_rank }}</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="btn btn-outline-sm" @click="add(item)">加入计划</button>
          </div>
        </div>
      </section>

      <!-- 保底类 -->
      <section class="risk-col">
        <div class="col-header risk-safe">🍏 保底（低风险）</div>
        <div v-for="item in items.save" :key="item.id" class="card uni-card">
          <div class="card-body">
            <h5>{{ item.university_name }}</h5>
            <p class="major-name">{{ item.major_name }}</p>
            <div class="meta">
              <span class="prob">最低录分: {{ item.last_min_score }}</span>
              <span class="reason">最低位次: {{ item.last_min_rank }}</span>
            </div>
          </div>
          <div class="card-actions">
            <button class="btn btn-outline-sm" @click="add(item)">加入计划</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../api/request'

const loading = ref(false)
const profile = ref(null)
const summary = ref('')
const items = ref({
  sprint: [],
  stable: [],
  save: []
})

const fetchProfileAndGenerate = async () => {
  loading.value = true
  try {
    const pRes = await request.get('/student/profile')
    if (pRes.code === 200) {
      profile.value = pRes.data
      // Generate automatically
      await generate()
    }
  } catch (err) {
    console.error('Failed to fetch profile', err)
  } finally {
    loading.value = false
  }
}

const generate = async () => {
  if (!profile.value) {
    alert('请先完善个人画像（分、位次）')
    return
  }
  loading.value = true
  try {
    const res = await request.post('/student/recommendation/generate', {
      score: profile.value.score,
      rank: profile.value.rank || 15000, // Fallback if rank not in profile
      province: profile.value.province || '广东',
      subject: profile.value.subject_selection || '物理类'
    })
    if (res.code === 200) {
      items.value.sprint = res.data.sprint
      items.value.stable = res.data.stable
      items.value.save = res.data.safe // mapping 'safe' from backend to 'save' in frontend ref
      summary.value = res.data.summary
    }
  } catch (err) {
    alert('生成失败：' + (err.response?.data?.msg || err.message))
  } finally {
    loading.value = false
  }
}

const add = (item) => alert('功能开发中：已加入备选志愿表')

onMounted(() => {
  fetchProfileAndGenerate()
})
</script>

<style scoped>
.recommend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px;
  margin-bottom: 32px;
}

.header-main h2 { color: var(--primary-color); margin-bottom: 8px; }

.recommend-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.col-header {
  padding: 12px;
  border-radius: 8px 8px 0 0;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.risk-high { background: var(--risk-high-bg); color: var(--risk-high-text); }
.risk-medium { background: var(--risk-medium-bg); color: var(--risk-medium-text); }
.risk-safe { background: var(--risk-safe-bg); color: var(--risk-safe-text); }

.uni-card {
  margin-bottom: 16px;
  padding: 20px;
}

h5 { font-size: 16px; margin-bottom: 8px; }
.major-name { font-size: 13px; color: #666; margin-bottom: 12px; }

.meta { font-size: 12px; color: #999; display: flex; flex-direction: column; gap: 4px; }
.prob { color: var(--primary-color); font-weight: bold; }

.card-actions { margin-top: 16px; }
.btn-outline-sm {
  width: 100%;
  padding: 6px;
  font-size: 12px;
  border: 1px solid #ddd;
  background: white;
}
</style>
