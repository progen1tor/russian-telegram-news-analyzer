from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME

client = TelegramClient(
    api_id=API_ID, 
    api_hash=API_HASH, 
    session=SESSION_NAME
)