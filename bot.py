import os
import sys
from backend.config import discord_token, sync_server, should_sync, presence
from backend.utils.logging import log
import discord.utils
from discord.ext import commands

class rollp2Bot(commands.Bot):
    def __init__(self,
        *args,
        **kwargs):

        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        print(os.listdir('./cogs'))
        for file in os.listdir('./cogs'):  # load cogs
            if file.endswith('.py'):
                print(file)
                await bot.load_extension(f'cogs.{file[:-3]}')
        if should_sync:
            await self.tree.sync(guild=bot.get_guild(sync_server))

intents = discord.Intents.default()

bot = rollp2Bot(intents=intents, command_prefix="idontneedacommandprefixsoillsetareallylongone")  # Setting prefix

# This is what gets run when the bot stars
@bot.event
async def on_ready():
    log.info(f"Bot is ready. Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name=presence))

# Run the actual bot
try:
    bot.run(discord_token)
except discord.LoginFailure:
    log.critical("Invalid Discord Token. Please check your config file.")
    sys.exit()
except Exception as err:
    log.critical(f"Error while connecting to Discord. Error: {err}")
    sys.exit()
