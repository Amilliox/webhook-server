from flask import Flask, request
import os

app = Flask(__name__)

# Устанавливаем токен подтверждения для верификации
VERIFY_TOKEN = "mywhatsappwebhooktokenmega"  # Токен подтверждения, который ты указал

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Верификация запроса от WhatsApp
    if request.method == 'GET':
        # Получаем параметры из запроса
        challenge = request.args.get('hub.challenge')  # Параметр challenge
        token = request.args.get('hub.verify_token')  # Параметр verify_token от WhatsApp

        # Сравниваем токен в запросе с нашим токеном
        if token == VERIFY_TOKEN:
            return challenge, 200  # Если токены совпали, возвращаем challenge для подтверждения
        else:
            return 'Invalid verification token', 403  # Если токен неверный, возвращаем ошибку

    # Обработка входящих сообщений (POST запросы от WhatsApp)
    if request.method == 'POST':
        data = request.json  # Получаем данные от WhatsApp
        print("Получено сообщение:", data)  # Выводим их в консоль для проверки

        # Тут можно добавить логику обработки сообщений
        # Например, отправка ответов или другая логика

        return "OK", 200  # Отправляем ответ, что всё прошло успешно

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Используем порт, предоставленный Render
    app.run(host='0.0.0.0', port=port)  # Запускаем сервер на всех интерфейсах
