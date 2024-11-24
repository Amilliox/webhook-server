from flask import Flask, request
import os
import openai  # Убедись, что библиотека openai установлена: pip install openai

app = Flask(__name__)

# Устанавливаем токен подтверждения для верификации
VERIFY_TOKEN = "mywhatsappwebhooktokenmega"  # Токен подтверждения, который ты указал
OPENAI_API_KEY = "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"  # Замените на свой API-ключ OpenAI

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

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

        # Проверяем, есть ли сообщение от пользователя
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        value = change.get('value')
                        if value:
                            messages = value.get('messages')
                            if messages:
                                for message in messages:
                                    phone_number = message['from']  # Номер отправителя
                                    text = message['text']['body']  # Текст сообщения

                                    # Получаем ответ от OpenAI
                                    response = get_openai_response(text)

                                    # Здесь можно будет отправить ответ обратно в WhatsApp
                                    print(f"Ответ от OpenAI для {phone_number}: {response}")

        return "OK", 200

# Функция для отправки запроса в OpenAI и получения ответа
def get_openai_response(user_input):
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",  # Используемый движок (замени на нужный)
            prompt=user_input,
            max_tokens=150,  # Максимальное количество токенов в ответе
            n=1,
            stop=None,
            temperature=0.7,  # Контролирует "креативность" ответа
        )
        return completion.choices[0].text.strip()  # Возвращаем текст ответа
    except Exception as e:
        print(f"Ошибка при запросе к OpenAI: {e}")
        return "Произошла ошибка при обработке запроса. Попробуйте снова."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
