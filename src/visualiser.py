import pandas as pd
import matplotlib.pyplot as plt 
import processor as pr
from constants import GRAPH_PATH


def tg_channels_by_message_count_graph(df: pd.DataFrame) -> None: 
    data = pr.tg_channels_by_message_count(df).reset_index()
    
    plt.figure(figsize=(12, 5))
    plt.barh(
        y=data.channel_title[::-1],  
        width=data.message_count[::-1],
        color=['#D32F2F', '#1A237E', '#0D47A1', '#C62828', '#1565C0', '#B71C1C', '#F57C00']
    )
    
    plt.xlabel('Message Count', labelpad=13)
    plt.title('Telegram Channels by Message Count')
    
    plt.savefig(
        f'{GRAPH_PATH}/tg_channels_by_message_count_graph.png', 
        bbox_inches='tight',
        dpi=300
    )
    
    
def most_active_dates_graph(df: pd.DataFrame) -> None:
    data = pr.most_active_dates(df).iloc[:10].reset_index()
    
    plt.figure(figsize=(12, 5))
    plt.bar(
        data.date, 
        data.message_count,
        color="#00158B"
        )  
    plt.xticks(data.date, rotation=90)  
    
    plt.xlabel('Date')
    plt.ylabel('Message Count')
    plt.title('Most Active Dates')
    
    plt.savefig(
        f'{GRAPH_PATH}/most_active_dates_graph.png', 
        bbox_inches='tight',
        dpi=300
    )
    
    
def time_activity_graph(df: pd.DataFrame) -> pd.DataFrame:  
    data = pr.most_active_time(df).reset_index()
    
    data['hour_msc_utc'] = data.hour_msc.astype(str).str.zfill(2) + ':00\n' + data.hour_utc.astype(str).str.zfill(2) + ':00'  
    data = data.sort_values('hour_msc')
    
    plt.figure(figsize=(15, 5))
    plt.plot(
        data.hour_msc_utc,
        data.message_count,
        color='red'
    )
    
    plt.xlabel('Time (MSC / UTC)', labelpad=12, fontsize=11)
    plt.ylabel('Message Count')
    plt.title('Hourly Activity', fontsize=14)
    
    plt.savefig(
        f'{GRAPH_PATH}/time_activity_graph.png', 
        bbox_inches='tight',
        dpi=300
    )
    
    
def tg_channels_by_views_count_graph(df: pd.DataFrame) -> None:
    data = pr.tg_channels_by_views_count(df).reset_index()
    
    plt.figure(figsize=(13, 5))
    
    plt.barh(   
        data.channel_title[::-1], 
        data.total_views[::-1],
        color=['#D32F2F', '#1A237E', '#0D47A1', '#C62828', '#1565C0', '#B71C1C', '#F57C00']
    )  
    
    plt.ticklabel_format(style='plain', axis='x')  
    
    plt.xlabel('Views Count', labelpad=12, fontsize=11)
    plt.title('Telegram Channels by Views Count', fontsize=14)
    
    plt.savefig(
        f'{GRAPH_PATH}/tg_channels_by_views_count_graph.png', 
        bbox_inches='tight',
        dpi=300
    )