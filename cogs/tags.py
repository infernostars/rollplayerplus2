# Importing our custom variables/functions from backend
from typing import Union

from cexprtk import ParseException

from bot import bot
import math, statistics, re
import random

from backend.utils.database import create_new_tag, DatabaseError, AlreadyInDatabaseError, NotInDatabaseError, \
    get_tag_by_name, increment_tag_uses, DatabasePermissionsError, edit_tag
from backend.utils.embed_templates import error_template, embed_template
from backend.utils.logging import log

import discord
from discord import app_commands
from discord.ext import commands
import cexprtk

from backend.utils.tag_parsing import process_tag_string

class TagsCog(commands.GroupCog, group_name="tags"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: tags loaded")

    @app_commands.command(name="create")
    async def create(self, interaction: discord.Interaction, name: str, code: str):
        """
        Creates a new tag.

        Parameters
        -----------
        name: str
            Name of the tag.
        code: str
            Code of the tag.
        """
        try:
            create_new_tag(interaction.user.id, name, code)
        except AlreadyInDatabaseError as e:
            interaction.response.send_message(embeds=[error_template(f"The tag {name} already exists!")])
            return

    @app_commands.command(name="create")
    async def create(self, interaction: discord.Interaction, name: str, template: str):
        """
        Creates a new tag.

        Parameters
        -----------
        name: str
            Name of the tag.
        template: str
            Code of the tag.
        """
        try:
            create_new_tag(interaction.user.id, name, template)
            await interaction.response.send_message(
                embeds=[embed_template("Tag created!", f"{name} created successfully!")])
        except AlreadyInDatabaseError as e:
            await interaction.response.send_message(embeds=[error_template(f"The tag {name} already exists!")])
            return

    @app_commands.command(name="info")
    async def info(self, interaction: discord.Interaction, name: str):
        """
        Gets info about a tag.

        Parameters
        -----------
        name: str
            Name of the tag.
        """
        try:
            tag = get_tag_by_name(name)
            username = await self.client.fetch_user(tag["creator_id"])
            await interaction.response.send_message(
                embeds=[embed_template(f"info about {name}",
                f"""
                ### made by {username} 
                ### on <t:{int(tag["created"]/1_000_000_000)}:f>
                ### last updated <t:{int(tag["updated"]/1_000_000_000)}:f>
                ### {tag["uses"]} uses
                code:
                ```
                {tag["template"]}
                ```
                """)])
        except NotInDatabaseError as e:
            await interaction.response.send_message(embeds=[error_template(f"The tag {name} doesn't exist!")])
            return

    @app_commands.command(name="edit")
    async def edit(self, interaction: discord.Interaction, name: str, template: str):
        """
        Edits a tag. You must be the owner of the tag to edit it!

        Parameters
        -----------
        name: str
            Name of the tag.
        template: str
            Code of the tag.
        """
        try:
            edit_tag(interaction.user.id, name, template)
            await interaction.response.send_message(
                embeds=[embed_template("Tag edited!", f"{name} edited successfully!")])
        except NotInDatabaseError as e:
            await interaction.response.send_message(embeds=[error_template(f"The tag {name} doesn't exist!")])
            return
        except DatabasePermissionsError as e:
            await interaction.response.send_message(embeds=[error_template(f"You aren't the owner of {name}!")])
            return

    @app_commands.command(name="run")
    async def run(self, interaction: discord.Interaction, name: str, args: Union[str, None]):
        """
        Runs a tag.

        Parameters
        -----------
        name: str
            Name of the tag.
        args: str
            Arguments, seperated by spaces [i.e. `1 2`]
        """
        try:
            tag = get_tag_by_name(name)["template"]
            if args == None:
                final_args = []
            else:
                final_args = args.split(" ")
            tag = process_tag_string(tag, final_args)
            await interaction.response.send_message(tag)
            increment_tag_uses(name)
        except NotInDatabaseError as e:
            await interaction.response.send_message(embeds=[error_template(f"The tag {name} doesn't exist!")])
            return

    @app_commands.command(name="exec")
    async def exec(self, interaction: discord.Interaction, code: str, args: Union[str, None]):
        """
        Runs a tag from code only..

        Parameters
        -----------
        code: str
            Code of the tag.
        args: str
            Arguments, seperated by spaces [i.e. `1 2`]
        """
        if args == None:
            final_args = []
        else:
            final_args = args.split(" ")
        tag = process_tag_string(code, final_args)
        await interaction.response.send_message(tag)


async def setup(client):
    await client.add_cog(TagsCog(client))
