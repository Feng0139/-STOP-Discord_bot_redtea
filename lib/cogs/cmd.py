from random import choice, randint
from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
import discord

class Cmd(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='roll', aliases=['dice', 'r'])
    async def _roll(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split('d'))

        embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
        )
        embed.set_author(name=f'{ctx.author}', icon_url=ctx.author.guild.icon_url)

        if dice < 40 and value <= 100 and dice > 0 and value > 0:
            rolls = [randint(1, value) for i in range(dice)]
            embed.add_field(name=f'{die_string} = {sum(rolls)}',value='( ' + ' + '.join([str(r) for r in rolls]) + ' )')
        else:
            embed.add_field(name='生成错误',value='骰子数量不超过 40, 骰子值不超过 100.\n同时两者不可少于 0.')
        
        await ctx.send(embed=embed)

    @command(name='hello', aliases=['hi'])
    async def _hello(self, ctx):
        await ctx.send(f"{ctx.author.mention} {choice(('Hello', 'Hi', 'Hey', 'Hiya'))}{choice(('!', '~', '?', '...'))}")

    @command(name='ping')
    async def _ping(self, ctx):
        await ctx.send(f'<@{ctx.author.id}> Pong! {round(self.bot.latency * 1000)}ms')

    @command(name='create_time', aliases=['c_t', 'ct'])
    async def _create_time(self, ctx):
        await ctx.send('> 2020/04/01 22:55 Done!')

    @command(name='echo', aliases=['say'], hidden=True)
    async def _echo(self, ctx, *, message=None):
        message = message or '$echo: 请提供必要的文字内容.'
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('cmd')

def setup(bot):
    bot.add_cog(Cmd(bot))