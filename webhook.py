from flask import Flask, request
import os
import openai
import requests

app = Flask(__name__)

# Устанавливаем токен подтверждения и токен доступа
VERIFY_TOKEN = "mywhatsappwebhooktokenmega"  # Токен подтверждения
ACCESS_TOKEN = "EAAIFtjwHax4BOZCKrNNxsGPQa1em7dmKaZBiS11ZAGQ7yyrvCFZA2KcJEAo8CnwOUQmFCCpb0HxOy4huVnN1zt8H7QkbN9XTdkYRjS81ZBFZC31nTlywPEAuArKAEdEbTPxVNu14O0IybK67dH8wwxTMVAEoe7ZA4ideS4A1vQXLZALX2yK9jZAZABovn2ZANOXZCCZB5z8ZAg280c4TYXWuO90tKZCZBC4brFjrvreKGE4ZARsUKFU0ZD"
# Подключение OpenAI API
openai.api_key = "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"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Верификация запроса от WhatsApp
        challenge = request.args.get('hub.challenge')
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Invalid verification token', 403

    if request.method == 'POST':
        # Получение данных от WhatsApp
        data = request.json
        if data and "messages" in data["entry"][0]["changes"][0]["value"]:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]  # ID отправителя
            text = message.get("text", {}).get("body", "")  # Текст сообщения

            # Отправляем запрос в OpenAI
            if text:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # Укажи модель
                    messages=[{"role": "user", "content": text}]
                )
                answer = response["choices"][0]["message"]["content"]

                # Отправляем ответ обратно в WhatsApp
                send_message(sender, answer)

        return "OK", 200

def send_message(recipient, text):
    """Функция отправки сообщения в WhatsApp."""
    url = f"https://graph.facebook.com/v17.0/456763200861670/messages"  # Здесь используется ваш ID телефона
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Ответ WhatsApp:", response.status_code, response.text)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
