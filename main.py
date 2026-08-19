from src.client import client
from src.tg_collector import gatherer
import src.cleaner as cln
import src.processor as prc 
import src.visualiser as vlr
from src.constants import CSV_RES_PATH

from typing import Any 

import asyncio
import pandas as pd 
import os 

# from tg_collector.py 
async def main() ->  list[dict[str, Any]]:
    async with client: 
        return await gatherer(client)

res = asyncio.run(main())
flattened_res = [dct for channel in res for dct in channel]

# from cleaner.py 
raw_news = pd.DataFrame(flattened_res)
news = cln.sorter(cln.stripper(cln.type_corrector(raw_news)))


# making dir  
os.makedirs(CSV_RES_PATH, exist_ok=True)


# base statistics:
prc.tg_channels_by_message_count(news).to_csv(f'{CSV_RES_PATH}/tg_channels_by_message_count.csv')
prc.most_active_dates(news).to_csv(f'{CSV_RES_PATH}/most_active_dates.csv')
prc.most_active_time(news).to_csv(f'{CSV_RES_PATH}/most_active_time.csv')

# channels popularity: 
prc.tg_channels_by_views_count(news).to_csv(f'{CSV_RES_PATH}/tg_channels_by_views_count.csv')
prc.tg_channels_by_subscribers(news).to_csv(f'{CSV_RES_PATH}/tg_channels_by_subscribers.csv')

# most interesting messages 
prc.most_popular_message(news).to_csv(f'{CSV_RES_PATH}/most_popular_message.csv', index=False)
prc.most_reacted_message(news).to_csv(f'{CSV_RES_PATH}/most_reacted_message.csv', index=False)
prc.longest_message(news).to_csv(f'{CSV_RES_PATH}/longest_message.csv', index=False)

# audience behavior: 
prc.most_used_reaction_by_channel(news).to_csv(f'{CSV_RES_PATH}/most_used_reaction_by_channel.csv', index=False)
prc.top_5_reactions(news).to_csv(f'{CSV_RES_PATH}/top_5_reactions.csv')
prc.engagement_rate(news).to_csv(f'{CSV_RES_PATH}/engagement_rate.csv')
prc.average_views_per_subscriber(news).to_csv(f'{CSV_RES_PATH}/average_views_per_subscriber.csv')
prc.virality_of_publications(news).to_csv(f'{CSV_RES_PATH}/virality_of_publications.csv', index=False)


# visualization: 
vlr.tg_channels_by_message_count_graph(news)
vlr.most_active_dates_graph(news)
vlr.time_activity_graph(news)
vlr.tg_channels_by_views_count_graph(news)
vlr.average_views_per_subscriber_graph(news)
vlr.top_5_reactions_graph(news)