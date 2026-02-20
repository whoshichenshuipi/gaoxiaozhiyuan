<template>
  <div class="community-page">
    <div class="community-header card">
      <div class="h-text">
        <h2>考生社区</h2>
        <p>发现更有趣的高考故事，与千万考生同行。</p>
      </div>
      <button class="btn btn-primary" @click="showModal = true">+ 发布动态</button>
    </div>

    <div class="community-content">
      <aside class="side-menu card">
        <h4>分类筛选</h4>
        <nav class="cat-nav">
          <a href="#" class="active">全部动态</a>
          <a href="#">经验分享</a>
          <a href="#">考研/出路</a>
          <a href="#">避雷指南</a>
        </nav>
      </aside>

      <main class="post-list">
        <div v-if="loading" class="loading-state">加载中...</div>
        <div v-else-if="posts.length === 0" class="empty-state">暂无动态，快来发布第一条吧！</div>
        <div v-for="post in posts" :key="post.id" class="card post-card">
          <div class="post-meta">
            <span class="author">👤 {{ post.author }}</span>
            <span class="time">{{ post.time }}</span>
            <span v-if="post.is_top" class="tag-top">置顶</span>
          </div>
          <h4 class="post-title">{{ post.title }}</h4>
          <p class="post-summary">{{ post.content }}</p>
          <div class="post-footer">
            <span class="stat">👍 {{ post.likes }}</span>
            <span class="stat">💬 {{ post.comments }}</span>
            <span class="share">分享</span>
          </div>
        </div>
      </main>
    </div>

    <!-- Publish Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-card card">
        <h3>发布新动态</h3>
        <div class="form-item">
          <label>标题</label>
          <input type="text" v-model="form.title" placeholder="起一个吸引人的标题吧...">
        </div>
        <div class="form-item">
          <label>正文内容</label>
          <textarea v-model="form.content" placeholder="分享你的故事或心得..."></textarea>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="showModal = false">取消</button>
          <button class="btn btn-primary" :disabled="submitting" @click="handlePublish">
            {{ submitting ? '发布中...' : '确认发布' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '../api/request'

const posts = ref([])
const total = ref(0)
const loading = ref(false)
const showModal = ref(false)
const submitting = ref(false)

const form = reactive({
  title: '',
  content: ''
})

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await request.get('/student/community/posts', {
      params: { page: 1, pageSize: 20 }
    })
    if (res.code === 200) {
      posts.value = res.data.list.map(p => ({
        id: p.id,
        author: p.author,
        time: p.create_time,
        title: p.title,
        content: p.content || '空内容',
        likes: p.like_num,
        comments: p.comment_num,
        is_top: p.top_flag === 1
      }))
      total.value = res.data.total
    }
  } catch (err) {
    console.error('Fetch posts failed:', err)
  } finally {
    loading.value = false
  }
}

const handlePublish = async () => {
  if (!form.title.trim() || !form.content.trim()) {
    return alert('标题和内容不能为空')
  }
  
  submitting.value = true
  try {
    const res = await request.post('/student/community/posts', {
      title: form.title,
      content: form.content
    })
    if (res.code === 200) {
      alert('发布成功！')
      showModal.value = false
      form.title = ''
      form.content = ''
      fetchPosts() // Refresh list
    }
  } catch (err) {
    alert('发布失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.community-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding: 32px; }
.h-text h2 { color: var(--primary-color); margin-bottom: 8px; }

.community-content { display: grid; grid-template-columns: 200px 1fr; gap: 24px; }

.cat-nav { display: flex; flex-direction: column; gap: 12px; margin-top: 16px; }
.cat-nav a { padding: 8px 12px; border-radius: 4px; color: #666; transition: all 0.3s; }
.cat-nav a.active, .cat-nav a:hover { background: #E3F2FD; color: var(--primary-color); font-weight: bold; }

.post-card { padding: 24px; margin-bottom: 20px; }
.post-meta { display: flex; align-items: center; gap: 16px; margin-bottom: 12px; font-size: 13px; color: #999; }
.tag-top { background: #FFF3E0; color: #EF6C00; padding: 2px 8px; border-radius: 4px; font-weight: bold; }

.post-title { font-size: 18px; margin-bottom: 12px; color: #333; }
.post-summary { font-size: 14px; color: #666; line-height: 1.6; margin-bottom: 20px; }

.post-footer { display: flex; gap: 24px; font-size: 13px; color: #999; border-top: 1px solid #f5f5f5; padding-top: 16px; }
.stat { cursor: pointer; }
.stat:hover { color: var(--primary-color); }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-card {
  width: 100%;
  max-width: 600px;
  padding: 32px;
}

.modal-card h3 { margin-bottom: 24px; color: var(--text-color); }

.form-item { margin-bottom: 20px; }
.form-item label { display: block; margin-bottom: 8px; font-weight: 500; font-size: 14px; }
.form-item input, .form-item textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  outline: none;
}
.form-item textarea { height: 160px; resize: vertical; }

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
}

.loading-state, .empty-state {
  text-align: center;
  padding: 48px;
  color: #999;
}
</style>
