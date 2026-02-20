<template>
  <div class="rag-audit">
    <div class="admin-card header">
      <h3>RAG 知识库审核</h3>
      <div class="filter-row">
        <span>当前待审核任务：<strong>5</strong> 项</span>
      </div>
    </div>

    <AdminTable
      :columns="columns"
      :data="pendingDocs"
      :total="5"
      :page="1"
      :page-size="10"
    >
      <template #status>
        <span class="tag status-pending">待审核</span>
      </template>
      <template #operation="{ row }">
        <div class="op-links">
          <a href="javascript:;" @click="previewDoc(row)">预览内容</a>
          <a href="javascript:;" class="text-success" @click="handleAudit(row, 'approve')">通过</a>
          <a href="javascript:;" class="text-danger" @click="handleAudit(row, 'reject')">驳回</a>
        </div>
      </template>
    </AdminTable>

    <!-- 预览弹窗模拟 -->
    <div v-if="previewing" class="modal-overlay" @click="previewing = false">
      <div class="modal-card" @click.stop>
        <div class="modal-header">
          <h4>文档预览: {{ selectedDoc.doc_name }}</h4>
          <button class="close-btn" @click="previewing = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-for="(chunk, i) in selectedDoc.preview_chunks" :key="i" class="chunk-item">
            <span class="chunk-index">片段 #{{ i + 1 }}</span>
            <p>{{ chunk }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="handleAudit(selectedDoc, 'approve')">通过审核并加入向量库</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminTable from '../components/AdminTable.vue'
import request from '../api/request'

const previewing = ref(false)
const selectedDoc = ref(null)
const pendingDocs = ref([])

const fetchPendingDocs = async () => {
  try {
    const res = await request.get('/admin/rag/audit')
    if (res.code === 200) {
      pendingDocs.value = res.data
    }
  } catch (err) {
    console.error('Failed to fetch pending RAG docs:', err)
  }
}

const columns = [
  { key: 'uni_name', label: '所属院校' },
  { key: 'doc_name', label: '文档名称' },
  { key: 'create_time', label: '提交时间' },
  { key: 'status', label: '当前状态' },
  { key: 'operation', label: '操作', width: '220px' }
]

const previewDoc = (row) => {
  selectedDoc.value = row
  // Mocking preview chunks for UI demonstration if backend doesn't provide them yet
  if (!row.preview_chunks) {
    row.preview_chunks = ['依据该文档建立索引中...', '系统正在提取核心语义片段...']
  }
  previewing.value = true
}

const handleAudit = async (row, action) => {
  const msg = action === 'approve' ? '审批通过将启动重调度任务，合并至 RAG 引擎向量索引，确认吗？' : '驳回将从系统中移除该文档，确认吗？'
  if (confirm(msg)) {
    try {
      const res = await request.put(`/admin/rag/audit/${row.id}`, { action })
      if (res.code === 200) {
        alert('操作成功')
        if (previewing.value) previewing.value = false
        fetchPendingDocs()
      }
    } catch (err) {
      alert('操作失败')
    }
  }
}

onMounted(() => {
  fetchPendingDocs()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.status-pending {
  background: #fff8e1;
  color: #f57f17;
}

.text-success { color: var(--success-color); }
.text-danger { color: var(--error-color); }

.op-links {
  display: flex;
  gap: 12px;
}

/* Modal Simple Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white;
  width: 600px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
}

.chunk-item {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.chunk-index {
  font-size: 12px;
  color: #999;
  display: block;
  margin-bottom: 8px;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  text-align: right;
}

.close-btn {
  background: none;
  font-size: 24px;
  color: #ccc;
}
</style>
