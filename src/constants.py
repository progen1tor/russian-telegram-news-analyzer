import datetime 

CONFIG_PATH = 'russian-telegram-news-analyzer/config.json'
RAW_JSON_PATH = 'russian-telegram-news-analyzer/data/raw.json'

OFFSET_DATE = datetime.date.today() - datetime.timedelta(days=2)
CHANNELS: list[str]