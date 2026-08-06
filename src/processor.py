import pandas as pd 

# === BASE STATISTCIS ===

def tg_channels_by_message_count(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel').agg(message_count=('message_id', 'count'))
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
    channels = df.groupby('channel').agg(total_views=('views_count', 'sum'))
    return channels.sort_values('total_views', ascending=False)


def tg_channels_by_subscribers(df: pd.DataFrame) -> pd.DataFrame:
    ...


# === MOST INTERESTING MESSAGES === 

def most_popular_message(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel', as_index=False)['views_count'].idxmax().set_index('views_count')
    res = channels.join(df, rsuffix='_source')[['channel', 'message_id', 'date', 'text', 'views_count']]
    return res.reset_index(drop=True).sort_values('views_count', ascending=False, ignore_index=True)


def most_reacted_message(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel', as_index=False)['reactions_count'].idxmax().set_index('reactions_count')
    res = channels.join(df, rsuffix='_source')[['channel', 'message_id', 'date', 'text', 'reactions_count']]
    return res.reset_index(drop=True).sort_values('reactions_count', ascending=False, ignore_index=True)


def longest_message(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel', as_index=False)['text_length'].idxmax().set_index('text_length')
    res = channels.join(df, rsuffix='_source')[['channel', 'message_id', 'date', 'text', 'text_length']]
    return res.reset_index(drop=True).sort_values('text_length', ascending=False, ignore_index=True)


# === AUDIENCE BEHAVIOR === 

def most_used_reaction_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    copied = df.copy()
    copied = copied.loc[copied.most_used_reaction != 'CUSTOM_EMOJI']
    
    grouped = copied.groupby(['channel']).most_used_reaction.value_counts().reset_index()
    grouped['rnk'] = grouped.groupby('channel')['count'].rank(method='dense', ascending=False).astype(int)
    
    return grouped.loc[grouped.rnk == 1].drop(columns='rnk').sort_values('count', ascending=False).rename(columns={'count': 'usage'})