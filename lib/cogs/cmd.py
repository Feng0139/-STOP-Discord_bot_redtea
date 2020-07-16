from discord.ext.commands import Cog, command
import discord

class Cmd(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='hello', aliases=['hi'])
    async def _hello(self, ctx):
        await ctx.send(f'{ctx.author.mention} Hi!')

    @command(name='ping')
    async def _ping(self, ctx):
        await ctx.send(f'<@{ctx.author.id}> Pong! {round(bot.latency * 1000)}ms')

    @command(name='create_time', aliases=['c_t', 'ct'])
    async def _create_time(self, ctx):
        await ctx.send('> 2020/04/01 22:55 Done!')

    @command(name='echo', aliases=['say'])
    async def _echo(self, ctx, *, message=None):
        message = message or '$echo: 请提供必要的文字内容.'
        await ctx.message.delete()
        await ctx.send(message)

    @command(name='help', aliases=['command','cmd'], hidden=False)
    async def _help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title = '帮助面板',
            description = 'RedTea 将提供以下所有帮助.',
            colour = discord.Color.red()
        )
        embed.set_author(name='Cyyou! 官方聊天室', url='https://discord.gg/SgEAh66', icon_url='https://cdn.discordapp.com/icons/341447602115444746/15d9b7379cb9eb44fc047089769aff81.png?size=512')
        embed.set_thumbnail(url='https://cdn.discordapp.com/icons/341447602115444746/15d9b7379cb9eb44fc047089769aff81.png?size=512')
        embed.set_footer(text='欢迎来到 Cyyou! 官方聊天室 !')
        embed.add_field(name='$help', value='查询帮助.')
        embed.add_field(name='$echo', value='无情复读机.')
        embed.add_field(name='$hello', value='Hi!')
        embed.add_field(name='$ping', value='Pong! 39ms')
        embed.add_field(name='$create_time', value='RedTea 的创建时间.', inline=False)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('cmd')

def setup(bot):
    bot.add_cog(Cmd(bot))