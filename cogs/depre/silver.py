from backend.utils.embed_templates import embed_template
from backend.utils.logging import log
from backend.roleplays.silverwinds.core import MineEvent

import discord
from discord import app_commands
from discord.ext import commands


class SilverWindsCog(commands.GroupCog, group_name="silver"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: silver winds loaded")

    @app_commands.command(name="mine")
    async def mine(self, interaction: discord.Interaction, depth: int, picklevel: int, times: int = 32):
        """
        Replies with ores you can mine.

        Arguments:
            depth: Sets the depth you're mining at, between +256 and -512.
            picklevel: Pickaxe level, currently between 1-10.
        """
        mine_event = MineEvent(depth, picklevel, times)
        mine_results = mine_event.mine()
        if not mine_results:
            merged_string = "Nothing! :D"
        merged_string = '\n'.join(str(ore) for ore in mine_results)
        await interaction.response.send_message(embed=embed_template("You mined...", merged_string))


# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog (Example) to the name of your class.
async def setup(client):
    # Here, `Example` is the name of the class
    await client.add_cog(SilverWindsCog(client))
