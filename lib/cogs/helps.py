from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
import discord

class Helps(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('helps')

def setup(bot):
    bot.add_cog(Helps(bot))