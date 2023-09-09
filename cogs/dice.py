# Importing our custom variables/functions from backend
from typing import Union

from backend.classes.dice_formatting_mode import FormattingMode, format_dice_roll, autoformatter
from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template
from backend.utils.rolling import dice_creator, DiceError, remap

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
    async def roll(self, interaction: discord.Interaction, dice_set: Union[str, None]):
        """
        Roll a dice! By default, rolls a 1d100.
        :param dice_set: Defaults to a singular 1d100. Add spaces to roll multiple sets of dice [i.e. `1d100 1d200`]
        """
        embed = embed_template("You rolled...")
        color_green_list = []
        color_red_list = []
        try:
            split_dice = dice_set.split(" ")
        except:
            split_dice = ["1d100"]
        if dice_set is None:
            split_dice = ["1d100"]
        for dice in split_dice:
            print(dice)
            dice_removed_formatting, dice_formatting_mode = autoformatter(dice)
            try:
                dice_obj = dice_creator(dice_removed_formatting)
                dice_result = dice_obj.roll()
            except DiceError as e:
                await interaction.response.send_message(embed=error_template(f"""## {e.id}\n{e}"""))
                return
            embed.add_field(name=dice, value=format_dice_roll(dice_formatting_mode, dice_result[1]), inline=False)
            if dice_result[0] != dice_result[1]:
                embed.add_field(name=f"{dice} (raw)", value=format_dice_roll(dice_formatting_mode, dice_result[0]), inline=True)
            try:
                color_g = int(remap(dice_obj.roll_min()[1][0], dice_obj.roll_max()[1][0], 0, 255, dice_result[1][0]))
                color_r = int(remap(dice_obj.roll_min()[1][0], dice_obj.roll_max()[1][0], 255, 0, dice_result[1][0]))
            except:
                color_g = 128
                color_r = 128
            finally:
                color_green_list.append(color_g)
                color_red_list.append(color_r)
        color_g_avg = int(sum(color_green_list) / len(color_green_list))
        color_r_avg = int(sum(color_red_list) / len(color_red_list))
        embed.color = discord.Color.from_rgb(color_r_avg, color_g_avg, 0)
        try:
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.response.send_message(embed=error_template("Your roll's result was too long!"))

async def setup(client):
    await client.add_cog(DiceCog(client))
