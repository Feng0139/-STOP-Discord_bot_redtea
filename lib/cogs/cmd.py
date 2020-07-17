from random import choice, randint

from discord.ext.commands import Cog
from discord.ext.commands import command
import discord

class Cmd(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='roll', aliases=['dice'])
    async def _roll(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split('d'))
        if dice <= 39:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(f'{ctx.author.mention}\n> ' + ' + '.join([str(r) for r in rolls]) + f' = {sum(rolls)}')
        else:
            await ctx.send(f'{ctx.author.mention}\n> 生成错误，请尝试少一点的骰子数量.')

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