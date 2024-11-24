from flask import Flask, request
import os
import requests

app = Flask(__name__)

# Токен подтверждения
VERIFY_TOKEN = "mywhatsappwebhooktokenmega" 

# Токен доступа для отправки сообщений (получен через WhatsApp Business API)
ACCESS_TOKEN = "your_whatsapp_access_token"  # Замените на ваш реальный токен

# URL WhatsApp API для отправки сообщений
WHATSAPP_API_URL = "https://graph.facebook.com/v14.0/your_phone_number_id/messages"  # Замените на свой

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # Верификация запроса от WhatsApp
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        token = request.args.get('hub.verify_token')

        if token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Invalid verification token', 403

    # Обработка входящих сообщений (POST запросы от WhatsApp)
    if request.method == 'POST':
        data = request.json  # Получаем данные от WhatsApp
        print("Получено сообщение:", data)

        # Пример обработки входящего сообщения
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        value = change.get('value')
                        if value:
                            # Получаем информацию о сообщении
                            messages = value.get('messages')
                            if messages:
                                for message in messages:
                                    # Пример автоматического ответа
                                    phone_number = message['from']
                                    send_message(phone_number, "Спасибо за ваше сообщение!")

        return "OK", 200

# Функция для отправки сообщения
def send_message(phone_number, text):
    payload = {
        'messaging_product': 'whatsapp',
        'to': phone_number,
        'text': {'body': text},
    }
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }
    
    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Сообщение отправлено на номер {phone_number}")
    else:
        print("Ошибка отправки сообщения:", response.json())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
