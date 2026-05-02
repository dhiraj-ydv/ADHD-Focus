<template>
  <div class="matrix-grid">
    <div v-for="q in 4" :key="q" class="quadrant" :class="'q' + q">
      <h3>{{ quadrantTitles[q-1] }}</h3>
      <div class="matrix-tasks">
        <div 
          v-for="task in getTasksByPriority(q)" 
          :key="task.id" 
          class="matrix-task-item"
          @click="$emit('select-task', task)"
        >
          {{ task.title }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['tasks']);
const emit = defineEmits(['select-task']);

const quadrantTitles = [
  'Do First (Urgent & Important)',
  'Schedule (Important, Not Urgent)',
  'Delegate (Urgent, Not Important)',
  'Don\'t Do (Neither)'
];

const getTasksByPriority = (priority) => {
  return props.tasks.filter(t => t.priority === priority && t.status !== 'completed');
};
</script>

<style scoped>
.matrix-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 1.5rem;
  height: 100%;
}

.quadrant {
  background: var(--bg-secondary);
  border-radius: 20px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  border-top: 5px solid transparent;
}

.q1 { border-color: #ff5555; }
.q2 { border-color: #55ff55; }
.q3 { border-color: #5555ff; }
.q4 { border-color: #888888; }

.quadrant h3 {
  font-size: 1rem;
  margin-bottom: 1rem;
  color: var(--text-muted);
}

.matrix-tasks {
  flex: 1;
  overflow-y: auto;
}

.matrix-task-item {
  background: rgba(255,255,255,0.05);
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
}

.matrix-task-item:hover {
  background: rgba(255,255,255,0.1);
}
</style>
