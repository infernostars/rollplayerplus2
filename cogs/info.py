# Importing our custom variables/functions from backend
from typing import Union

from backend.config import version
from backend.utils.logging import log

import discord
from discord import app_commands
from discord.ext import commands


class InfoCog(commands.GroupCog, group_name="info"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: info loaded")

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

    @app_commands.command(name="version")
    async def version(self, interaction: discord.Interaction):
        """
        Get the bot's version.
        """
        await interaction.response.send_message(f"""
    Rollplayer, patron saint of Vorigaria, version **{version}**""")

    @app_commands.command(name="cogs")
    async def cogs(self, interaction: discord.Interaction):
        """
        Get the bot's running cogs.
        """
        cogs = self.client.coglist
        cogs = '\n'.join(cogs)
        await interaction.response.send_message(f"""
{cogs}""")


async def setup(client):
    await client.add_cog(InfoCog(client))
