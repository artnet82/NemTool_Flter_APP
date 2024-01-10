import sqlite3

def load_model(model_name):
    conn = sqlite3.connect('nemtool.db')
    c = conn.cursor()

    c.execute('SELECT keywords FROM models WHERE name = ?', (model_name,))
    keywords = c.fetchone()[0]

    conn.close()

    # Обработка ключевых слов и создание модели
    model = {}

    # Пример обработки ключевых слов и создания модели
    for keyword in keywords.split(','):
        # Ваш код обработки каждого ключевого слова
        # и добавления его в модель
        normalized_keyword = keyword.lower().strip()
        model[normalized_keyword] = True

    return model

def filter_content(model, content):
    filtered_content = []

    words = content.split()

    for word in words:
        if word in model:
            filtered_content.append(word)

    filtered_content = ' '.join(filtered_content)

    return filtered_content

# Пример использования модели
model_name = 'Model 1'
content = 'Some content'

model = load_model(model_name)
filtered_content = filter_content(model, content)

print(filtered_content)
