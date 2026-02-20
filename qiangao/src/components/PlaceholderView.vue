<template>
  <div class="placeholder-view card">
    <div class="icon-box">
      <School :size="48" />
    </div>
    <h2>{{ title }}</h2>
    <p>该功能模块正在全速开发中...</p>
    <button class="btn btn-primary" @click="$router.push('/')">返回首页</button>
  </div>
</template>

<script setup>
import { School } from 'lucide-vue-next'
defineProps({
  title: { type: String, default: '功能模块' }
})
</script>

<style scoped>
.placeholder-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
}
.icon-box {
  width: 80px;
  height: 80px;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--primary-color);
  margin-bottom: 24px;
}
h2 { margin-bottom: 8px; color: #1e293b; }
p { color: #64748b; margin-bottom: 32px; }
</style>
