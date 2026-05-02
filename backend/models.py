from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    estimated_pomodoros = db.Column(db.Integer, default=1)
    completed_pomodoros = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending') # pending, completed, cancelled
    priority = db.Column(db.Integer, default=4) # 1: Urgent/Imp, 2: Not Urgent/Imp, 3: Urgent/Not Imp, 4: Not Urgent/Not Imp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    focus_time = db.Column(db.Integer, default=25)
    short_break = db.Column(db.Integer, default=5)
    long_break = db.Column(db.Integer, default=15)
    auto_start_breaks = db.Column(db.Boolean, default=False)
    auto_start_tasks = db.Column(db.Boolean, default=False)
    ambient_sound = db.Column(db.String(50), default='none')
