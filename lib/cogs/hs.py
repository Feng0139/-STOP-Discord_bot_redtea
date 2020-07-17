from datetime import datetime
from typing import Optional

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
from discord import Embed
import discord

# def syntax(command):
#     cmd_and_aliases = '|'.join([str(command), *command.aliases])
#     params = []

#     for key, value in command.paramas.items():
#         if key not in ('self', 'ctx'):
#             params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')

#     params = ' '.join(params)

#     return f"```{cmd_and_aliases} {params}```"

class Hs(Cog):
    def __init__(self, bot):
        self.bot = bot

    # async def cmd_help(self, ctx, command):
    #     embed = Embed(
    #         titl = f'{command} 帮助',
    #         description = syntax(command),
    #         colour = discord.Color.red(),
    #         timestamp = datetime.now()
    #     )
    #     embed.add_field(name='命令描述', value=command.help)
    #     await ctx.send(embed=embed)

    @command(name='helps')
    async def _help(self, ctx, cmd: Optional[str]):
        """显示这条信息."""
        if cmd is None:
            pass
        else:
            # if (command := get(self.bot.commands, name=cmd)):
            #     await self.cmd_help(ctx, command)
            # else:
            #     await ctx.send('未找到此命令.')
            pass

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('hs')

def setup(bot):
    bot.add_cog(Hs(bot))