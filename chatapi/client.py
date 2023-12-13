import aiohttp
import ssl
import json
from os import getenv
from uuid import uuid4
from pathlib import Path

from dotenv import load_dotenv

from exceptions import ChatGPTException, GigaChatException

load_dotenv()

path_to_certificate = Path(__file__).parent.resolve().joinpath(
    'certificates/russian_trusted_root_ca_pem.crt'
)
ssl_ctx = ssl.create_default_context(cafile=path_to_certificate)


async def answer_chatgpt(data: dict):
    if data.get('messages')[0].get('role') != 'system':
        data = await set_prompt(data)
    headers = {'Authorization': f'Bearer {getenv("API_KEY")}'}
    async with aiohttp.ClientSession(
        headers=headers, conn_timeout=3.05
    ) as session:
        async with session.post(getenv('URL_GPT'), data=data) as resp:
            try:
                resp.raise_for_status()
                data_response = await resp.json()
                data.get('messages').append(
                    data_response.get('choices')[0].get('message')
                )
                return data
            except Exception:
                raise ChatGPTException


async def answer_gigachat(data: dict):
    if data.get('messages')[0].get('role') != 'system':
        data = await set_prompt(data)
    conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
    async with aiohttp.ClientSession(
        connector=conn, conn_timeout=3.05
    ) as session:
        headers_auth = {
            'Authorization': f'Basic {getenv("AUTH_CREDENTIALS")}',
            'RqUID': f'{uuid4()}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        payload = {'scope': f'{getenv("SCOPE")}'}
        async with session.post(
            getenv('AUTH_URL'), headers=headers_auth, data=payload
        ) as resp:
            try:
                resp.raise_for_status()
                data_response = await resp.json()
                token = data_response.get('access_token')
            except Exception:
                raise GigaChatException
        headers_token = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        async with session.post(getenv('URL_GIGACHAT'),
                                headers=headers_token,
                                data=json.dumps(data),
                                ) as resp:
            try:
                resp.raise_for_status()
                data_response = await resp.json()
                data.get('messages').append(
                    data_response.get('choices')[0].get('message')
                )
                return data
            except Exception:
                raise ChatGPTException


async def set_prompt(data: dict):
    message = {
        'role': 'system',
        'content': ('Ты заботливый ассистент и хочешь '
                    'помочь пользователю решить его проблему'
                    )
    }
    new_data = {
        'model': "gpt-3.5-turbo",
        'messages': [
            message
        ]
    }
    new_data['messages'].append(data['messages'])
    return new_data
