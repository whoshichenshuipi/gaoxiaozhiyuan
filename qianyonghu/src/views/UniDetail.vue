<template>
  <div class="uni-detail">
    <!-- Header -->
    <div class="card detail-header">
      <div class="uni-brand">
        <div class="uni-logo">🏫</div>
        <div class="uni-titles">
          <h2>{{ uniInfo.name }}</h2>
          <div class="tags">
            <span v-for="tag in uniInfo.tags" :key="tag" class="tag">{{ tag }}</span>
            <span class="region">{{ uniInfo.region }}</span>
          </div>
        </div>
      </div>
      <button class="btn btn-outline" @click="toggleFav">
        {{ isFav ? '❤️ 已入备选库' : '🤍 加入备选库' }}
      </button>
    </div>

    <!-- Tabs -->
    <div class="tab-container">
      <div class="tabs">
        <button 
          v-for="t in tabs" 
          :key="t.value" 
          :class="{ active: currentTab === t.value }"
          @click="currentTab = t.value"
        >
          {{ t.label }}
        </button>
      </div>

      <div class="tab-panel">
        <!-- 简介 -->
        <div v-if="currentTab === 'intro'" class="card intro-card">
          <h4>学校简介</h4>
          <p class="summary">{{ uniInfo.summary }}</p>
          <div class="features">
            <div class="feature-item">
              <strong>特色专业：</strong>
              <span>计算机科学、人工智能、微电子、自动化</span>
            </div>
            <div class="feature-item">
              <strong>就业情况：</strong>
              <span>历年就业率保持在 95% 以上，头部学子多去往华为、腾讯等企业。</span>
            </div>
          </div>
        </div>

        <!-- 录取数据图表 -->
        <div v-if="currentTab === 'data'" class="card data-card">
          <div class="chart-header">
            <h4>近三年录取位次走势</h4>
            <div class="chart-options">
              <select><option>全部专业</option><option>计算机科学</option></select>
            </div>
          </div>
          <div id="scoreChart" class="chart-box"></div>
          <p class="hint-text">💡 提示：折线呈下降趋势表示报考热度持续上升，位次要求更严苛。</p>
        </div>

        <!-- 专业库 -->
        <div v-if="currentTab === 'majors'" class="card majors-card">
          <h4>开设专业 ({{ uniInfo.majors.length }})</h4>
          <div class="majors-grid">
            <div v-for="m in uniInfo.majors" :key="m.id" class="major-item">
              <span class="m-name">{{ m.name }}</span>
              <span class="m-cat">{{ m.category }}</span>
            </div>
          </div>
        </div>

        <!-- 智能问答 -->
        <div v-if="currentTab === 'qa'" class="qa-wrapper">
          <ChatWindow :university-name="uniInfo.name" :university-id="route.params.id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import ChatWindow from '../components/ChatWindow.vue'
import request from '../api/request'

const route = useRoute()
const currentTab = ref('intro')
const isFav = ref(false)
const loading = ref(false)

const tabs = [
  { label: '学校简介', value: 'intro' },
  { label: '录取数据', value: 'data' },
  { label: '专业库', value: 'majors' },
  { label: '智能问答', value: 'qa' }
]

const uniInfo = ref({
  name: '',
  tags: [],
  region: '',
  summary: '',
  majors: [],
  admission_data: []
})

const fetchUniDetail = async () => {
  const id = route.params.id
  loading.value = true
  try {
    const res = await request.get(`/student/universities/${id}`)
    if (res.code === 200) {
      const data = res.data
      uniInfo.value = {
        name: data.info.name,
        tags: data.info.level ? data.info.level.split('/') : [],
        region: data.info.region,
        summary: data.info.intro || '暂无详细介绍',
        majors: data.majors,
        admission_data: data.admission_data
      }
    }
  } catch (err) {
    console.error('Fetch uni detail failed:', err)
  } finally {
    loading.value = false
  }
}

const toggleFav = async () => {
  // Mock add to volunteer plan
  try {
    const res = await request.post('/student/volunteer', {
      type: '备选库',
      university_id: route.params.id,
      priority: 50
    })
    if (res.code === 200) {
      isFav.value = true
      alert('已加入备选志愿表')
    }
  } catch (err) {
    alert('操作失败')
  }
}

const initChart = () => {
  const chartDom = document.getElementById('scoreChart')
  if (!chartDom || !uniInfo.value.admission_data.length) return
  const myChart = echarts.init(chartDom)
  
  // Pivot data for years
  const yearData = {}
  uniInfo.value.admission_data.forEach(s => {
    if (!yearData[s.year]) yearData[s.year] = []
    yearData[s.year].push(s.min_rank)
  })
  
  const years = Object.keys(yearData).sort()
  const avgRanks = years.map(y => {
    const ranks = yearData[y]
    return Math.floor(ranks.reduce((a, b) => a + b, 0) / ranks.length)
  })

  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: years
    },
    yAxis: {
      type: 'value',
      inverse: true,
      name: '平均录位'
    },
    series: [{
      data: avgRanks,
      type: 'line',
      smooth: true,
      color: '#1E88E5',
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(30, 136, 229, 0.3)' },
          { offset: 1, color: 'rgba(30, 136, 229, 0)' }
        ])
      }
    }]
  }
  myChart.setOption(option)
}

onMounted(async () => {
  await fetchUniDetail()
  if (currentTab.value === 'data') initChart()
})

watch(currentTab, (newTab) => {
  if (newTab === 'data') {
    setTimeout(initChart, 100)
  }
})
</script>

<style scoped>
.uni-detail {
  max-width: 1200px;
  margin: 0 auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px;
  margin-bottom: 24px;
}

.uni-brand {
  display: flex;
  gap: 24px;
  align-items: center;
}

.uni-logo {
  font-size: 48px;
  background: #f8f9fa;
  padding: 16px;
  border-radius: 12px;
}

.uni-titles h2 { margin-bottom: 8px; }

.tag {
  background: #E3F2FD;
  color: var(--primary-color);
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 13px;
  margin-right: 8px;
}

.region { font-size: 14px; color: #666; }

.tabs {
  display: flex;
  gap: 40px;
  margin-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.tabs button {
  background: none;
  border: none;
  padding: 12px 16px;
  font-size: 16px;
  color: #666;
  cursor: pointer;
}

.tabs button.active {
  color: var(--primary-color);
  font-weight: bold;
  border-bottom: 2px solid var(--primary-color);
}

.intro-card { line-height: 1.8; }
.summary { font-size: 16px; margin-bottom: 24px; }
.feature-item { margin-bottom: 12px; }

.chart-box {
  height: 400px;
  width: 100%;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.majors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.major-item {
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.m-name { font-weight: 500; }
.m-cat { font-size: 12px; color: #999; }
</style>
