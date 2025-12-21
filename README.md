# uma-telegram-client

## Как запускать это чучело локально с docker-compose

создать в корне репа .env - его я дам.

Пример: 

```.env.example
BOT_TOKEN=( ͡° ͜ʖ ͡°) #check botFather in telegram to generate token
BOT_USERNAME=username_bot #bot username. MUST BE WRITTEN WITHOUT '@'

N8N_SERVICE_ADDR=http://localhost:8080 #n8n service address
N8N_ANSWER_FORMAT=DEFAULT #optional. if parse mode not defined - it will be DAFAULT.

EVENT_STORAGE_ADDR=http://localhost:8081 #event-storage address
```

- парс мод опциональный: можно указать MARKDOWN, HTML - смотря как модель форматирует ответ.
    - можно попробовать MARKDOWN_V2 но он строже к форматированию, потеницально с ним больше ошибок.  
    - Если модель ошибется и неправильно форматнет текст - он будет отправлен в любом случае. Теги почистятся.

Бот токен и юзернейм я дам. Адрес n8n я не дам.

запускаем из корня репозитория:

```
docker-compose up --build
```

Пишем боту в тг: @bsuir_assistant_bot либо добавляем в группу и тегаем бота

Вы превосходны

## Входы - выходы ВАЖНО

Бот отправляет на адрес: {N8N_SERVICE_ADDR}/webhook/pipeline http-сообщение с телом:


```json
{
    "query":"строка с сообщением пользователя из телеграм",
    "sessionId":123456789 //число с id телеграм-юзера
}
```

Бот ожидает в ответ получить http с таким телом:

```
{"response" : "ответ от llm"}
```

Но в целом распарсит любое и кинет в чат юзеру.

--- 

## Обновы

Теперь бот сохраняет ивенты в event-storage: сообщения, команды, ошибки. 

С поддерживаемыми типами ивентов можно ознакомиться в [репе](https://github.com/semantic-hallucinations/uma-event-storage)


В целом если сервис отвалится бот продолжит работу в штатном режиме, но мы потеряем часть истории просто не сохранится в сторедже. Хотелось бы, чтобы он не отваливался.
