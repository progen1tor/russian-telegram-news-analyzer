import pandas as pd 
import string 


def tg_channels_by_message_count(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel').agg(message_count=('message_id', 'count'))
    return channels.sort_values('message_count', ascending=False)


def most_active_time(df: pd.DataFrame) -> pd.DataFrame:
    copied = df.copy()
    
    copied['hour_utc'] = df.datetime_utc.dt.hour 
    copied['hour_msc'] = df.datetime_msc.dt.hour 
    
    hours = copied.groupby(['hour_utc', 'hour_msc']).agg(message_count=('message_id', 'nunique'))
    return hours.sort_values('message_count', ascending=False)


def tg_channels_by_views_count(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel').agg(total_views=('views_count', 'sum'))
    return channels.sort_values('total_views', ascending=False)


def most_popular_message(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel', as_index=False)['views_count'].idxmax().set_index('views_count')
    res = channels.join(df, rsuffix='_source')[['channel', 'message_id', 'date', 'text', 'views_count']]
    return res.reset_index(drop=True).sort_values('views_count', ascending=False, ignore_index=True)


def most_reacted_message(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel', as_index=False)['reactions_count'].idxmax().set_index('reactions_count')
    res = channels.join(df, rsuffix='_source')[['channel', 'message_id', 'date', 'text', 'reactions_count']]
    return res.reset_index(drop=True).sort_values('reactions_count', ascending=False, ignore_index=True)


def lonhgest_message(df: pd.DataFrame) -> pd.DataFrame:
    channels = df.groupby('channel', as_index=False)['text_length'].idxmax().set_index('text_length')
    res = channels.join(df, rsuffix='_source')[['channel', 'message_id', 'date', 'text', 'text_length']]
    return res.reset_index(drop=True).sort_values('text_length', ascending=False, ignore_index=True)


def most_popular_themes_by_keywords(df: pd.DataFrame) -> pd.DataFrame:
    copied = df.copy()[['channel', 'message_id', 'text']]
    
    copied.text = copied.text.str.replace(rf'[{string.punctuation}]', '', regex=True).str.split()
    copied = copied.explode('text')
    copied['is_not_word'] = ~(copied.text.str.match(pat=r'[A-Za-zА-Яа-я]'))
    copied = copied.loc[~(copied.is_not_word)].drop(columns='is_not_word')
    
    groups = copied.groupby('text').agg(keyword_count=('message_id', 'count'))
    
    return groups.sort_values('keyword_count', ascending=False)