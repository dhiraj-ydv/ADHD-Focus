# FocusFlow - ADHD Focus App

FocusFlow is a productivity tool designed specifically for the ADHD brain, combining a Pomodoro timer, task management, and an Eisenhower Matrix for prioritization. Built with **Flask** and **Vue.js 3**.

## 🚀 Features

- **Pomodoro Timer:** Custom focus and break intervals to maintain momentum.
- **Task Management:** Integrated task list with Pomodoro estimations to combat time blindness.
- **Eisenhower Matrix:** Visual 4-quadrant prioritization (Urgent vs. Important).
- **ADHD-Friendly UI:** Calming dark theme designed to reduce distractions and cognitive load.
- **Real-time Progress:** Daily completion stats and visual feedback.

## 🛠️ Tech Stack

- **Frontend:** Vue.js 3, Vite, Axios, Lucide Icons.
- **Backend:** Flask, Flask-SQLAlchemy, Flask-CORS.
- **Database:** SQLite.

## 🏁 Getting Started

### Prerequisites

- Python 3.x
- Node.js (v16+)
- npm

### Installation & Launch

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dhiraj-ydv/ADHD-Focus.git
   cd ADHD-Focus
   ```

2. **Setup (First time only):**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ../frontend
   npm install
   ```

3. **Run the App:**
   Simply double-click the **`start.bat`** file in the root directory.
   
   - **Frontend:** http://localhost:8080
   - **Backend:** http://localhost:5000

## 🕹️ Controls
You can manage the application lifecycle directly from the sidebar:
- **Restart App:** Restarts both backend and frontend processes.
- **Stop App:** Shuts down all processes and closes the terminal.

## 🧠 Design Philosophy

ADHD users often struggle with:
- **Time Blindness:** Addressed by using Pomodoro counts instead of just "tasks".
- **Choice Paralysis:** Addressed by the Eisenhower Matrix view.
- **Distraction:** Addressed by a minimalist, focused UI.

## 📝 License

MIT License
