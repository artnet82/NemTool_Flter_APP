import os
import sqlite3
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'keywords'   # Папка для загруженных файлов
app.config['SQLITE_DB'] = 'nemtool.db'     # Файл базы данных SQLite

def create_database():
    conn = sqlite3.connect(app.config['SQLITE_DB'])
    c = conn.cursor()

    # Создание таблицы models, если она не существует
    c.execute('''CREATE TABLE IF NOT EXISTS models
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                keywords TEXT NOT NULL)''')

    conn.commit()
    conn.close()

def train_model():
    conn = sqlite3.connect(app.config['SQLITE_DB'])
    c = conn.cursor()

    c.execute('SELECT keywords FROM models')
    rows = c.fetchall()
    keywords = [row[0] for row in rows]

    # Инициализация векторизатора TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(keywords)

    # Получение целевых меток из базы данных или другого источника данных
    c.execute('SELECT labels FROM models')
    rows = c.fetchall()
    labels = [row[0] for row in rows]

    # Обучение модели
    model = SVC()
    model.fit(X, labels)

    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            keywords = file.read().decode('utf-8')   # Чтение содержимого файла с ключевыми словами

            conn = sqlite3.connect(app.config['SQLITE_DB'])
            c = conn.cursor()

            # Вставка названия модели и ключевых слов в таблицу models базы данных
            c.execute('INSERT INTO models (name, keywords) VALUES (?, ?)', ('Model 1', keywords))

            conn.commit()
            conn.close()

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   # Сохранение файла в папке keywords

            train_model()   # Обучение модели на основе данных из базы данных

            return 'Модель успешно обучена!'

    conn = sqlite3.connect(app.config['SQLITE_DB'])
    c = conn.cursor()

    c.execute('SELECT name FROM models')
    models = c.fetchall()

    conn.close()

    return render_template('index.html', models=models)

if __name__ == '__main__':
    create_database()
    app.run()
