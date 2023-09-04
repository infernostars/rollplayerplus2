# Importing our custom variables/functions from backend
from typing import Union

from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template
from backend.utils.name_generation import name_generator
from backend.utils.rolling import dice_creator, dice_error
from backend.utils.text_manipulation import plural

import discord
from discord import app_commands
from discord.ext import commands
from os import listdir
from os.path import splitext


class CreditsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: credits loaded")

    @app_commands.command(name="credits")
    async def credits(self, interaction: discord.Interaction):
        """
        Credits people who helped with the bot in a major way.
        """
        await interaction.response.send_message("""
## LegitSi
he let me add rolling pretty epic
## [fantasynamegenerators](https://www.fantasynamegenerators.com/)
used them for most of the name generation
                                                """)


async def setup(client):
    await client.add_cog(CreditsCog(client))
