<template>
  <div class="feedback-management">
    <div class="admin-card header">
      <h3>用户反馈中心</h3>
      <p>处理来自考生的建议与投诉</p>
    </div>

    <AdminTable
      :columns="columns"
      :data="feedbacks"
      :total="feedbacks.length"
      :page="1"
      :pageSize="10"
    >
      <template #status="{ row }">
        <span class="tag" :class="row.status === 1 ? 'processed' : 'pending'">
          {{ row.status === 1 ? '已处理' : '待处理' }}
        </span>
      </template>
      <template #operation="{ row }">
        <div class="op-links">
          <a href="javascript:;" @click="handleReply(row)">{{ row.status === 1 ? '查看回复' : '立即处理' }}</a>
          <a href="javascript:;" class="text-danger" @click="handleDelete(row)">忽略</a>
        </div>
      </template>
    </AdminTable>

    <!-- 回复弹窗模拟 -->
    <div v-if="replying" class="modal-overlay" @click="replying = false">
      <div class="modal-card" @click.stop>
        <div class="modal-header">
          <h4>处理反馈: #{{ selectedItem.id }}</h4>
        </div>
        <div class="modal-body">
          <div class="user-msg">
            <p><strong>反馈内容：</strong></p>
            <div class="msg-box">{{ selectedItem.content }}</div>
          </div>
          <div class="reply-form">
            <p><strong>回复内容：</strong></p>
            <textarea v-model="replyText" placeholder="请输入答复考生的内容..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-primary" @click="submitReply">发送并标记已处理</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminTable from '../components/AdminTable.vue'
import request from '../api/request'

const replying = ref(false)
const selectedItem = ref(null)
const replyText = ref('')
const feedbacks = ref([])

const fetchFeedbacks = async () => {
  try {
    const res = await request.get('/admin/feedbacks')
    if (res.code === 200) {
      feedbacks.value = res.data.list
    }
  } catch (err) {
    console.error('Fetch failed:', err)
  }
}

const columns = [
  { key: 'user', label: '用户', width: '120px' },
  { key: 'type', label: '反馈类型', width: '100px' },
  { key: 'content', label: '反馈描述' },
  { key: 'status', label: '状态', width: '100px' },
  { key: 'create_time', label: '提交日期', width: '180px' },
  { key: 'operation', label: '操作', width: '150px' }
]

const handleReply = (row) => {
  selectedItem.value = row
  replyText.value = row.reply || ''
  replying.value = true
}

const submitReply = async () => {
  if (!replyText.value) return alert('请输入回复内容')
  try {
    const res = await request.post(`/admin/feedbacks/${selectedItem.value.id}/reply`, {
      reply: replyText.value
    })
    if (res.code === 200) {
      alert('已告知用户')
      replying.value = false
      fetchFeedbacks()
    }
  } catch (err) {
    alert('回复失败')
  }
}

const handleDelete = (row) => {
  alert('功能开发中：忽略 ID ' + row.id)
}

onMounted(() => {
  fetchFeedbacks()
})
</script>

<style scoped>
.header { margin-bottom: 24px; }
.header p { color: #666; font-size: 14px; }

.pending { background: #e8f5e9; color: #2e7d32; }
.processed { background: #f5f5f5; color: #999; }

.op-links { display: flex; gap: 12px; }
.text-danger { color: var(--error-color); }

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center;
  z-index: 1000;
}

.modal-card {
  background: white; width: 500px; border-radius: 8px;
}

.modal-header { padding: 20px; border-bottom: 1px solid #eee; }
.modal-body { padding: 20px; }

.msg-box {
  background: #f8f9fa; padding: 12px; border-radius: 4px;
  margin-top: 8px; margin-bottom: 20px; font-size: 14px;
}

textarea {
  width: 100%; height: 120px; padding: 12px;
  border: 1px solid #ddd; border-radius: 4px;
  margin-top: 8px; resize: none;
}

.modal-footer { padding: 20px; border-top: 1px solid #eee; text-align: right; }
</style>
