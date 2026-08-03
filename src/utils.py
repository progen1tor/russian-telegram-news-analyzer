from telethon import types


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
