import json
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'diary-super-secret-key'

DB_FILE = 'entries.json'

# ============================================================
# ЗАДАНИЕ 12. Функции для работы с JSON
# ============================================================
def load_entries():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_entries(entries_list):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(entries_list, f, ensure_ascii=False, indent=4)

# Загружаем записи один раз при старте
entries = load_entries()

# ============================================================
# МАРШРУТЫ ПРИЛОЖЕНИЯ
# ============================================================

# Задание 13. Главная страница
@app.route('/')
def index():
    return render_template('index.html', entries=entries)

# Задание 14. Просмотр одной записи
@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry:
        return render_template('detail.html', entry=entry)
    return 'Запись не найдена', 404

# Задание 15. Добавление записи (GET и POST)
@app.route('/add', methods=['GET', 'POST'])
def add():
    global entries
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Генерация ID (максимальный + 1)
        new_id = max([e['id'] for e in entries], default=0) + 1
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        new_entry = {
            "id": new_id,
            "title": title,
            "content": content,
            "date": current_date
        }
        
        entries.append(new_entry)
        save_entries(entries)
        return redirect(url_for('index'))
        
    return render_template('add.html')

# Задание 16. Редактирование записи (GET и POST)
@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    global entries
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if not entry:
        return 'Запись не найдена', 404
        
    if request.method == 'POST':
        entry['title'] = request.form.get('title')
        entry['content'] = request.form.get('content')
        save_entries(entries)
        return redirect(url_for('detail', entry_id=entry_id))
        
    return render_template('edit.html', entry=entry)

# Задание 17. Удаление записи (POST)
@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect(url_for('index'))

# Задание 18. Маршрут поиска
@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    filtered_entries = [e for e in entries if query in e['title'].lower()]
    return render_template('index.html', entries=filtered_entries, search_query=query)

# Задание 19. Фильтр за последние 7 дней
@app.route('/filter/week')
def filter_week():
    seven_days_ago = datetime.now() - timedelta(days=7)
    filtered_entries = []
    
    for e in entries:
        try:
            entry_date = datetime.strptime(e['date'], '%Y-%m-%d')
            if entry_date >= seven_days_ago:
                filtered_entries.append(e)
        except ValueError:
            continue
            
    return render_template('index.html', entries=filtered_entries, filter_active=True)

# Задание 20. Запуск приложения
if __name__ == '__main__':
    app.run(debug=True, port=5000)
