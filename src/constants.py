from zoneinfo import ZoneInfo
import datetime 

GRAPH_PATH = 'data/graphs'
CSV_RES_PATH = 'data/results_csv'

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

MSC_TZ = ZoneInfo('Europe/Moscow')

TOP_MESSAGES = 20

PLOT_COLORS = ['#D32F2F', '#1A237E', '#0D47A1', '#C62828', '#1565C0', '#B71C1C', '#F57C00']