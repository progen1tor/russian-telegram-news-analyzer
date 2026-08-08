import pandas as pd
from .utils import best_message_by

# === BASE STATISTCIS ===

def tg_channels_by_message_count(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby(['channel', 'channel_title']).agg(message_count=('message_id', 'count'))
    return channels.sort_values('message_count', ascending=False)


def most_active_dates(df: pd.DataFrame) -> pd.DataFrame:
    dates = df.groupby('date').agg(message_count=('message_id', 'nunique'))
    return dates.sort_values('message_count', ascending=False)


def most_active_time(df: pd.DataFrame) -> pd.DataFrame:
    copied = df.copy()
    
    copied['hour_utc'] = df.datetime_utc.dt.hour 
    copied['hour_msc'] = df.datetime_msc.dt.hour 
    
    hours = copied.groupby(['hour_utc', 'hour_msc']).agg(message_count=('message_id', 'nunique'))
    return hours.sort_values('message_count', ascending=False)


# === CHANNELS POPULARITY === 

def tg_channels_by_views_count(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby(['channel', 'channel_title']).agg(total_views=('views_count', 'sum'))
    return channels.sort_values('total_views', ascending=False)


def tg_channels_by_subscribers(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['channel', 'channel_title']).subscribers_count.max().sort_values(ascending=False).to_frame()


# === MOST INTERESTING MESSAGES === 

def most_popular_message(df: pd.DataFrame) -> pd.DataFrame:
    return best_message_by(df, 'views_count').head(20)  # выводить лучше первые 20

def most_reacted_message(df: pd.DataFrame) -> pd.DataFrame:
    return best_message_by(df, 'reactions_count').head(20)

def lonhgest_message(df: pd.DataFrame) -> pd.DataFrame:
    return best_message_by(df, 'text_length').head(20)


# === AUDIENCE BEHAVIOR === 

def most_used_reaction_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    copied = df.copy()
    copied = copied.loc[copied.most_used_reaction != 'CUSTOM_EMOJI']
    
    grouped = copied.groupby(['channel', 'channel_title']).most_used_reaction.value_counts().reset_index()
    grouped['rnk'] = grouped.groupby('channel')['count'].rank(method='dense', ascending=False).astype(int)
    
    return grouped.loc[grouped.rnk == 1].drop(columns='rnk').sort_values('count', ascending=False).rename(columns={'count': 'usage'})