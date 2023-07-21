import discord, inflect
from discord import app_commands
from discord.ext import commands
from os import listdir
from os.path import splitext

p = inflect.engine()

# Importing our custom variables/functions from backend.py
from backend import log, embed_template, name_generator, plural


class NameGeneratorCog(commands.Cog, group_name="generators"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: name generator loaded")

    choices = listdir("data/name_generator")

    @app_commands.command(name="names")
    @app_commands.choices(kind=
                          #"greek_city.txt" -> Choice("Greek City","greek_city")
                          [app_commands.Choice(name=splitext(i)[0].replace("_"," ").title(), value=splitext(i)[0]) for i in choices])
    async def test_embed(self, interaction: discord.Interaction, kind: app_commands.Choice[str], amount: int = 10):
        """
        Generate randomized names! Capped between 1 and 25.

        Parameters
        -----------
        kind: app_commands.Choice[str]
            Type of name to generate. See options for what types exist.
        amount: int
            Amount of names to generate. 10 by default, but goes from 1-25.
        """
        amount = max(min(amount, 25), 1)
        embed = embed_template(f""" {plural("name", amount)} generated!""",
                               "\n".join([name.title() for name in name_generator(kind.value, amount)]))
        await interaction.response.send_message(embeds=[embed])


# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog (Example) to the name of your class.
async def setup(client):
    # Here, `Example` is the name of the class
    await client.add_cog(NameGeneratorCog(client))
