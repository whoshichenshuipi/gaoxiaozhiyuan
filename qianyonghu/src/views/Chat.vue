<template>
  <div class="chat-page card">
    <ChatWindow />
  </div>
</template>

<script setup>
import ChatWindow from '../components/ChatWindow.vue'
</script>

<style scoped>
.chat-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 0;
  height: 700px;
}
</style>
