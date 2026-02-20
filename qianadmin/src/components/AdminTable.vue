<template>
  <div class="admin-table">
    <div class="table-actions" v-if="$slots.actions">
      <slot name="actions"></slot>
    </div>
    
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th v-if="selectable" width="40">
              <input type="checkbox" :checked="isAllSelected" @change="$emit('toggleSelectAll')">
            </th>
            <th v-for="col in columns" :key="col.key" :width="col.width">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in data" :key="index">
            <td v-if="selectable">
              <input 
                type="checkbox" 
                :checked="selectedIds.includes(row.id)" 
                @change="$emit('toggleSelect', row.id)"
              >
            </td>
            <td v-for="col in columns" :key="col.key">
              <slot :name="col.key" :row="row">
                {{ row[col.key] }}
              </slot>
            </td>
          </tr>
          <tr v-if="data.length === 0">
            <td :colspan="columns.length + (selectable ? 1 : 0)" class="empty-cell">
              暂无数据
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="total > 0">
      <span class="total">共 {{ total }} 条</span>
      <div class="pager">
        <button :disabled="page <= 1" @click="$emit('update:page', page - 1)">上一页</button>
        <span class="current">{{ page }}</span>
        <button :disabled="page * pageSize >= total" @click="$emit('update:page', page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  columns: Array,
  data: Array,
  total: Number,
  page: Number,
  pageSize: Number,
  selectable: Boolean,
  selectedIds: Array,
  isAllSelected: Boolean
})

defineEmits(['update:page', 'toggleSelect', 'toggleSelectAll'])
</script>

<style scoped>
.admin-table {
  background: white;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.table-actions {
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  gap: 12px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #666;
}

tr:hover {
  background: #fcfcfc;
}

.empty-cell {
  text-align: center;
  padding: 40px;
  color: #999;
}

.pagination {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.pager {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pager button {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  background: white;
  border-radius: 4px;
}

.pager button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.current {
  font-weight: 600;
  color: var(--primary-color);
}
</style>
