<template>
  <div class="dashboard">
    <!-- Quick Stats Grid -->
    <div class="stats-grid">
      <div v-for="s in stats" :key="s.title" class="stat-card">
        <div class="stat-info">
          <p class="stat-label">{{ s.title }}</p>
          <h2 class="stat-value">{{ s.value }}</h2>
          <p class="stat-trend" :class="s.trend > 0 ? 'up' : 'down'">
            {{ s.trend > 0 ? '+' : '' }}{{ s.trend }}% 较昨日
          </p>
        </div>
        <div class="stat-icon" :style="{ backgroundColor: s.color + '15', color: s.color }">
          <component :is="s.icon" />
        </div>
      </div>
    </div>

    <div class="dashboard-main">
      <!-- Left: Recent Activity & Quick Actions -->
      <div class="main-left">
        <div class="card mb-20 section-card">
          <div class="section-header">
            <h3>快捷操作</h3>
          </div>
          <div class="quick-actions">
            <button v-for="a in actions" :key="a.name" class="action-btn" @click="handleAction(a)">
              <div class="action-icon" :style="{ background: a.bg }">
                <component :is="a.icon" />
              </div>
              <span class="action-name">{{ a.name }}</span>
            </button>
          </div>
        </div>

        <div class="card section-card">
          <div class="section-header">
            <h3>待办审核</h3>
            <a href="#" class="more-link">查看全部</a>
          </div>
          <div class="todo-list">
            <div v-for="t in todos" :key="t.id" class="todo-item">
              <div class="todo-info">
                <span class="todo-type" :class="t.type">{{ t.typeName }}</span>
                <p class="todo-title">{{ t.title }}</p>
              </div>
              <span class="todo-time">{{ t.time }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Source Overview Map/Chart -->
      <div class="main-right">
        <div class="card source-card">
          <div class="section-header">
            <h3>生源热度分布</h3>
            <router-link to="/source" class="more-link">分析报告</router-link>
          </div>
          <div ref="chartRef" class="source-chart"></div>
          <div class="source-summary">
            <div class="summary-item">
              <span class="dot primary"></span>
              <span class="label">华南地区</span>
              <span class="value">45%</span>
            </div>
            <div class="summary-item">
              <span class="dot secondary"></span>
              <span class="label">华东地区</span>
              <span class="value">28%</span>
            </div>
            <div class="summary-item">
              <span class="dot warning"></span>
              <span class="label">其他地区</span>
              <span class="value">27%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { 
  Users, 
  MessageCircle, 
  FileCheck, 
  Bell,
  PlusCircle,
  FileUp,
  Mail,
  Newspaper
} from 'lucide-vue-next'

const chartRef = ref(null)

const stats = [
  { title: '备选库总人数', value: '1,284', trend: 12, icon: Users, color: '#1565C0' },
  { title: '待处理咨询', value: '18', trend: -5, icon: MessageCircle, color: '#D32F2F' },
  { title: '待审核计划', value: '3', trend: 0, icon: FileCheck, color: '#F57C00' },
  { title: '未读系统通知', value: '7', trend: 2, icon: Bell, color: '#311B92' }
]

const actions = [
  { name: '发布招生章程', icon: PlusCircle, bg: '#E3F2FD', color: '#1565C0' },
  { name: '导入录取数据', icon: FileUp, bg: '#F3E5F5', color: '#7B1FA2' },
  { name: '回复考生留言', icon: Mail, bg: '#E8F5E9', color: '#2E7D32' },
  { name: '发布校园资讯', icon: Newspaper, bg: '#FFF3E0', color: '#E65100' }
]

const todos = [
  { id: 1, type: 'plan', typeName: '计划', title: '2024年江苏省物理类招生计划待确认', time: '2小时前' },
  { id: 2, type: 'score', typeName: '录取', title: '2023年广东省最低分录入有误待修正', time: '5小时前' },
  { id: 3, type: 'audit', typeName: '资质', title: '新的校园授权文件待上传复核', time: '昨日 17:30' }
]

onMounted(() => {
  const chart = echarts.init(chartRef.value)
  const option = {
    tooltip: { trigger: 'item' },
    series: [
      {
        name: '省份分布',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: { show: false },
        data: [
          { value: 1048, name: '广东' },
          { value: 735, name: '江苏' },
          { value: 580, name: '浙江' },
          { value: 484, name: '山东' },
          { value: 300, name: '其他' }
        ]
      }
    ]
  }
  chart.setOption(option)
  window.addEventListener('resize', () => chart.resize())
})

const handleAction = (a) => {
  console.log('Action:', a.name)
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.stat-label { color: var(--text-muted); font-size: 14px; margin-bottom: 8px; }
.stat-value { font-size: 28px; font-weight: 800; color: #1e293b; margin-bottom: 4px; }
.stat-trend { font-size: 12px; font-weight: 600; }
.stat-trend.up { color: #10b981; }
.stat-trend.down { color: #f43f5e; }

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dashboard-main {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.section-card { height: 100%; }

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h3 { font-size: 16px; font-weight: 700; color: #1e293b; }
.more-link { font-size: 13px; color: var(--primary-color); }

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.action-btn {
  background: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.2s;
}

.action-btn:hover { transform: translateY(-5px); }

.action-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.action-name { font-size: 13px; font-weight: 600; color: #475569; }

.todo-list { display: flex; flex-direction: column; gap: 12px; }
.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.todo-info { display: flex; align-items: center; gap: 12px; }
.todo-type {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  color: white;
}
.todo-type.plan { background: #3b82f6; }
.todo-type.score { background: #8b5cf6; }
.todo-type.audit { background: #f59e0b; }

.todo-title { font-size: 14px; font-weight: 500; color: #1e293b; }
.todo-time { font-size: 12px; color: #94a3b8; }

.source-card { height: 100%; display: flex; flex-direction: column; }
.source-chart { flex: 1; min-height: 250px; }

.source-summary {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  align-items: center;
  font-size: 13px;
}

.dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }
.dot.primary { background: #1565C0; }
.dot.secondary { background: #7B1FA2; }
.dot.warning { background: #F57C00; }

.summary-item .label { color: #64748b; flex: 1; }
.summary-item .value { font-weight: 700; color: #1e293b; }

@media (max-width: 1400px) {
  .dashboard-main { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
