import discord
from discord.ext import commands

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

#bot = discord.Client()
bot = commands.Bot(command_prefix = '$')
bot.config_token = read_token()


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Cyyou! OCR'))

@bot.command(name='hello', aliases=['hi', 'Hi', 'Hello'])
async def _ping(ctx):
    await ctx.send(f'{ctx.author.mention} Hi!')

@bot.command(name='ping')
async def _ping(ctx):
    await ctx.send(f'<@{ctx.author.id}> Pong!')

@bot.command(name='creatr_time')
async def _creatr_time(ctx):
    await ctx.send('2020/04/01 22:55 Done!')

#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    if message.content.startswith('$create_time'):
#        await message.channel.send('2020/04/01 22:55 Done!')

bot.run(bot.config_token)
