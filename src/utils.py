from telethon import types


def reaction_handler(reaction_object: types.MessageReactions) -> tuple[int, str | None]:
    if reaction_object:
        reactions_data = reaction_object.results
        ttl_reactions_count = sum(r.count for r in reactions_data)
        most_used_reaction = reactions_data[0].reaction.emoticon
        return ttl_reactions_count, most_used_reaction
    return 0, None 
