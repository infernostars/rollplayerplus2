# Importing our custom variables/functions from backend
from typing import Union

from backend.classes.dice_formatting_mode import FormattingMode, format_dice_roll
from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template
from backend.utils.rolling import dice_creator

from bot import bot

import discord
from discord import app_commands
from discord.ext import commands


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
        if dice is None:
            dice = "1d100"
        dice_removed_formatting = dice
        print(dice)
        dice_formatting_mode = FormattingMode.DEFAULT
        if dice.startswith("r"):
            dice_removed_formatting = dice[1:]
            dice_formatting_mode = FormattingMode.ROWS
        if dice.startswith("l"):
            dice_removed_formatting = dice[1:]
            dice_formatting_mode = FormattingMode.LIST_ONLY
        if dice.startswith("s"):
            dice_removed_formatting = dice[1:]
            dice_formatting_mode = FormattingMode.SUM_ONLY
        dice_result = dice_creator(dice_removed_formatting)
        #if bot.dice_error is not None:
        #    await interaction.response.send_message(embed=error_template(f"{bot.dice_error[0]}: {bot.dice_error[1]}"))
        #    bot.dice_error = None
        #    print("a")
        #    return
        dice_result = dice_result.roll()
        embed = embed_template("You rolled...")
        embed.add_field(name=dice, value=format_dice_roll(dice_formatting_mode, dice_result[1]))
        if dice_result[0] != dice_result[1]:
            embed.add_field(name=f"{dice} (raw)", value=format_dice_roll(dice_formatting_mode, dice_result[0]))
        try:
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.response.send_message(embed=error_template("Your roll's result was too long!"))

async def setup(client):
    await client.add_cog(DiceCog(client))
