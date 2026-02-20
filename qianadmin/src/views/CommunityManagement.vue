<template>
  <div class="community-management">
    <div class="admin-card toolbar">
      <div class="filter-group">
        <button 
          v-for="f in filterTypes" 
          :key="f.label" 
          class="filter-btn" 
          :class="{ active: currentFilter === f.value }"
          @click="currentFilter = f.value"
        >
          {{ f.label }}
        </button>
      </div>
    </div>

    <AdminTable
      :columns="columns"
      :data="posts"
      :total="posts.length"
      :page="1"
      :page-size="10"
    >
      <template #content="{ row }">
        <div class="post-preview">
          <strong>{{ row.title }}</strong>
          <p>{{ row.content.substring(0, 50) }}...</p>
        </div>
      </template>
      <template #is_top="{ row }">
        <span v-if="row.is_top" class="tag top-tag">置顶</span>
        <span v-else class="text-muted">-</span>
      </template>
      <template #operation="{ row }">
        <div class="op-links">
          <a href="javascript:;" @click="toggleTop(row)">{{ row.is_top ? '取消置顶' : '置顶' }}</a>
          <a href="javascript:;" class="text-danger" @click="handleDelete(row)">删除</a>
          <a href="javascript:;" @click="viewPost(row)">查看全文</a>
        </div>
      </template>
    </AdminTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminTable from '../components/AdminTable.vue'
import request from '../api/request'

const currentFilter = ref('all')
const filterTypes = [
  { label: '全部帖子', value: 'all' },
  { label: '违规历史', value: 'banned' },
  { label: '置顶内容', value: 'top' }
]

const posts = ref([])
const total = ref(0)
const page = ref(1)

const fetchPosts = async () => {
  try {
    const res = await request.get('/admin/posts', {
      params: { page: page.value, pageSize: 10 }
    })
    if (res.code === 200) {
      posts.value = res.data.list
      total.value = res.data.total
    }
  } catch (err) {
    console.error('Fetch posts failed:', err)
  }
}

const columns = [
  { key: 'content', label: '内容摘要' },
  { key: 'author', label: '发布人', width: '120px' },
  { key: 'is_top', label: '状态', width: '100px' },
  { key: 'time', label: '发布日期', width: '180px' },
  { key: 'operation', label: '操作', width: '200px' }
]

const toggleTop = async (row) => {
  try {
    const res = await request.put(`/admin/posts/${row.id}/top`)
    if (res.code === 200) {
      alert('已更新置顶状态')
      fetchPosts()
    }
  } catch (err) {
    alert('操作失败')
  }
}

const handleDelete = async (row) => {
  if (confirm('确定要删除该帖吗？操作不可撤销，且会记录在系统日志中。')) {
    try {
      const res = await request.delete(`/admin/posts/${row.id}`)
      if (res.code === 200) {
        alert('已删除')
        fetchPosts()
      }
    } catch (err) {
      alert('删除失败')
    }
  }
}

const viewPost = (row) => alert('查看详情功能开发中: ' + row.title)

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.toolbar {
  margin-bottom: 24px;
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-btn {
  background: #f1f1f1;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  color: #666;
  font-weight: 500;
}

.filter-btn.active {
  background: var(--primary-color);
  color: white;
}

.post-preview {
  max-width: 400px;
}

.post-preview strong {
  display: block;
  margin-bottom: 4px;
  color: #333;
}

.post-preview p {
  font-size: 13px;
  color: #666;
}

.top-tag {
  background: #fff3e0;
  color: #ef6c00;
  border: 1px solid #ffe0b2;
}

.text-muted { color: #ccc; }
.op-links { display: flex; gap: 12px; }
.text-danger { color: var(--error-color); }
</style>
