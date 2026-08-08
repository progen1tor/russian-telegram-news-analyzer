from telethon import types
import pandas as pd 


def reaction_handler(reaction_object: types.MessageReactions) -> tuple[int, str | None]:
    if reaction_object:
        reactions_data = reaction_object.results
        ttl_reactions_count = sum(r.count for r in reactions_data)
        try: 
            most_used_reaction = reactions_data[0].reaction.emoticon
        except AttributeError:
            most_used_reaction = 'CUSTOM_EMOJI'
        return ttl_reactions_count, most_used_reaction
    return 0, None 


def best_message_by(df: pd.DataFrame, stat_col: str) -> pd.DataFrame:
    channels = df.groupby(['channel', 'channel_title'], as_index=False)[stat_col].idxmax().set_index(stat_col)
    result = channels.join(df, rsuffix='_source')[['channel', 'channel_title', 'message_id', 'date', 'text', stat_col]]
    return result.reset_index(drop=True).sort_values(stat_col, ascending=False, ignore_index=True)