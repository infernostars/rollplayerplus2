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


class DiceCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: dice loaded")

    @app_commands.command(name="roll")
    async def roll(self, interaction: discord.Interaction, dice: Union[str, None]):
        """
        Roll a dice! By default, rolls a 1d100.
        """
        print(dice)
        if dice == None:
            dice = "1d100"
        dice_result = dice_creator(dice).roll()
        if dice_result == int:
            await interaction.response.send_message(embed=error_template(f"{dice_error[0]}: {dice_error[1]}"))
            return
        dice_raw_format = ", ".join([f"{x}" for x in dice_result[0][1]])
        dice_format = ", ".join([f"{x}" for x in dice_result[1][1]])
        embed = embed_template("You rolled...")
        embed.add_field(name=dice, value=f"{dice_format} (total: {dice_result[1][0]})")
        if dice_result[0][0] != dice_result[1][0]:
            embed.add_field(name=f"{dice} (raw)", value=f"{dice_raw_format} (total: {dice_result[0][0]})")

        await interaction.response.send_message(embed=embed)


async def setup(client):
    await client.add_cog(DiceCog(client))
