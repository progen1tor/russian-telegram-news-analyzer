import pandas as pd
from .utils import grouper, best_message_by

# === BASE STATISTCIS ===

def tg_channels_by_message_count(df: pd.DataFrame) -> pd.DataFrame:
    channels = grouper(df).agg(message_count=('message_id', 'count'))
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
    channels = grouper(df).agg(total_views=('views_count', 'sum'))
    return channels.sort_values('total_views', ascending=False)


def tg_channels_by_subscribers(df: pd.DataFrame) -> pd.DataFrame:
    return grouper(df).subscribers_count.max().sort_values(ascending=False).to_frame()


# === MOST INTERESTING MESSAGES === 

def most_popular_message(df: pd.DataFrame) -> pd.DataFrame:
    return best_message_by(df, 'views_count').head(20)  # выводить лучше первые 20

def most_reacted_message(df: pd.DataFrame) -> pd.DataFrame:
    return best_message_by(df, 'reactions_count').head(20)

def longest_message(df: pd.DataFrame) -> pd.DataFrame:
    return best_message_by(df, 'text_length').head(20)


# === AUDIENCE BEHAVIOR === 

def most_used_reaction_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    without_custom_reacts = df.loc[df.most_used_reaction != 'CUSTOM_EMOJI']
    
    grouped = grouper(without_custom_reacts).most_used_reaction.value_counts().reset_index()
    grouped['rnk'] = grouped.groupby('channel')['count'].rank(method='dense', ascending=False).astype(int)
    
    return grouped.loc[grouped.rnk == 1].drop(columns='rnk').sort_values('count', ascending=False).rename(columns={'count': 'usage'})


def top_5_reactions(df: pd.DataFrame) -> pd.DataFrame:
    without_custom_reacts = df.loc[df.most_used_reaction != 'CUSTOM_EMOJI']
    reactions = without_custom_reacts.groupby('most_used_reaction').agg(reaction_count=('most_used_reaction', 'count'))
    return reactions.sort_values('reaction_count', ascending=False).iloc[:5]


def engagement_rate(df: pd.DataFrame) -> pd.DataFrame:
    channels = grouper(df).agg(
        ttl_views=('views_count','sum'),
        ttl_forwards=('forwards_count','sum'),
        ttl_reactions=('reactions_count','sum')
        )
    
    channels['forward_percent'] = round(channels.ttl_forwards / channels.ttl_views * 100, 2) 
    channels['reaction_percent'] = round(channels.ttl_reactions / channels.ttl_views * 100, 2)
    channels['engagement_rate'] = round((channels.ttl_forwards + channels.ttl_reactions)  / channels.ttl_views * 100, 2)
    
    cols = ['forward_percent', 'reaction_percent', 'engagement_rate']
    return channels[cols].sort_values(cols[::-1], ascending=False)


def average_views_per_subscriber(df: pd.DataFrame) -> pd.DataFrame:
    channels = grouper(df).agg(
        avg_publication_views=('views_count', 'mean'),
        subscribers=('subscribers_count', 'max')
    )
    
    channels['views_to_subscribers_ratio'] = (channels.avg_publication_views / channels.subscribers).round(3)
    return channels[['subscribers', 'views_to_subscribers_ratio']].sort_values('views_to_subscribers_ratio', ascending=False)


def virality_of_publications(df: pd.DataFrame) -> pd.DataFrame:
    copied = df.copy()
    
    copied['virality'] = (copied.forwards_count / copied.views_count).round(3)
    return copied[['channel', 'channel_title', 'text', 'virality']].sort_values(['virality', 'text'], ascending=[False, True]).iloc[:10]