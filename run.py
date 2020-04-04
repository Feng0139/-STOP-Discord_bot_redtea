import discord
from discord.ext import commands
import json
import mysql.connector

key = json.loads(open('key.json', encoding='utf-8').read())

bot = commands.Bot(command_prefix = '$', case_insensitive=True, owner_id='341273212656680960')
bot.config_token = key["token"]
# bot.config_token = read_token()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Cyyou! OCR Code: SgEAh66"))

@bot.command(name='hello', aliases=['hi'])
async def _hello(ctx):
    """
    Hi!
    """
    await ctx.send(f'{ctx.author.mention} Hi!')

@bot.command(name='ping')
async def _ping(ctx):
    """
    Pong!
    """
    await ctx.send(f'<@{ctx.author.id}> Pong!')

@bot.command(name='creatr_time', aliases=['c_t', 'ct'])
async def _creatr_time(ctx):
    """
    Robot creation time
    """
    await ctx.send('2020/04/01 22:55 Done!')

@bot.command()
async def echo(ctx, *, message=None):
    """
    Let the robot say something
    """
    message = message or '请提供必要的文字内容.'
    await ctx.message.delete()
    await ctx.send(message)

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    if message.content.startswith('$create_time'):
#        await message.channel.send('2020/04/01 22:55 Done!')

bot.run(bot.config_token)
