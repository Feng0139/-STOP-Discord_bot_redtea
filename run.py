import discord
from discord.ext import commands
import json

# setting prefix & online status & admin id
bot = commands.Bot(command_prefix = '$', case_insensitive=True, owner_id='341273212656680960')
bot.remove_command('help')

key = json.loads(open('key.json', encoding='utf-8').read())
bot.config_token = key["token"]

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Command: $help"))

@bot.command(name='help')
async def _help(ctx, *, message=None):
    embed = discord.Embed(
        title = '帮助面板',
        description = 'RedTea 将提供以下所有帮助.',
        colour = discord.Color.red()
    )
    embed.set_author(name='Cyyou!官方聊天室', url='https://discord.gg/SgEAh66', icon_url='https://cdn.discordapp.com/icons/341447602115444746/15d9b7379cb9eb44fc047089769aff81.png?size=512')
    embed.set_thumbnail(url='https://cdn.discordapp.com/icons/341447602115444746/15d9b7379cb9eb44fc047089769aff81.png?size=512')
    embed.set_footer(text='__*欢迎来到 Cyyou! 官方聊天室 !*__')
    embed.add_field(name='$help', value='查询帮助.')
    embed.add_field(name='$echo', value='无情复读机.')
    embed.add_field(name='$hello', value='Hi!')
    embed.add_field(name='$ping', value='Pong!')
    embed.add_field(name='$create_time', value='RedTea 的创建时间.', inline=False)

    await ctx.send(embed=embed)


@bot.command(name='hello', aliases=['hi'])
async def _hello(ctx):
    await ctx.send(f'{ctx.author.mention} Hi!')

@bot.command(name='ping')
async def _ping(ctx):
    await ctx.send(f'<@{ctx.author.id}> Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='creatr_time', aliases=['c_t', 'ct'])
async def _creatr_time(ctx):
    await ctx.send('2020/04/01 22:55 Done!')

@bot.command()
async def echo(ctx, *, message=None):
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
