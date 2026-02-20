<template>
  <div class="user-management">
    <div class="admin-card filter-card">
      <div class="filter-row">
        <input v-model="filters.username" type="text" placeholder="搜索用户名" class="search-input">
        <select v-model="filters.role">
          <option value="">全部角色</option>
          <option value="student">考生</option>
          <option value="university">高校</option>
          <option value="admin">管理员</option>
        </select>
        <select v-model="filters.status">
          <option value="">全部状态</option>
          <option value="1">正常</option>
          <option value="0">禁用</option>
        </select>
        <button class="btn-primary" @click="fetchUsers">查询</button>
      </div>
    </div>

    <AdminTable
      :columns="columns"
      :data="users"
      :total="total"
      v-model:page="page"
      :page-size="pageSize"
      selectable
      :selected-ids="selectedIds"
      :is-all-selected="isAllSelected"
      @toggleSelect="toggleSelect"
      @toggleSelectAll="toggleSelectAll"
    >
      <template #actions>
        <button class="btn-batch btn-danger" :disabled="!selectedIds.length" @click="handleBatchDisable">批量禁用</button>
        <button class="btn-batch" :disabled="!selectedIds.length" @click="handleBatchEnable">批量启用</button>
      </template>

      <template #role="{ row }">
        <span class="tag role-tag" :class="row.role">{{ roleMap[row.role] }}</span>
      </template>

      <template #status="{ row }">
        <span class="status-dot" :class="row.status === 1 ? 'online' : 'offline'"></span>
        {{ row.status === 1 ? '正常' : '禁用' }}
      </template>

      <template #operation="{ row }">
        <div class="op-links">
          <a href="javascript:;" @click="handleStatusUpdate(row, row.status === 1 ? 0 : 1)">
            {{ row.status === 1 ? '禁用' : '启用' }}
          </a>
          <a href="javascript:;" class="text-danger" @click="handleDelete(row)">彻底删除</a>
          <a href="javascript:;" @click="editUser(row)">编辑</a>
        </div>
      </template>
    </AdminTable>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import AdminTable from '../components/AdminTable.vue'
import request from '../api/request'

const users = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const selectedIds = ref([])

const filters = reactive({
  username: '',
  role: '',
  status: ''
})

const columns = [
  { key: 'id', label: 'ID', width: '60px' },
  { key: 'username', label: '用户名' },
  { key: 'role', label: '角色' },
  { key: 'status', label: '状态' },
  { key: 'create_time', label: '注册时间' },
  { key: 'operation', label: '操作', width: '200px' }
]

const roleMap = {
  student: '考生',
  university: '高校',
  admin: '管理员'
}

const isAllSelected = computed(() => {
  return users.value.length > 0 && selectedIds.value.length === users.value.length
})

const fetchUsers = async () => {
  try {
    const params = {
      page: page.value,
      pageSize: pageSize,
      ...filters
    }
    const res = await request.get('/admin/users', { params })
    if (res.code === 200) {
      users.value = res.data.list
      total.value = res.data.total
    }
  } catch (err) {
    console.error('Failed to fetch users:', err)
  }
}

const toggleSelect = (id) => {
  const index = selectedIds.value.indexOf(id)
  if (index > -1) selectedIds.value.splice(index, 1)
  else selectedIds.value.push(id)
}

const toggleSelectAll = () => {
  if (isAllSelected.value) selectedIds.value = []
  else selectedIds.value = users.value.map(u => u.id)
}

const handleStatusUpdate = async (row, newStatus) => {
  try {
    const res = await request.put(`/admin/users/${row.id}/status`, { status: newStatus })
    if (res.code === 200) {
      alert('状态更新成功')
      fetchUsers()
    }
  } catch (err) {
    alert('更新失败: ' + (err.response?.data?.msg || err.message))
  }
}

const handleDelete = async (row) => {
  if (confirm(`确定要彻底删除用户 ${row.username} 吗？此操作不可逆！`)) {
    try {
      const res = await request.delete(`/admin/users/${row.id}`)
      if (res.code === 200) {
        alert('删除成功')
        fetchUsers()
      }
    } catch (err) {
      alert('删除失败')
    }
  }
}

const handleBatchDisable = async () => {
  if (!selectedIds.value.length) return
  if (confirm(`确定要禁用选中的 ${selectedIds.value.length} 个用户吗？`)) {
    // 循环调用或增加批量接口，这里演示循环调用状态更新
    for (const id of selectedIds.value) {
      await request.put(`/admin/users/${id}/status`, { status: 0 })
    }
    alert('操作完成')
    selectedIds.value = []
    fetchUsers()
  }
}

const editUser = (row) => alert('编辑功能开发中: ' + row.username)
const resetPwd = (row) => confirm('确定重置 ' + row.username + ' 的密码为初始密码吗？')

watch(page, () => {
  fetchUsers()
})

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.filter-card {
  margin-bottom: 24px;
}

.filter-row {
  display: flex;
  gap: 16px;
  align-items: center;
}

.search-input {
  min-width: 240px;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

select {
  padding: 8px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: white;
}

.tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.role-tag.student { background: #e8f5e9; color: #2e7d32; }
.role-tag.university { background: #fff3e0; color: #ef6c00; }
.role-tag.admin { background: #ede7f6; color: #512da8; }

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

.online { background: var(--success-color); }
.offline { background: var(--error-color); }

.op-links {
  display: flex;
  gap: 12px;
}

.text-danger { color: var(--error-color); }

.btn-batch {
  padding: 6px 12px;
  border-radius: 4px;
  background: #f1f1f1;
  border: 1px solid #ddd;
  font-size: 13px;
}

.btn-danger {
  color: #d32f2f;
  border-color: #ffcdd2;
}

.btn-batch:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
