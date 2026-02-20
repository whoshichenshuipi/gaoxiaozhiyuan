<template>
  <div class="volunteer-page">
    <div class="v-header card">
      <div class="h-text">
        <h2>志愿方案管理</h2>
        <p>位次：第 {{ profile?.rank || '未知' }} 名 | 批次：普通本科批 | 剩余可填报位：{{ 80 - plan.length }}</p>
      </div>
      <div class="h-actions">
        <button class="btn btn-outline" @click="analyze">录取概率分析</button>
        <button class="btn btn-primary" @click="save">保存并导出 Excel</button>
      </div>
    </div>

    <div class="v-container">
      <!-- Plan List -->
      <div class="plan-section card">
        <div class="section-title">
          <span>当前填报方案 ({{ plan.length }})</span>
          <span class="tip">拖拽可调整排序</span>
        </div>
        <div class="plan-list">
          <div v-for="(item, i) in plan" :key="item.id" class="plan-item">
            <div class="rank">{{ i + 1 }}</div>
            <div class="content">
              <strong>{{ item.name }}</strong>
              <p>{{ item.major }}</p>
            </div>
            <div class="risk-indicator" :class="item.risk">
              {{ riskLabels[item.risk] }}
            </div>
            <div class="actions">
              <button class="icon-btn" @click="remove(i)">🗑️</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Analysis Results -->
      <aside class="analysis-section card">
        <h3>全量风险评估</h3>
        <div class="analysis-summary">
          <div class="donut-chart-mock">
            <div class="percent">92%</div>
            <p>综合录取概率</p>
          </div>
          <div class="analysis-text">
            <p>您的志愿方案呈现<strong>“哑铃型”</strong>结构：</p>
            <ul>
              <li>冲刺类占用 12%</li>
              <li>稳妥类占用 68%</li>
              <li>保底类占用 20%</li>
            </ul>
            <p class="suggestion">💡 建议：可适当增加 2-3 个冲刺志愿以寻求更优院校。</p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../api/request'

const riskLabels = { high: '冲', medium: '稳', safe: '保' }
const plan = ref([])
const profile = ref(null)
const analysis = ref(null)

const fetchInitialData = async () => {
  try {
    const pRes = await request.get('/student/profile')
    if (pRes.code === 200) profile.value = pRes.data
    
    await fetchPlans()
  } catch (err) {
    console.error('Fetch error:', err)
  }
}

const fetchPlans = async () => {
  try {
    const res = await request.get('/student/volunteer')
    if (res.code === 200) {
      // Map backend data to frontend view
      plan.value = res.data.map(p => ({
        id: p.id,
        name: p.university,
        major: p.major,
        risk: p.priority > 80 ? 'high' : (p.priority > 40 ? 'medium' : 'safe')
      }))
    }
  } catch (err) {
    console.error('Fetch plans failed:', err)
  }
}

const remove = async (index) => {
  const item = plan.value[index]
  try {
    const res = await request.delete(`/student/volunteer/${item.id}`)
    if (res.code === 200) {
      plan.value.splice(index, 1)
      alert('已移出志愿表')
    }
  } catch (err) {
    alert('删除失败')
  }
}

const analyze = async () => {
  if (!profile.value?.rank) return alert('请先设置您的位次信息')
  try {
    const res = await request.post('/student/volunteer/analyze', {
      rank: profile.value.rank
    })
    if (res.code === 200) {
      analysis.value = res.data
      alert('分析完成：' + res.data.details)
    }
  } catch (err) {
    alert('分析失败')
  }
}

const save = () => alert('正在导出 Excel...')

onMounted(() => {
  fetchInitialData()
})
</script>

<style scoped>
.v-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.h-text h2 { color: var(--primary-color); }

.h-actions { display: flex; gap: 12px; }

.v-container {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 24px;
}

.section-title {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.tip { font-size: 12px; color: #999; }

.plan-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 8px;
  margin-bottom: 12px;
  background: white;
  transition: transform 0.2s;
}

.rank {
  width: 32px;
  height: 32px;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  margin-right: 16px;
}

.content { flex: 1; }
.content p { font-size: 13px; color: #666; margin-top: 4px; }

.risk-indicator {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  margin-right: 20px;
}

.risk-indicator.high { background: var(--risk-high-bg); color: var(--risk-high-text); }
.risk-indicator.medium { background: var(--risk-medium-bg); color: var(--risk-medium-text); }
.risk-indicator.safe { background: var(--risk-safe-bg); color: var(--risk-safe-text); }

.icon-btn { background: none; font-size: 18px; }

.donut-chart-mock {
  width: 120px;
  height: 120px;
  border: 10px solid var(--risk-safe-bg);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  margin: 0 auto 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.donut-chart-mock .percent { font-size: 24px; font-weight: bold; color: var(--primary-color); }
.donut-chart-mock p { font-size: 12px; color: #666; }

.analysis-text { font-size: 14px; line-height: 1.8; }
.analysis-text ul { margin: 12px 0; padding-left: 20px; }
.suggestion { margin-top: 16px; color: var(--primary-color); }
</style>
