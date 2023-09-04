# Importing our custom variables/functions from backend
from cexprtk import ParseException

import math, statistics
import random

from backend.utils.embed_templates import error_template
from backend.utils.logging import log

import discord
from discord import app_commands
from discord.ext import commands
import cexprtk


class TemplatesCog(commands.GroupCog, group_name="template"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: templates loaded")

    @app_commands.command(name="create")
    async def create(self, interaction: discord.Interaction, name: str, template: str):
        pass


async def setup(client):
    await client.add_cog(TemplatesCog(client))
