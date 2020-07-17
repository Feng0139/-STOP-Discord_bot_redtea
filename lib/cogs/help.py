from datetime import datetime

from discord.utils import get
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
import discord

# def syntax(command):
#     cmd_and_aliases = "|".join([str(command), *command.aliases])
#     return

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    # async def cmd_help(self, ctx, command):
    #     embed = Embed(
    #         title=f'{command} 帮助面板',
    #         description=syntax(command),
    #         colour=ctx.author.colour
    #     )
    #     embed.add_field(name='命令说明', value=command.help)
    
    # @command(name='test')
    # async def show_help(self, ctx, cmd: Optional[str]):
    #     """Show this message."""
    #     if cmd is None:
    #         pass
    #     else:
    #         if (command := get(self.bot.commands, name=cmd)):
    #             await self.cmd_help(ctx, command)

    #         else:
    #             await ctx.send('That command does not exist.')


    @command(name='help', aliases=['command', 'cmd'], hidden=False)
    async def _help(self, ctx):
        await ctx.message.delete()
        embed = Embed(
            title = '命令面板',
            description = 'RedTea 将提供以下所有帮助.',
            colour = discord.Color.red(),
            timestamp = datetime.now()
        )
        embed.set_author(name='Cyyou! 官方聊天室', url='https://discord.gg/SgEAh66', icon_url=self.bot.guild.icon_url)
        embed.set_thumbnail(url=self.bot.guild.icon_url)
        embed.set_footer(text='欢迎来到 Cyyou! 官方聊天室 !')
        embed.add_field(name='$help', value='查询帮助.')
        # embed.add_field(name='$echo', value='无情复读机.')
        embed.add_field(name='$hello', value='Hi!')
        embed.add_field(name='$ping', value='Pong! 39ms')
        embed.add_field(name='$roll', value='掷骰子($roll 1d6)', inline=False)
        embed.add_field(name='$create_time', value='RedTea 的创建时间.', inline=False)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('help')

def setup(bot):
    bot.add_cog(Help(bot))