import asyncio 
from datetime import datetime 
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from typing import Any 
from constants import OFFSET_DATE, CHANNELS, MSC_TZ
from utils import reaction_handler


async def tg_collector(client: TelegramClient, channel_link: str) -> list[dict[str, Any]]: 
    channel_records = []
    
    channel_info = await client.get_entity(channel_link)
    channel_full_info = await client(GetFullChannelRequest(channel_link))
    title = channel_info.title 
    subscribers_count = getattr(channel_full_info.full_chat, 'participants_count', None) 
    
    async for msg in client.iter_messages(channel_link, offset_date=OFFSET_DATE, reverse=True):
        if not msg.message:
            continue
        
        reactions_data = reaction_handler(msg.reactions)
        
        channel_records.append({
            'collected_at': datetime.now().astimezone(MSC_TZ),
            'channel': channel_link,
            'channel_title': title,
            'subscribers_count': subscribers_count,
            'message_id': msg.id, 
            'datetime_utc': msg.date, 
            'datetime_msc': msg.date.astimezone(MSC_TZ),
            'date': msg.date.astimezone(MSC_TZ).date(),  
            'text': msg.message,
            'text_length': len(msg.message),
            'has_media': bool(msg.media),
            'views_count': msg.views, 
            'forwards_count': msg.forwards,
            'reactions_count': reactions_data[0],
            'most_used_reaction': reactions_data[1]
        })
        
    return channel_records


async def gatherer(client: TelegramClient) -> list[dict[str, Any]]:
    coros = [tg_collector(client, channel) for channel in CHANNELS] 
    return await asyncio.gather(*coros)