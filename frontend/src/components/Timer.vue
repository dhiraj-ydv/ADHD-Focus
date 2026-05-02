<template>
  <div class="timer-container" :class="currentMode">
    <div class="modes">
      <button @click="setMode('focus')" :class="{ active: currentMode === 'focus' }">Focus</button>
      <button @click="setMode('shortBreak')" :class="{ active: currentMode === 'shortBreak' }">Short Break</button>
      <button @click="setMode('longBreak')" :class="{ active: currentMode === 'longBreak' }">Long Break</button>
    </div>

    <div class="timer-display">
      {{ formatTime(timeLeft) }}
    </div>

    <div class="controls">
      <button @click="toggleTimer" class="btn-primary">
        {{ isRunning ? 'Pause' : 'Start' }}
      </button>
      <button @click="resetTimer" class="btn-secondary">Reset</button>
    </div>

    <div class="timer-info">
      <p v-if="currentTask">Focusing on: <strong>{{ currentTask.title }}</strong></p>
      <p v-else>Select a task to stay focused</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, watch } from 'vue';

const props = defineProps(['settings', 'currentTask']);
const emit = defineEmits(['pomodoro-complete']);

const currentMode = ref('focus');
const isRunning = ref(false);
const timeLeft = ref(25 * 60);
let timerInterval = null;

const setMode = (mode) => {
  currentMode.value = mode;
  resetTimer();
};

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
};

const toggleTimer = () => {
  if (isRunning.value) {
    clearInterval(timerInterval);
  } else {
    timerInterval = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--;
      } else {
        completeSession();
      }
    }, 1000);
  }
  isRunning.value = !isRunning.value;
};

const resetTimer = () => {
  clearInterval(timerInterval);
  isRunning.value = false;
  if (currentMode.value === 'focus') timeLeft.value = props.settings.focus_time * 60;
  else if (currentMode.value === 'shortBreak') timeLeft.value = props.settings.short_break * 60;
  else timeLeft.value = props.settings.long_break * 60;
};

const completeSession = () => {
  clearInterval(timerInterval);
  isRunning.value = false;
  
  if (currentMode.value === 'focus') {
    emit('pomodoro-complete');
    alert('Focus session complete! Take a break.');
  } else {
    alert('Break over! Ready to focus?');
  }
  resetTimer();
};

watch(() => props.settings, () => {
  resetTimer();
}, { deep: true });

onUnmounted(() => {
  clearInterval(timerInterval);
});
</script>

<style scoped>
.timer-container {
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  transition: background 0.3s ease;
  background: var(--bg-secondary);
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.modes {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 2rem;
}

.modes button {
  padding: 8px 16px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  background: rgba(255,255,255,0.1);
  color: inherit;
  font-weight: 500;
}

.modes button.active {
  background: var(--primary-color);
  color: white;
}

.timer-display {
  font-size: 6rem;
  font-weight: 700;
  margin: 1rem 0;
  font-variant-numeric: tabular-nums;
}

.controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary {
  padding: 12px 40px;
  font-size: 1.2rem;
  border-radius: 30px;
  background: var(--primary-color);
  color: white;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.btn-secondary {
  padding: 12px 20px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: 30px;
  cursor: pointer;
}

.timer-info {
  margin-top: 2rem;
  color: var(--text-muted);
}
</style>
