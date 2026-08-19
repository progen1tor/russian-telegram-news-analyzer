import warnings 
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt 
import src.processor as pr
from src.constants import GRAPH_PATH, PLOT_COLORS


def tg_channels_by_message_count_graph(df: pd.DataFrame) -> None: 
    data = pr.tg_channels_by_message_count(df).reset_index()
    
    plt.figure(figsize=(12, 5))
    plt.barh(
        y=data.channel_title[::-1],  
        width=data.message_count[::-1],
        color=PLOT_COLORS
    )
    
    plt.xlabel('Message Count', labelpad=13)
    plt.title('Telegram Channels by Message Count')
    
    plt.savefig(
        f'{GRAPH_PATH}/tg_channels_by_message_count_graph.png', 
        bbox_inches='tight',
        dpi=300
    )
    plt.close()
    
    
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
    plt.close()
    
    
def time_activity_graph(df: pd.DataFrame) -> None:  
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
    plt.close()
    
    
def tg_channels_by_views_count_graph(df: pd.DataFrame) -> None:
    data = pr.tg_channels_by_views_count(df).reset_index()
    
    plt.figure(figsize=(13, 5))
    
    plt.barh(   
        data.channel_title[::-1], 
        data.total_views[::-1],
        color=PLOT_COLORS
    )  
    
    plt.ticklabel_format(style='plain', axis='x')  
    
    plt.xlabel('Views Count', labelpad=12, fontsize=11)
    plt.title('Telegram Channels by Views Count', fontsize=14)
    
    plt.savefig(
        f'{GRAPH_PATH}/tg_channels_by_views_count_graph.png', 
        bbox_inches='tight',
        dpi=300
    )
    plt.close()
    
    
def average_views_per_subscriber_graph(df: pd.DataFrame) -> None:
    data = pr.average_views_per_subscriber(df).reset_index()
    
    _, ax = plt.subplots(figsize=(10, 5))
    
    scatter_colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02', '#a6761d']
    
    for ch, color in zip(data.channel_title, scatter_colors):
        pt = data.loc[data.channel_title == ch]
        ax.scatter(pt.subscribers, pt.views_to_subscribers_ratio, label=ch, color=color, s=110, marker='s')
        
    ax.legend()
    ax.grid(alpha=.3, ls='--')
    
    ax.ticklabel_format(style='plain')
    
    ax.set_title('Average Publication Views / Subscribers')  
    ax.set_xlabel('Subscribers')
    ax.set_ylabel('Views / Subscribers', labelpad=13)
    
    plt.savefig(
        f'{GRAPH_PATH}/average_views_per_subscriber_graph.png', 
        bbox_inches='tight',
        dpi=300
    )
    plt.close()
    
    
def top_5_reactions_graph(df: pd.DataFrame) -> None: 
    with warnings.catch_warnings():
        warnings.filterwarnings(action='ignore', module='seaborn')

        data = pr.top_5_reactions(df)
        ax = sns.heatmap(
            data,
            annot=True, fmt='d',
            cmap='magma'
            )
        
        for lbl in ax.get_xticklabels():
            lbl.set_fontfamily('Segoe UI Emoji')
            
        ax.set_title('Top-5 Reaction Usage by Channel', pad=10)  
        ax.set_xlabel('Reaction', labelpad=13)
        ax.set_ylabel('')
        
        plt.savefig(
            f'{GRAPH_PATH}/top_5_reactions_graph.png', 
            bbox_inches='tight',
            dpi=300
        )
        plt.close()