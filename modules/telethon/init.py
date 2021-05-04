from telethon.sync import TelegramClient
from config import api_id, api_hash, phone
from loguru import logger
import os

if os.path.exists('/config/config.py'):
    client = TelegramClient('/config/current-session', api_id, api_hash)
else:
    client = TelegramClient('current-session', api_id, api_hash)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, code=input('Enter code sent to helper account\n>>> '))

me = client.get_me()

logger.info('Telethon init                   [ OK ]')
