from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Task, Settings
import os

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adhd_focus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()
    # Create default settings if not exists
    if not Settings.query.first():
        default_settings = Settings()
        db.session.add(default_settings)
        db.session.commit()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'estimated_pomodoros': t.estimated_pomodoros,
        'completed_pomodoros': t.completed_pomodoros,
        'status': t.status,
        'priority': t.priority,
        'created_at': t.created_at.isoformat()
    } for t in tasks])

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        title=data.get('title'),
        description=data.get('description', ''),
        estimated_pomodoros=data.get('estimated_pomodoros', 1),
        priority=data.get('priority', 4)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id}), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    if 'title' in data: task.title = data['title']
    if 'status' in data: task.status = data['status']
    if 'completed_pomodoros' in data: task.completed_pomodoros = data['completed_pomodoros']
    if 'priority' in data: task.priority = data['priority']
    
    db.session.commit()
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = Settings.query.first()
    return jsonify({
        'focus_time': settings.focus_time,
        'short_break': settings.short_break,
        'long_break': settings.long_break,
        'auto_start_breaks': settings.auto_start_breaks,
        'auto_start_tasks': settings.auto_start_tasks,
        'ambient_sound': settings.ambient_sound
    })

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    settings = Settings.query.first()
    data = request.json
    
    if 'focus_time' in data: settings.focus_time = data['focus_time']
    if 'short_break' in data: settings.short_break = data['short_break']
    if 'long_break' in data: settings.long_break = data['long_break']
    if 'ambient_sound' in data: settings.ambient_sound = data['ambient_sound']
    
    db.session.commit()
    return jsonify({'message': 'Settings updated'})

@app.route('/api/system/control', methods=['POST'])
def system_control():
    action = request.json.get('action')
    if action == 'stop':
        with open('stop.signal', 'w') as f:
            f.write('stop')
        return jsonify({'message': 'Stop signal sent'})
    elif action == 'restart':
        with open('restart.signal', 'w') as f:
            f.write('restart')
        return jsonify({'message': 'Restart signal sent'})
    return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
