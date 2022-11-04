"""
This is the code for the bot.
Edit the file for adding more commands/customizing the bot.
"""

import os
import nextcord
from nextcord.ext import commands, ipc
from dotenv import load_dotenv

load_dotenv()

class BotClass(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc_server = ipc.Server(self, secret_key="Hercules")

    async def on_ready(self):
        """Called upon the bot is ready to use"""
        print("Bot is ready")

    async def on_ipc_ready(self):
        """Called upon the ipc server is ready to use"""
        print("The ipc server is ready")

    async def on_ipc_error(self, endpoint, error):
        """Called upon the endpoint raises an error"""
        print(f"{error} was raised by {endpoint}")

# if you use slash commands then change whatever needed, don't remove anything except the command prefix
bot = BotClass(command_prefix="!", intents=nextcord.Intents.all())

@bot.ipc_server.route()
async def get_guild_count(data):
    guild_count = len(bot.guilds)
    return guild_count

@bot.ipc_server.route()
async def get_guild_ids(data):
    guild_ids = [int(guild.id) for guild in bot.guilds]
    return guild_ids

@bot.command()
async def test(ctx):
    """
    This command is not necessary, you can remove this command and 
    add whatever command you need.
    """
    await ctx.reply("Everything is working perfectly")

if __name__ == "__main__":
    bot.ipc_server.start()
    bot.run(os.getenv("BOT_TOKEN"))