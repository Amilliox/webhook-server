from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json  # Получаем JSON-данные от WhatsApp
    print("Получено сообщение:", data)  # Выводим их в консоль для проверки
    return "OK", 200  # Отвечаем WhatsApp API, что запрос обработан успешно

if __name__ == '__main__':
    # Убираем app.run() для продакшн-режима, так как Render автоматически настроит сервер
    pass
