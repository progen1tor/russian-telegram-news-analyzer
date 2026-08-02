import datetime 

CONFIG_PATH = 'russian-telegram-news-analyzer/config.json'

OFFSET_DATE = datetime.datetime.today() - datetime.timedelta(days=90)
CHANNELS: list[str] = [
    'https://t.me/toporlive', 
    'https://t.me/rt_russian', 
    'https://t.me/rbc_news', 
    'https://t.me/ria_novosti_russiya',
    'https://t.me/rian_ru',
    'https://t.me/bazabazon',
    'https://t.me/novosti_russia360'
    ]