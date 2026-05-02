<template>
  <div class="app-container">
    <aside class="sidebar">
      <div class="logo">FocusFlow</div>
      <nav>
        <button @click="view = 'planner'" :class="{ active: view === 'planner' }">Planner</button>
        <button @click="view = 'matrix'" :class="{ active: view === 'matrix' }">Matrix</button>
        <button @click="view = 'settings'" :class="{ active: view === 'settings' }">Settings</button>
      </nav>
      <div class="ambient-control">
        <label>Ambience</label>
        <select v-model="settings.ambient_sound" @change="updateSettings">
          <option value="none">None</option>
          <option value="rain">Rain</option>
          <option value="waves">Waves</option>
          <option value="cafe">Cafe</option>
        </select>
      </div>

      <div class="system-controls">
        <button @click="systemControl('restart')" class="btn-restart">Restart App</button>
        <button @click="systemControl('stop')" class="btn-stop">Stop App</button>
      </div>
    </aside>

    <main class="content">
      <header class="top-bar">
        <h1>{{ viewTitle }}</h1>
        <div class="stats-summary">
          <span>Today's Progress: {{ progress }}%</span>
        </div>
      </header>

      <section v-if="view === 'planner'" class="planner-view">
        <div class="timer-section">
          <Timer 
            :settings="settings" 
            :currentTask="currentTask"
            @pomodoro-complete="handlePomoComplete"
          />
        </div>
        <div class="tasks-section">
          <TaskList 
            :tasks="tasks" 
            :currentTaskId="currentTask?.id"
            @add-task="addTask"
            @update-task="updateTask"
            @delete-task="deleteTask"
            @select-task="selectTask"
          />
        </div>
      </section>

      <section v-else-if="view === 'matrix'" class="matrix-view">
        <Matrix :tasks="tasks" @select-task="selectTask" />
      </section>

      <section v-else-if="view === 'settings'" class="settings-view">
        <div class="settings-card">
          <h3>Timer Settings</h3>
          <div class="setting-item">
            <label>Focus Time (min)</label>
            <input type="number" v-model="settings.focus_time" @change="updateSettings" />
          </div>
          <div class="setting-item">
            <label>Short Break (min)</label>
            <input type="number" v-model="settings.short_break" @change="updateSettings" />
          </div>
          <div class="setting-item">
            <label>Long Break (min)</label>
            <input type="number" v-model="settings.long_break" @change="updateSettings" />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import Timer from './components/Timer.vue';
import TaskList from './components/TaskList.vue';
import Matrix from './components/Matrix.vue';

const API_URL = 'http://localhost:5000/api';

const view = ref('planner');
const tasks = ref([]);
const settings = ref({
  focus_time: 25,
  short_break: 5,
  long_break: 15,
  ambient_sound: 'none'
});
const currentTask = ref(null);

const viewTitle = computed(() => {
  if (view.value === 'planner') return 'Daily Planner';
  if (view.value === 'matrix') return 'Eisenhower Matrix';
  return 'Settings';
});

const progress = computed(() => {
  if (tasks.value.length === 0) return 0;
  const completed = tasks.value.filter(t => t.status === 'completed').length;
  return Math.round((completed / tasks.value.length) * 100);
});

const fetchTasks = async () => {
  try {
    const res = await axios.get(`${API_URL}/tasks`);
    tasks.value = res.data;
  } catch (err) {
    console.error('Failed to fetch tasks', err);
  }
};

const fetchSettings = async () => {
  try {
    const res = await axios.get(`${API_URL}/settings`);
    settings.value = res.data;
  } catch (err) {
    console.error('Failed to fetch settings', err);
  }
};

const addTask = async (task) => {
  try {
    await axios.post(`${API_URL}/tasks`, task);
    fetchTasks();
  } catch (err) {
    console.error('Failed to add task', err);
  }
};

const updateTask = async (id, data) => {
  try {
    await axios.put(`${API_URL}/tasks/${id}`, data);
    fetchTasks();
  } catch (err) {
    console.error('Failed to update task', err);
  }
};

const deleteTask = async (id) => {
  try {
    await axios.delete(`${API_URL}/tasks/${id}`);
    fetchTasks();
    if (currentTask.value?.id === id) currentTask.value = null;
  } catch (err) {
    console.error('Failed to delete task', err);
  }
};

const updateSettings = async () => {
  try {
    await axios.put(`${API_URL}/settings`, settings.value);
  } catch (err) {
    console.error('Failed to update settings', err);
  }
};

const selectTask = (task) => {
  currentTask.value = task;
  view.value = 'planner';
};

const handlePomoComplete = () => {
  if (currentTask.value) {
    updateTask(currentTask.value.id, {
      completed_pomodoros: currentTask.value.completed_pomodoros + 1
    });
  }
};

const systemControl = async (action) => {
  if (confirm(`Are you sure you want to ${action} the application?`)) {
    try {
      await axios.post(`${API_URL}/system/control`, { action });
      alert(`System ${action} signal sent. The application will ${action} shortly.`);
    } catch (err) {
      console.error(`Failed to ${action} system`, err);
    }
  }
};

onMounted(() => {
  fetchTasks();
  fetchSettings();
});
</script>

<style>
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --primary-color: #38bdf8;
  --text-primary: #f8fafc;
  --text-muted: #94a3b8;
  --border-color: #334155;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.5;
}

.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 260px;
  background: var(--bg-secondary);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-color);
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--primary-color);
  margin-bottom: 3rem;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

nav button {
  text-align: left;
  padding: 12px 16px;
  border-radius: 10px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

nav button:hover, nav button.active {
  background: rgba(255,255,255,0.05);
  color: var(--text-primary);
}

nav button.active {
  border-left: 3px solid var(--primary-color);
}

.ambient-control {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ambient-control select {
  background: var(--bg-primary);
  color: var(--text-primary);
  padding: 8px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  width: 100%;
  cursor: pointer;
}

.ambient-control select option {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
}

.system-controls {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.system-controls button {
  padding: 10px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-restart {
  background: rgba(56, 189, 248, 0.1);
  color: var(--primary-color);
  border: 1px solid var(--primary-color) !important;
}

.btn-stop {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid #ef4444 !important;
}

.content {
  flex: 1;
  padding: 2rem 3rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.planner-view {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 3rem;
  flex: 1;
}

.settings-card {
  background: var(--bg-secondary);
  padding: 2rem;
  border-radius: 20px;
  max-width: 500px;
}

.setting-item {
  margin: 1.5rem 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.setting-item input {
  width: 80px;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: white;
}
</style>
