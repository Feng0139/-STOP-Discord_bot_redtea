import discord
from discord.ext import commands
import json
import mysql.connector

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

def relink_mydb():
    return mysql.connector.connect(host=key["ipaddress"],user=key["username"],passwd=key["password"],database=key["username"])

key = json.loads(open('key.json', encoding='utf-8').read())

# setting prefix & online status & admin id
bot = commands.Bot(command_prefix = '$', case_insensitive=True, owner_id='341273212656680960')
bot.config_token = key["token"]
# bot.config_token = read_token()

mydb = relink_mydb()
mycursor = mydb.cursor()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Command: $help"))

@bot.command()
async def displayEmbed(ctx, *, message=None):
    """
    Embed Test
    """
    embed = discord.Embed(
        title = 'Title',
        description = 'this is a description.',
        colour = discord.Color.blue()
    )

    embed.set_footer(text="this is a footer.")
    embed.set_image(url='https://www.teeworlds.cn/images/logo.png')
    embed.set_thumbnail(url='https://www.teeworlds.cn/images/logo.png')
    embed.set_author(name='Author Name', icon_url='https://www.teeworlds.cn/images/logo.png')
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=False)
    embed.add_field(name='Field Name', value='Field Value', inline=True)

    await ctx.send(embed=embed)
    
@bot.event
async def help(ctx, *, message=None):
    """
    Help panel
    """
    embed = discord.Embed(
        title = '帮助面板',
        description = 'RedTea 将提供以下所有帮助.',
        colour = discord.Color.red()
    )
    embed.set_author(name='Cyyou!官方聊天室', url='https://discord.gg/SgEAh66', icon_url='https://cdn.discordapp.com/icons/341447602115444746/15d9b7379cb9eb44fc047089769aff81.png?size=512')
    embed.set_thumbnail(url='https://cdn.discordapp.com/icons/341447602115444746/15d9b7379cb9eb44fc047089769aff81.png?size=512')
    embed.set_footer(text='欢迎来到 Cyyou! 官方聊天室 !')
    embed.add_field(name='help', value='查询帮助.', inline=False)
    embed.add_field(name='echo', value='无情复读机.', inline=False)
    embed.add_field(name='hello', value='Hi!', inline=False)
    embed.add_field(name='ping', value='Pong!', inline=False)
    embed.add_field(name='create_time', value='RedTea 的创建时间.', inline=False)
    #embed.add_field(name='searchn', value='按 用户名 查找信息.', inline=False)
    #embed.add_field(name='searchu', value='按 UID 查找信息.', inline=False)

    await ctx.send(embed=embed)


@bot.command(aliases=['search'])
async def searchu(ctx, *, message=None):
    """
    Search in UID(num)
    """
    try:
        # mydb.ping()

        sql = "select uid, username, newpoints, postnum, threadnum from `tws_users` where uid = " + message + ";"

        mycursor.ping(reconnect=True)
        
        mycursor.execute(sql)
        buf = mycursor.fetchone()
        await ctx.send(f'{ctx.author.mention}\n```UID: {buf[0]}\nUser: {buf[1]}\nPoints: {buf[2]}\nPost Num: {buf[3]}\nThread Num: {buf[4]}```')
    except:
        # mydb = relink_mydb()
        await ctx.send(f'{ctx.author.mention} 无法查询')

@bot.command()
async def searchn(ctx, *, message=None):
    """
    Search in userName(str)
    """
    try:
        sql = "select uid, username, newpoints, postnum, threadnum from `tws_users` where username = '" + message + "';"

        mycursor.ping(reconnect=True)

        mycursor.execute(sql)
        buf = mycursor.fetchone()
        await ctx.send(f'{ctx.author.mention}\n```UID: {buf[0]}\nUser: {buf[1]}\nPoints: {buf[2]}\nPost Num: {buf[3]}\nThread Num: {buf[4]}```')
    except:
        mydb = relink_mydb()
        await ctx.send(f'{ctx.author.mention} 无法查询')

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
