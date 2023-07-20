import discord, inflect
from discord import app_commands
from discord.ext import commands

p = inflect.engine()

# Importing our custom variables/functions from backend.py
from backend import log, embed_template, greek_name_generator, plural


class NameGeneratorCog(commands.GroupCog, group_name="generators"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: name generator loaded")

    @app_commands.command(name="greek-city", description="Generate greek city names! Capped at 1 and 25.")
    async def test_embed(self, interaction: discord.Interaction, amount: int = 10):
        amount = max(min(amount, 25), 1)
        embed = embed_template(f"""Greek city {plural("name", amount)} generated!""", "\n".join(greek_name_generator(amount)))
        await interaction.response.send_message(embeds=[embed])


# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog (Example) to the name of your class.
async def setup(client):
    # Here, `Example` is the name of the class
    await client.add_cog(NameGeneratorCog(client))
