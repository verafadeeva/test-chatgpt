## LanguageModelChat

### Описание проекта
Простой сервис, который получает запрос от пользователя, перенаправляет его к апи chatgpt / gigachat, полученный ответ отдает пользователю.

### Технологии
- Python 3.11
- aiohttp
- pydantic
- poetry

### Запуск проекта

1. Склонировать репозиторий:

```
git clone git@github.com:verafadeeva/test-chatgpt.git
```
2. Перейти папку с проектом:
```
cd test-chatgpt
```
3. В корне проекта необходимо создать .env файл с таким содержанием:
```
URL_GPT='https://api.openai.com/v1/chat/completions'
API_KEY='<your key>'

SCOPE='GIGACHAT_API_PERS'
AUTH_CREDENTIALS='<your key>'
URL_GIGACHAT='https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
AUTH_URL='https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
```
4. Для управления зависимостями в проекте используется [poetry](https://python-poetry.org/docs/).
5. В директории /test-chatgpt выполнить команду:
```
make
```
6. После установки зависимостей и активации окружения, для запуска сервера выполнить:
```
make run
```

### Пример использования
Локально сервер доступен по адресу http://127.0.0.1:8080. Текущий ответ модели - это всегда последний объект в списке "messages". Чтобы сохранить контекст переписки и вести связный разговор - необходимо каждый раз отправлять весь массив сообщений.

Доступны следующие эндпоинты:
```
1. POST /chatgpt/
```
Пример запроса:
```
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "Привет!"
        }
    ]
}
```
Ответ:
```
{
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "Ты заботливый ассистент и хочешь помочь пользователю решить его проблему"
        },
        {
            "role": "user",
            "content": "Привет!"
        },
        {
            "role": "assistant",
            "content": "Привет! Чем я могу тебе помочь?"
        }
    ]
}
```
```
2. POST /gigachat/
```
Пример запроса:
```
{
    "model": "GigaChat:latest",
    "messages": [
        {
            "role": "user",
            "content": "Привет!"
        }
    ]
}
```
Ответ:
```
{
    "model": "GigaChat:latest",
    "messages": [
        {
            "role": "system",
            "content": "Ты заботливый ассистент и хочешь помочь пользователю решить его проблему"
        },
        {
            "role": "user",
            "content": "Привет!"
        },
        {
            "role": "assistant",
            "content": "Привет! Чем я могу тебе помочь?"
        }
    ]
}
```

### Автор
- Вера Фадеева ([@fadeevavera](https://t.me/fadeevavera))