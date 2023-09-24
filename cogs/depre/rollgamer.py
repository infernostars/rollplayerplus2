# Importing our custom variables/functions from backend
from typing import Union

from backend.config import version
from backend.utils.logging import log

import discord
from discord import app_commands
from discord.ext import commands


class RollgamerCog(commands.GroupCog, group_name="rollgamer"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: info loaded")

    @app_commands.command(name="create")
    async def credits(self, interaction: discord.Interaction):
        pass



async def setup(client):
    await client.add_cog(RollgamerCog(client))
