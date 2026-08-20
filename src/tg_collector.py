import asyncio 
import time 
from datetime import datetime 
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from typing import Any 
from src.constants import OFFSET_DATE, CHANNELS, MSC_TZ
from src.utils import reaction_handler
from src.loggers import error_logger, info_logger  


async def tg_collector(client: TelegramClient, channel_link: str) -> list[dict[str, Any]]: 
    info_logger.info(f'started collection: {channel_link}.')
    channel_records = []
    
    try: 
        channel_info = await client.get_entity(channel_link)
        channel_full_info = await client(GetFullChannelRequest(channel_link))
    except (TypeError, ValueError) as exp:  
        error_logger.error(f'{channel_link}: {exp} ({type(exp).__name__})')
        return []
    
    title = getattr(channel_info, 'title', None)
    subscribers_count = getattr(channel_full_info.full_chat, 'participants_count', None) 
    
    try: 
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
            
        info_logger.info(f'collected {len(channel_records)} messages from {channel_link}.')
        return channel_records

    except Exception as exp: 
        error_logger.error(f'failed to collect messages from {channel_link}: {exp} ({type(exp).__name__})')
        return []


async def gatherer(client: TelegramClient) -> list[list[dict[str, Any]]]:
    start = time.perf_counter()  
    
    coros = [tg_collector(client, channel) for channel in CHANNELS] 
    res = await asyncio.gather(*coros)
    
    info_logger.info(f'successfully collected messages from {len(CHANNELS)} channels in {time.perf_counter() - start:.3f} seconds.')  
    return res 