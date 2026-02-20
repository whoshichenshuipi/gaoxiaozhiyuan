<template>
  <div class="home-page">
    <!-- Hero Section: Modern Gradient Banner -->
    <section class="hero-section card">
      <div class="hero-content">
        <h1>精准匹配，开启名校之旅</h1>
        <p>基于您的画像信息，AI 助您在 2700+ 高校中找到最优解</p>
        
        <div class="search-box card">
          <input type="text" v-model="searchKeyword" placeholder="搜索院校、专业代码或名称..." class="search-input" @keyup.enter="goSearch">
          <button class="btn btn-primary" @click="goSearch">全库检索</button>
        </div>
        
        <div class="hot-search">
          <span>热门：计算机科学</span>
          <span>临床医学</span>
          <span>人工智能</span>
          <span>法学</span>
        </div>
      </div>
      <!-- Decorative Orbs -->
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>
    </section>

    <!-- Bento Grid Dashboard -->
    <div class="bento-grid">
      <!-- Profile Insight -->
      <div class="card intro-card">
        <div class="card-header">
          <h3>高考画像</h3>
          <button class="text-btn" @click="$router.push('/profile')">更新配置 →</button>
        </div>
        <div class="stat-rows">
          <div class="stat-row">
            <span class="label">所在省份</span>
            <span class="val">{{ profile.province }} / {{ profile.subject_selection }}</span>
          </div>
          <div class="stat-row">
            <span class="label">预估总分</span>
            <div class="score-display">
              <span class="score">{{ profile.score }}</span>
              <span class="unit">分</span>
            </div>
          </div>
          <div class="stat-row">
            <span class="label">预估位次</span>
            <div class="score-display">
              <span class="score">{{ profile.rank || '-' }}</span>
              <span class="unit">名</span>
            </div>
          </div>
        </div>
        <div class="insight-box">
          <p>🎉 您的分数当前位于全省前 <strong>1.5%</strong>，建议关注 Top 20 重点院校。</p>
        </div>
      </div>

      <!-- Action Tools -->
      <div class="tools-grid">
        <div class="tool-card card" @click="$router.push('/recommend')">
          <div class="icon-box bg-blue">✨</div>
          <h4>智能志愿推荐</h4>
          <p>基于冲引稳保算法，一键生成匹配方案</p>
        </div>
        <div class="tool-card card" @click="$router.push('/volunteer')">
          <div class="icon-box bg-purple">📋</div>
          <h4>方案管理中心</h4>
          <p>管理并分析您的模拟志愿填报方案</p>
        </div>
        <div class="tool-card card" @click="$router.push('/search')">
          <div class="icon-box bg-orange">🔍</div>
          <h4>院校库全查核</h4>
          <p>百万级招生数据秒级查询，精准到校</p>
        </div>
        <div class="tool-card dark-card" @click="$router.push('/chat')">
          <div class="card-inner">
            <h4>AI 咨询助手</h4>
            <p>RAG 知识库加持，各校政策随时答疑解惑</p>
            <span class="link-label">立即对话 →</span>
          </div>
        </div>
      </div>

      <!-- News Feed -->
      <div class="card news-card">
        <h4 class="section-title">高校动态</h4>
        <div class="news-list">
          <div v-for="(news, index) in newsList" :key="news.id" class="news-item">
            <div class="dot" :class="{ active: index === 0 }"></div>
            <div class="news-body">
              <p class="title">{{ news.title }}</p>
              <p class="desc">{{ news.create_time }} · {{ news.type }}</p>
            </div>
          </div>
          <button class="btn btn-outline btn-sm" @click="$router.push('/community')">查看全部动态</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import request from '../api/request'

const profile = ref({
  score: 645, // default fallback
  province: '广东',
  subject_selection: '物理类'
})

const newsList = ref([
  { id: 1, title: '中山大学开放日', type: '公告', create_time: '2024-05-20' },
  { id: 2, title: '清华大学人工智能新专业', type: '技巧', create_time: '2024-05-18' }
])

const searchKeyword = ref('')
const router = useRouter() // Wait, I need to import useRouter

const goSearch = () => {
  if (!searchKeyword.value.trim()) return
  router.push({ path: '/search', query: { keyword: searchKeyword.value } })
}

const fetchHomeData = async () => {
  try {
    const pRes = await request.get('/student/profile')
    if (pRes.code === 200 && pRes.data.score) {
      profile.value = pRes.data
    } else {
      router.push('/profile')
    }
  } catch (err) {
    router.push('/profile')
  }

  try {
    const nRes = await request.get('/student/news', { params: { pageSize: 3 } })
    if (nRes.code === 200) {
      newsList.value = nRes.data.list
    }
  } catch (err) {
    console.error('News fetch failed', err)
  }
}

onMounted(() => {
  fetchHomeData()
})
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.hero-section {
  background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
  padding: 80px 48px;
  text-align: center;
  color: white;
  position: relative;
  overflow: hidden;
  border: none;
  box-shadow: 0 20px 50px rgba(30, 136, 229, 0.2);
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 720px;
  margin: 0 auto;
}

.hero-section h1 {
  font-size: 40px;
  margin-bottom: 16px;
  letter-spacing: -0.01em;
}

.hero-section p {
  opacity: 0.8;
  font-size: 18px;
  margin-bottom: 40px;
}

.search-box {
  background: white;
  padding: 8px;
  display: flex;
  gap: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  margin-bottom: 24px;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0 24px;
  font-size: 16px;
  color: var(--text-color);
}

.hot-search {
  display: flex;
  justify-content: center;
  gap: 24px;
  font-size: 13px;
  opacity: 0.7;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: rgba(255,255,255,0.1);
  top: -100px;
  right: -50px;
}

.orb-2 {
  width: 200px;
  height: 200px;
  background: rgba(30, 136, 229, 0.4);
  bottom: -50px;
  left: -50px;
}

.bento-grid {
  display: grid;
  grid-template-columns: 1fr 1.25fr 0.75fr;
  gap: 32px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.text-btn {
  background: none;
  border: none;
  color: var(--primary-color);
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
}

.stat-rows {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-color);
}

.stat-row .label { color: var(--text-secondary); font-weight: 500; }
.stat-row .val { font-weight: 700; }

.score-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.score {
  font-size: 32px;
  color: var(--primary-color);
  font-weight: 800;
}

.unit {
  font-size: 12px;
  color: var(--text-secondary);
}

.insight-box {
  margin-top: 32px;
  padding: 20px;
  background: #f0fff4;
  border-radius: 16px;
  border: 1px solid #dcfce7;
  color: #166534;
  font-size: 14px;
  line-height: 1.6;
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 24px;
}

.tool-card {
  padding: 32px;
  cursor: pointer;
}

.tool-card:hover {
  border-color: var(--primary-color);
}

.icon-box {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.bg-blue { background: #eff6ff; color: #1e88e5; }
.bg-purple { background: #f5f3ff; color: #7c3aed; }
.bg-orange { background: #fff7ed; color: #ea580c; }

.tool-card h4 { margin-bottom: 8px; font-size: 16px; }
.tool-card p { font-size: 12px; color: var(--text-secondary); line-height: 1.5; }

.dark-card {
  background: var(--text-color);
  color: white;
  border: none;
  position: relative;
  overflow: hidden;
}

.link-label {
  display: block;
  margin-top: 20px;
  color: var(--primary-color);
  font-weight: 700;
  font-size: 13px;
}

.section-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-secondary);
  margin-bottom: 24px;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.news-item {
  display: flex;
  gap: 16px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--border-color);
  margin-top: 6px;
  flex-shrink: 0;
}

.dot.active { background: var(--primary-color); }

.news-body p.title { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.news-body p.desc { font-size: 12px; color: var(--text-secondary); }

.btn-sm { width: 100%; margin-top: 16px; padding: 8px; font-size: 12px; }
</style>
