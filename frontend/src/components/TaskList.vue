<template>
  <div class="task-list">
    <div class="task-header">
      <h2>Tasks</h2>
      <div class="stats">
        <span>{{ completedCount }} / {{ tasks.length }} Done</span>
      </div>
    </div>

    <div class="add-task">
      <input 
        v-model="newTaskTitle" 
        @keyup.enter="addTask" 
        placeholder="What are we focusing on?"
        class="task-input"
      />
      <div class="task-options">
        <select v-model="newTaskPriority">
          <option :value="1">Urgent & Important</option>
          <option :value="2">Important, Not Urgent</option>
          <option :value="3">Urgent, Not Important</option>
          <option :value="4">Neither</option>
        </select>
        <input type="number" v-model="newTaskPomos" min="1" max="10" title="Estimated Pomodoros" />
        <button @click="addTask" class="btn-add">+</button>
      </div>
    </div>

    <div class="tasks">
      <div 
        v-for="task in tasks" 
        :key="task.id" 
        class="task-item"
        :class="{ active: currentTaskId === task.id, completed: task.status === 'completed' }"
        @click="$emit('select-task', task)"
      >
        <div class="task-content">
          <input 
            type="checkbox" 
            :checked="task.status === 'completed'" 
            @change.stop="toggleTask(task)"
          />
          <span class="title">{{ task.title }}</span>
        </div>
        <div class="task-meta">
          <span class="pomos">{{ task.completed_pomodoros }}/{{ task.estimated_pomodoros }}</span>
          <button @click.stop="deleteTask(task.id)" class="btn-delete">×</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps(['tasks', 'currentTaskId']);
const emit = defineEmits(['add-task', 'update-task', 'delete-task', 'select-task']);

const newTaskTitle = ref('');
const newTaskPriority = ref(4);
const newTaskPomos = ref(1);

const completedCount = computed(() => props.tasks.filter(t => t.status === 'completed').length);

const addTask = () => {
  if (!newTaskTitle.value.trim()) return;
  emit('add-task', {
    title: newTaskTitle.value,
    priority: newTaskPriority.value,
    estimated_pomodoros: newTaskPomos.value
  });
  newTaskTitle.value = '';
};

const toggleTask = (task) => {
  const newStatus = task.status === 'completed' ? 'pending' : 'completed';
  emit('update-task', task.id, { status: newStatus });
};

const deleteTask = (id) => {
  if (confirm('Delete this task?')) {
    emit('delete-task', id);
  }
};
</script>

<style scoped>
.task-list {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.add-task {
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-input {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: rgba(255,255,255,0.05);
  color: inherit;
}

.task-options {
  display: flex;
  gap: 10px;
}

.task-options select, .task-options input {
  padding: 8px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: rgba(255,255,255,0.05);
  color: inherit;
}

.task-options select option {
  background-color: var(--bg-secondary);
  color: white;
}

.btn-add {
  padding: 8px 16px;
  border-radius: 8px;
  background: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.tasks {
  overflow-y: auto;
  flex: 1;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 12px;
  background: rgba(255,255,255,0.03);
  cursor: pointer;
  transition: all 0.2s;
}

.task-item:hover {
  background: rgba(255,255,255,0.08);
}

.task-item.active {
  border-left: 4px solid var(--primary-color);
  background: rgba(255,255,255,0.05);
}

.task-item.completed .title {
  text-decoration: line-through;
  color: var(--text-muted);
}

.task-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.task-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pomos {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.btn-delete {
  background: transparent;
  border: none;
  color: #ff5555;
  cursor: pointer;
  font-size: 1.2rem;
  opacity: 0;
}

.task-item:hover .btn-delete {
  opacity: 1;
}
</style>
