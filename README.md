# uma-telegram-client

## Как запускать это чучело локально

создать .env как в .env.example.
- парс мод опциональный: можно указать MARKDOWN, HTML - смотря как модель форматирует ответ.
    - можно попробовать MARKDOWN_V2 но он строже к форматированию, потеницально с ним больше ошибок.  
    - Если модель ошибется и неправильно форматнет текст - он будет отправлет в любом случае. Теги почистятся.

Бот токен и юзернейм я дам. Адрес n8n я не дам.

```.env.example
BOT_TOKEN=( ͡° ͜ʖ ͡°) #check botFather in telegram to generate token
BOT_USERNAME=username_bot #bot username. MUST BE WRITTEN WITHOUT '@'

N8N_SERVICE_ADDR=http://localhost:8080 #n8n service address
N8N_ANSWER_FORMAT=DEFAULT #optional. if parse mode not defined - it will be DAFAULT.
```

запускаем:

```
docker-compose up --build
```

Пишем боту в тг: @bsuir_assistant_bot

Вы превосходны

## Входы - выходы ВАЖНО

Бот отправляет на адрес: {N8N_SERVICE_ADDR}/ (СКАЗАТЬ МНЕ АДРЕС ЭНДПОИНТА ПОТОМ. Либо правьте файл src/web/client.py) http-сообщение с телом:


```
{"query":"строка с сообщением пользователя из телеграм"}
```

Бот ожидает в ответ получить http с таким телом:

```
{"response" : "ответ от llm"}
```

Но в целом распарсит любое и кинет в чат юзеру.