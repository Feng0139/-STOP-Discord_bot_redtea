from datetime import datetime
from typing import Optional

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
from discord import Embed
import discord

def syntax(command):
    cmd_and_aliases = '|'.join([str(command), *command.aliases])
    params = []

    for key, value in command.paramas.items():
        if key not in ('self', 'ctx'):
            params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')

    params = ' '.join(params)

    return f"```{cmd_and_aliases} {params}```"

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    async def cmd_help(self, ctx, command):
        embed = Embed(
            title = f'`{command}` 帮助说明',
            description = syntax(command),
            colour = discord.Color.red(),
            timestamp = datetime.now()
        )
        embed.add_field(name='命令描述', value=command.help)
        await ctx.send(embed=embed)
    
    @command(name='helps')
    async def _helps(self, ctx, cmd: Optional[str]):
        """显示这条信息."""
        if cmd is None:
            pass
        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send('未找到此命令.')


    @command(name='help', aliases=['command', 'cmd'], hidden=False)
    async def _help(self, ctx):
        # await ctx.message.delete()
        embed = Embed(
            title = '命令面板',
            description = 'RedTea 将提供以下所有帮助.',
            colour = discord.Color.red(),
            timestamp = datetime.now()
        )
        embed.set_author(name='Cyyou! 官方聊天室', url='https://discord.gg/SgEAh66', icon_url=self.bot.guild.icon_url)
        embed.set_thumbnail(url=self.bot.guild.icon_url)
        embed.set_footer(text='欢迎使用命令面板.')
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