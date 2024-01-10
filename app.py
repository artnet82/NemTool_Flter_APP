import os
import sqlite3
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'keywords'
app.config['SQLITE_DB'] = 'nemtool.db'

def create_database():
    conn = sqlite3.connect(app.config['SQLITE_DB'])
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS models
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                keywords TEXT NOT NULL)''')

    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            keywords = file.read().decode('utf-8')

            conn = sqlite3.connect(app.config['SQLITE_DB'])
            c = conn.cursor()

            c.execute('INSERT INTO models (name, keywords) VALUES (?, ?)', ('Model 1', keywords))

            conn.commit()
            conn.close()

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

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
