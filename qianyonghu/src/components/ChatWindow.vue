<template>
  <div class="chat-container card">
    <div class="chat-header">
      <h4>🤖 智能助手: {{ universityName || '高考咨询' }}</h4>
      <p class="status">AI 助手在线，支持 RAG 知识库检索</p>
    </div>
    
    <div class="message-list" ref="msgList">
      <div v-for="(msg, i) in messages" :key="i" class="message-wrapper" :class="msg.role">
        <div class="avatar">{{ msg.role === 'assistant' ? '🤖' : '👤' }}</div>
        <div class="message-content">
          <div class="text">{{ msg.content }}</div>
          <div v-if="msg.source" class="source-box">
            <p><strong>来源指引：</strong></p>
            <ul>
              <li v-for="(s, si) in msg.source" :key="si">
                <a href="#">{{ s }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div v-if="loading" class="loading-msg">思考中...</div>
    </div>

    <div class="chat-input-area">
      <input 
        v-model="input" 
        type="text" 
        placeholder="输入您想咨询的问题，例如：该校计算机专业位次要求？"
        @keyup.enter="sendMessage"
      >
      <button class="btn btn-primary" :disabled="loading" @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import request from '../api/request'

const props = defineProps({
  universityName: String,
  universityId: [Number, String]
})

const messages = ref([
  { role: 'assistant', content: `您好！我是${props.universityName || ''}智能咨询助手，您可以问我关于招生简章、录取分线或专业特色相关的问题。` }
])
const input = ref('')
const loading = ref(false)
const msgList = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (msgList.value) {
    msgList.value.scrollTop = msgList.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!input.value.trim() || loading.value) return

  const userMsg = input.value
  messages.value.push({ role: 'user', content: userMsg })
  input.value = ''
  loading.value = true
  scrollToBottom()

  try {
    const res = await request.post('/student/qa/general', {
      question: userMsg,
      university_id: props.universityId
    })
    
    if (res.code === 200) {
      messages.value.push({
        role: 'assistant',
        content: res.data.answer,
        source: res.data.rag_used ? ['知识库匹配数据'] : ['通用智库']
      })
    }
  } catch (err) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，我现在无法回答这个问题，请稍后再试。'
    })
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.chat-container {
  height: 600px;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
}

.chat-header {
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
  background: #f8f9fa;
}

.chat-header h4 { margin: 0; color: var(--primary-color); }
.status { font-size: 12px; color: #2e7d32; margin-top: 4px; }

.message-list {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-wrapper {
  display: flex;
  gap: 12px;
  max-width: 85%;
}

.message-wrapper.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  background: #eee;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  flex-shrink: 0;
}

.message-content {
  background: #f1f1f1;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
}

.user .message-content {
  background: var(--primary-color);
  color: white;
}

.source-box {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #ccc;
  font-size: 12px;
}

.source-box ul {
  list-style: none;
  padding: 0;
  margin-top: 4px;
}

.source-box a {
  color: #1565c0;
  text-decoration: underline;
}

.loading-msg {
  font-size: 12px;
  color: #999;
  font-style: italic;
}

.chat-input-area {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 12px;
}

.chat-input-area input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
}

.chat-input-area input:focus {
  border-color: var(--primary-color);
}
</style>
