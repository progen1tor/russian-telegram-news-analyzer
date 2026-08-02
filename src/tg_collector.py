import asyncio 
from datetime import datetime 
from telethon import TelegramClient
from typing import Any 
from constants import OFFSET_DATE, CHANNELS
from utils import reaction_handler


async def tg_collector(client: TelegramClient, channel_link: str) -> list[dict[str, Any]]: 
    channel_records = []
    
    async for msg in client.iter_messages(channel_link, offset_date=OFFSET_DATE, reverse=True):
        reactions_data = reaction_handler(msg.reactions)
        
        channel_records.append({
            'collected_at': datetime.now(),
            'channel': channel_link,
            'message_id': msg.id, 
            'datetime': msg.date, 
            'date': msg.date.date(),  
            'text': msg.message,
            'text_length': len(msg.message),
            'has_media': bool(msg.media),
            'views_count': msg.views, 
            'forwards_count': msg.forwards,
            'reactions_count': reactions_data[0],
            'most_used_reaction': reactions_data[1]
        })  # ? collected_at ? 
        
    return channel_records


async def gatherer(client: TelegramClient) -> list[dict[str, Any]]:
    coros = []
    for channel in CHANNELS:
        coros.append(tg_collector(client, channel))
        
    return await asyncio.gather(*coros)