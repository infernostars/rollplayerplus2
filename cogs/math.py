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


class MathCog(commands.GroupCog, group_name="math"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: math loaded")

    @app_commands.command(name="eval")
    async def eval(self, interaction: discord.Interaction, equation: str):
        """
        Solves math equation!

        Parameters
        -----------
        equation: str
            Equation to solve
        """

        # funcs for st.functions
        def cexprtk_random(low, high):
            return random.uniform(low, high)

        solution = False
        symbol_table = cexprtk.Symbol_Table(variables={"pi": math.pi, "e": math.e}, functions={"rand": cexprtk_random})

        try:  # use the Expression class instead with the updated symbol_table
            expr = cexprtk.Expression(equation, symbol_table)
            solution = expr()  # to evaluate the expression just call it
        except ParseException as e:
            await interaction.response.send_message(embed=error_template(f"Parsing error: {e}"))
            raise
        except Exception as e:
            await interaction.response.send_message(embed=error_template(f"{type(e)}: {e}"))
            raise

        if type(solution) == float:
            if solution % 1 == 0:
                solution = int(solution)

        # Use `await interaction.response.send_message()` to send a message
        await interaction.response.send_message(f"answer: **{solution}**")


async def setup(client):
    await client.add_cog(MathCog(client))
