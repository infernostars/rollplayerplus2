import discord
from discord import app_commands
from discord.ext import commands

# Importing our custom variables/functions from backend
from backend import log, embed_template, error_template


class TestCog(commands.GroupCog, group_name="testing"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: testing loaded")

    # Use @commands.slash_command() for a slash-command
    # I recommend using only slash-commands for your bot.
    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        """
        Replies with "pong".
        """
        # Use `await interaction.response.send_message()` to send a message
        await interaction.response.send_message("pong")

    @app_commands.command(name="testembed")
    async def test_embed(self, interaction: discord.Interaction):
        """
        Testing embed for if things go successfully.
        """
        embed = embed_template("Test embed", "Something went right!")
        await interaction.response.send_message(embeds=[embed])

    @app_commands.command(name="testembed2")
    async def test_embed2(self, interaction: discord.Interaction):
        """
        Testing embed for if things go wrong.
        """
        error_embed = error_template("Oops! Something went wrong!")
        await interaction.response.send_message(embeds=[error_embed])


# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog (Example) to the name of your class.
async def setup(client):
    # Here, `Example` is the name of the class
    await client.add_cog(TestCog(client))
