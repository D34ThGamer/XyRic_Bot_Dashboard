"""
We will create some functions in this file which will make our work easier.
"""

async def check_guild(guild_id: int, discord):
    """A helper function to check if the guild is a proper guild to work with"""
    user_guilds = await discord.fetch_guilds()
    guild = None
    for each_guild in user_guilds:
        if int(each_guild.id) == int(guild_id):
            guild = each_guild
    return guild