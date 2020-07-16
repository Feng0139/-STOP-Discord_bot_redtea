from discord.ext.commands import Cog
from discord.ext.commands import command
import discord

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
    
    @command(name='help', aliases=['command', 'cmd'], hidden=False)
    async def _help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title = '命令面板',
            description = 'RedTea 将提供以下所有帮助.',
            colour = discord.Color.red()
        )
        embed.set_author(name='Cyyou! 官方聊天室', url='https://discord.gg/SgEAh66', icon_url=self.bot.guild.icon_url)
        embed.set_thumbnail(url=self.bot.guild.icon_url)
        embed.set_footer(text='欢迎来到 Cyyou! 官方聊天室 !')
        embed.add_field(name='$helps', value='查询帮助.')
        embed.add_field(name='$echo', value='无情复读机.')
        embed.add_field(name='$hello', value='Hi!')
        embed.add_field(name='$ping', value='Pong! 39ms')
        embed.add_field(name='$create_time', value='RedTea 的创建时间.', inline=False)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('help')

def setup(bot):
    bot.add_cog(Help(bot))