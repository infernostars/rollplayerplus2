# Importing our custom variables/functions from backend
from backend.calendars.logotsai_calendar import logotsai_calendar
from backend.calendars.utils import OffsetType
from backend.utils.logging import log
from backend.utils.embed_templates import embed_template, error_template

import discord
from discord import app_commands
from discord.ext import commands


class CalendarCog(commands.GroupCog, group_name="calendars"):
    def __init__(self, client):
        self.client = client

    # Use @command.Cog.listener() for an event-listener (on_message, on_ready, etc.)
    @commands.Cog.listener()
    async def on_ready(self):
        log.info("Cog: calendar loaded")

    @app_commands.command(name="convert_to")
    @app_commands.choices(calendar_set=[app_commands.Choice(name="Logotsai Calendar (offset)", value="logotsai_calendar_offset")])
    async def convert_to(self, interaction: discord.Interaction, calendar_set: app_commands.Choice[str], days: int):
        """
        Conversion to calendars in roleplays. Generally, all of them are offset so typing in "0" would be equivalent to January 1st, 1 AD in the Gregorian calendar.

        Parameters
        -----------
        calendar_set: app_commands.Choice[str]
            Type of calendar to convert to.
        days: int
            Days since January 1st, 1 AD.
        """
        embed_to_send = error_template("No date generated!")
        match calendar_set:
            case "logotsai_calendar_offset":
                embed_to_send = embed_template("The date is:", logotsai_calendar(days, OffsetType.OFFSET_CONVERT))

        await interaction.response.send_message(embed=embed_to_send)



# The `setup` function is required for the cog to work
# Don't change anything in this function, except for the
# name of the cog (Example) to the name of your class.
async def setup(client):
    # Here, `Example` is the name of the class
    await client.add_cog(CalendarCog(client))
