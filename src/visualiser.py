import pandas as pd
import matplotlib.pyplot as plt 
from constants import GRAPH_PATH


def tg_channels_by_message_count_graph(df: pd.DataFrame) -> None: 
    copied = df.copy().reset_index()  
    
    plt.barh(
        y=copied.channel_title[::-1],  
        width=copied.message_count[::-1],
        color=['#D32F2F', '#1A237E', '#0D47A1', '#C62828', '#1565C0', '#B71C1C', '#F57C00']
    )
    
    plt.savefig(
        f'{GRAPH_PATH}/tg_channels_by_message_count_graph.png', 
        bbox_inches='tight',
        dpi=300
        )