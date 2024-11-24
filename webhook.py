from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Получаем JSON-данные от WhatsApp
    print("Получено сообщение:", data)  # Выводим их в консоль для проверки
    return "OK", 200  # Отвечаем WhatsApp API, что запрос обработан успешно

if __name__ == '__main__':
    # Используем переменную окружения для порта
    port = int(os.environ.get("PORT", 5000))  # Используем 5000 по умолчанию для локальной разработки
    app.run(host='0.0.0.0', port=port)  # Flask будет слушать на правильном порту
