<template>
  <div class="data-management">
    <div class="tab-header">
      <button 
        v-for="tab in tabs" 
        :key="tab.value" 
        class="tab-btn" 
        :class="{ active: currentTab === tab.value }"
        @click="currentTab = tab.value"
      >
        {{ tab.label }}
      </button>
    </div>

    <div v-if="currentTab === 'university'" class="tab-content">
      <div class="admin-card toolbar">
        <button class="btn-primary" @click="handleAddUni">+ 新增院校</button>
        <button class="btn-outline">批量导入</button>
        <button class="btn-outline">导出模板</button>
      </div>
      
      <AdminTable
        :columns="uniColumns"
        :data="universities"
        :total="uniTotal"
        v-model:page="uniPage"
        :page-size="10"
      >
        <template #level="{ row }">
          <span class="tag level-tag">{{ row.level }}</span>
        </template>
        <template #operation="{ row }">
          <div class="op-links">
            <a href="javascript:;">编辑</a>
            <a href="javascript:;" @click="manageMajors(row)">专业库</a>
            <a href="javascript:;" class="text-danger">删除</a>
          </div>
        </template>
      </AdminTable>
    </div>

    <div v-else class="tab-content">
      <div class="admin-card toolbar">
        <button class="btn-primary">+ 新增录取数据</button>
        <div class="import-hint">支持 .xlsx 格式批量导入招生计划与历年分线</div>
      </div>
      <!-- 录取数据表格类似不再赘述 -->
      <div class="empty-placeholder">
        招生录取数据管理模块 - 联动 Excel 导入处理中...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import AdminTable from '../components/AdminTable.vue'
import request from '../api/request'

const currentTab = ref('university')
const tabs = [
  { label: '院校管理', value: 'university' },
  { label: '招生录取数据', value: 'admission' }
]

const universities = ref([])
const uniTotal = ref(0)
const uniPage = ref(1)

const uniColumns = [
  { key: 'id', label: 'ID', width: '60px' },
  { key: 'name', label: '院校名称' },
  { key: 'level', label: '办学层次' },
  { key: 'region', label: '所在地区' },
  { key: 'official_url', label: '官方网址' },
  { key: 'operation', label: '操作', width: '220px' }
]

const fetchUniversities = async () => {
  try {
    const res = await request.get('/admin/universities', {
      params: { page: uniPage.value, pageSize: 10 }
    })
    if (res.code === 200) {
      universities.value = res.data.list
      uniTotal.value = res.data.total
    }
  } catch (err) {
    console.error('Fetch failed:', err)
  }
}

const handleAddUni = () => alert('弹出新增院校弹窗')
const manageMajors = (row) => alert('进入 ' + row.name + ' 的专业管理详情')

const handleImport = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)
  try {
    const res = await request.post('/admin/admission-data/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res.code === 200) alert('导入成功，请进入 RAG 审核或数据审核模块查看')
  } catch (err) {
    alert('导入失败')
  }
}

watch(uniPage, fetchUniversities)

onMounted(() => {
  fetchUniversities()
})
</script>

<style scoped>
.tab-header {
  display: flex;
  margin-bottom: 24px;
  border-bottom: 2px solid var(--border-color);
}

.tab-btn {
  background: none;
  padding: 12px 32px;
  font-size: 16px;
  font-weight: 600;
  color: #666;
  position: relative;
  transition: all 0.3s;
}

.tab-btn.active {
  color: var(--primary-color);
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary-color);
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.btn-outline {
  background: white;
  border: 1px solid var(--border-color);
  padding: 8px 16px;
  border-radius: 4px;
  margin-left: 12px;
}

.import-hint {
  font-size: 13px;
  color: #999;
}

.level-tag {
  background: #f0f4f8;
  color: #546e7a;
}

.op-links {
  display: flex;
  gap: 12px;
}

.text-danger { color: var(--error-color); }

.empty-placeholder {
  min-height: 400px;
  background: white;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ccc;
  border: 1px dashed #ddd;
}
</style>
