<template>
  <div class="search-page">
    <!-- Filter Section -->
    <div class="card filter-section">
      <div class="search-bar">
        <input type="text" v-model="queryParams.keyword" placeholder="搜索院校或专业名称..." class="main-search">
        <button class="btn btn-primary" @click="handleSearch">搜索</button>
      </div>
      
      <div class="filter-group">
        <div class="filter-item">
          <span class="label">地域：</span>
          <select v-model="queryParams.region">
            <option value="">全部</option>
            <option value="北京">北京</option>
            <option value="上海">上海</option>
            <option value="广东">广东</option>
          </select>
        </div>
        <div class="filter-item">
          <span class="label">院校层次：</span>
          <select v-model="queryParams.level">
            <option value="">全部</option>
            <option value="985/211/双一流">985/211/双一流</option>
            <option value="985/211">985/211</option>
            <option value="双一流">双一流</option>
            <option value="一本">一本</option>
            <option value="二本">二本</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="results-container">
      <div class="results-header">
        <div class="tabs">
          <span :class="{ active: mode === 'uni' }" @click="mode = 'uni'">院校列表</span>
          <span :class="{ active: mode === 'major' }" @click="mode = 'major'">专业列表</span>
        </div>
        <div class="sort-options">
          <span>共找到 {{ total }} 条结果</span>
        </div>
      </div>

      <div class="results-list" v-if="mode === 'uni'">
        <div v-for="uni in universities" :key="uni.id" class="card uni-card">
          <div class="uni-info">
            <div class="uni-main">
              <h4>{{ uni.name }}</h4>
              <div class="tags">
                <span v-for="tag in uni.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="uni-meta">
              <span>📍 {{ uni.region }}</span>
              <span class="score-hint">去年录取：{{ uni.last_score }}分</span>
            </div>
          </div>
          <div class="uni-actions">
            <button class="btn btn-primary" @click="viewDetail(uni)">查看详情</button>
            <button class="btn btn-secondary" @click="toggleFavorite(uni)">
              {{ uni.isFav ? '❤️ 已收藏' : '🤍 加入收藏' }}
            </button>
          </div>
        </div>
      </div>

      <div class="results-table" v-else>
        <table class="card">
          <thead>
            <tr>
              <th>专业名称</th>
              <th>所属院校</th>
              <th>平均分</th>
              <th>招生计划</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="major in majors" :key="major.id">
              <td><strong>{{ major.name }}</strong></td>
              <td>{{ major.uni_name }}</td>
              <td class="text-primary">{{ major.avg_score }}</td>
              <td>{{ major.plan_count }}</td>
              <td><a href="#" @click.prevent="viewDetail(major)">详情</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import request from '../api/request'

const router = useRouter()
const route = useRoute()
const mode = ref('uni')
const total = ref(0)
const loading = ref(false)

const queryParams = reactive({
  keyword: route.query.keyword || '',
  region: '',
  level: '',
  page: 1,
  pageSize: 10
})

const universities = ref([])
const majors = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    if (mode.value === 'uni') {
      const res = await request.get('/student/universities', {
        params: {
          name: queryParams.keyword,
          region: queryParams.region,
          level: queryParams.level,
          page: queryParams.page,
          pageSize: queryParams.pageSize
        }
      })
      if (res.code === 200) {
        // Adapt backend data to frontend UI
        universities.value = res.data.list.map(u => ({
          ...u,
          tags: u.level ? u.level.split('/') : [],
          last_score: '详见详情', // Backend list doesn't have last_score
          isFav: false
        }))
        total.value = res.data.total
      }
    } else {
      const res = await request.get('/student/majors', {
        params: {
          name: queryParams.keyword,
          page: queryParams.page,
          pageSize: queryParams.pageSize
        }
      })
      if (res.code === 200) {
        majors.value = res.data.list.map(m => ({
          ...m,
          avg_score: '详见详情',
          plan_count: '-'
        }))
        total.value = res.data.total
      }
    }
  } catch (err) {
    console.error('Fetch failed:', err)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  queryParams.page = 1
  fetchData()
}

const viewDetail = (item) => {
  if (mode.value === 'uni') {
    router.push(`/uni/${item.id}`)
  } else {
    // For major, we might go to the university detail where it belongs or a major detail
    // For now, let's find the university id if available or just alert
    alert('正在进入专业：' + item.name)
  }
}

const toggleFavorite = (uni) => {
  uni.isFav = !uni.isFav
  alert(uni.isFav ? '已加入收藏' : '已取消收藏')
}

watch(mode, () => {
  queryParams.page = 1
  fetchData()
})

watch(() => route.query.keyword, (newVal) => {
  if (newVal !== undefined) {
    queryParams.keyword = newVal
    handleSearch()
  }
})

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.filter-section {
  background: white;
  padding: 32px;
}

.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.main-search {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.filter-group {
  display: flex;
  gap: 40px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-item select {
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.checks {
  display: flex;
  gap: 16px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 32px 0 16px;
}

.tabs {
  display: flex;
  gap: 32px;
  font-weight: 500;
  color: #666;
  border-bottom: 2px solid transparent;
}

.tabs span {
  cursor: pointer;
  padding-bottom: 8px;
}

.tabs span.active {
  color: var(--primary-color);
  border-bottom: 2px solid var(--primary-color);
}

.uni-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
}

.uni-main h4 {
  font-size: 20px;
  margin-bottom: 8px;
}

.tag {
  background: #E3F2FD;
  color: var(--primary-color);
  padding: 2px 8px;
  font-size: 12px;
  border-radius: 4px;
  margin-right: 8px;
}

.uni-meta {
  color: #666;
  font-size: 14px;
  margin-top: 8px;
}

.score-hint {
  margin-left: 20px;
  font-weight: 500;
  color: #2C3E50;
}

.uni-actions {
  display: flex;
  gap: 12px;
}

.btn-secondary {
  background: white;
  border: 1px solid #ddd;
  color: #666;
}

table {
  width: 100%;
  border-collapse: collapse;
  padding: 0;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f8f9fa;
  color: #666;
}

.text-primary { color: var(--primary-color); font-weight: bold; }
</style>
