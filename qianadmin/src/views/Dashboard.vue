<template>
  <div class="dashboard">
    <header class="page-title">
      <h1>控制面板核心状态</h1>
      <p>实时监控全局业务数据与系统性能负载。</p>
    </header>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="card stat-card">
        <div class="stat-main">
          <div class="stat-info">
            <p class="label">{{ stat.label }}</p>
            <p class="value">{{ stat.value }}</p>
          </div>
          <div class="stat-icon" :style="{ color: stat.color }">{{ stat.icon }}</div>
        </div>
        <div class="stat-trend" :class="stat.trend > 0 ? 'up' : 'down'">
          <span>{{ stat.trend > 0 ? '↑' : '↓' }} {{ Math.abs(stat.trend) }}%</span>
          <span class="period">较昨日同期</span>
        </div>
      </div>
    </div>

    <!-- Charts & Action Bento -->
    <div class="bento-container">
      <div class="card graph-card">
        <div class="card-header">
          <h3>资源请求动力学</h3>
          <div class="chart-tabs">
            <button class="active">实时</button>
            <button>存档</button>
          </div>
        </div>
        <div class="mock-chart-canvas">
          [ VIRTUAL CHARTING ENGINE - REALTIME STREAM ]
        </div>
      </div>

      <div class="card todo-card">
        <h3>核心待办事项</h3>
        <div class="todo-list">
          <div v-for="todo in todos" :key="todo.id" class="todo-item">
            <div class="todo-dot" :style="{ background: todo.color }"></div>
            <div class="todo-body">
              <p class="title">{{ todo.title }}</p>
              <p class="desc">{{ todo.desc }}</p>
            </div>
            <button class="action-link">立即处理 →</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../api/request'

const stats = ref([
  { label: '活跃用户总数', value: '0', icon: '👥', trend: 0, color: '#3b82f6', key: 'total_users' },
  { label: '院校库总量', value: '0', icon: '🏫', trend: 0, color: '#ec4899', key: 'total_universities' },
  { label: '专业库总量', value: '0', icon: '📝', trend: 0, color: '#f59e0b', key: 'total_majors' },
  { label: '累计问答次数', value: '0', icon: '💬', trend: 0, color: '#10b981', key: 'total_qa' }
])

const todos = ref([
  { id: 1, title: 'RAG 知识片段审核', desc: '清华大学 - 12 条待审', color: '#3b82f6' },
  { id: 2, title: '用户反馈分分拨', desc: '待分配 - 共 25 条', color: '#64748b' },
  { id: 3, title: '社区违规内容自动检举', desc: '拦截疑似 5 条', color: '#f59e0b' }
])

const fetchDashboardStats = async () => {
  try {
    const res = await request.get('/admin/statistics/dashboard')
    if (res.code === 200) {
      const data = res.data.summary
      stats.value.forEach(item => {
        if (item.key === 'total_users') item.value = data.total_users.toLocaleString()
        if (item.key === 'total_universities') item.value = data.total_universities.toLocaleString()
        if (item.key === 'total_majors') item.value = data.total_majors.toLocaleString()
        if (item.key === 'total_qa') item.value = data.total_qa.toLocaleString()
      })
    }
  } catch (err) {
    console.error('Failed to fetch stats:', err)
  }
}

onMounted(() => {
  fetchDashboardStats()
})
</script>

<style scoped>
.page-title { margin-bottom: 40px; }
.page-title h1 { font-size: 28px; margin-bottom: 8px; }
.page-title p { color: var(--text-muted); font-size: 14px; }

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 32px;
  margin-bottom: 40px;
}

.stat-card {
  position: relative;
  overflow: hidden;
}

.stat-card:before {
  content: '';
  position: absolute;
  right: -20px;
  bottom: -20px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.05) 0%, transparent 70%);
}

.stat-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.stat-info .label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  font-weight: 800;
  margin-bottom: 8px;
}

.stat-info .value {
  font-size: 32px;
  font-weight: 800;
  color: white;
}

.stat-icon {
  font-size: 24px;
  opacity: 0.8;
}

.stat-trend {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 10px;
  font-weight: 800;
}

.stat-trend.up { color: #10b981; }
.stat-trend.down { color: #ef4444; }
.period { color: var(--text-muted); font-weight: 500; }

.bento-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.graph-card { padding: 40px; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.chart-tabs {
  display: flex;
  background: rgba(0,0,0,0.2);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.chart-tabs button {
  background: transparent;
  border: none;
  padding: 6px 16px;
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  border-radius: 8px;
}

.chart-tabs button.active {
  background: var(--primary-color);
  color: white;
  box-shadow: var(--glow-blue);
}

.mock-chart-canvas {
  height: 320px;
  background: rgba(0,0,0,0.2);
  border: 1px dashed #334155;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #334155;
  font-weight: 800;
  letter-spacing: 0.3em;
  font-size: 12px;
}

.todo-list {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.todo-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.todo-dot {
  width: 3px;
  height: 24px;
  border-radius: 4px;
  flex-shrink: 0;
  margin-top: 4px;
}

.todo-body .title { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.todo-body .desc { font-size: 11px; color: var(--text-muted); }

.action-link {
  margin-left: auto;
  background: none;
  border: none;
  color: var(--primary-color);
  font-weight: 800;
  font-size: 11px;
  cursor: pointer;
}
</style>
