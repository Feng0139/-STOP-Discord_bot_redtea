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

bot = commands.Bot(command_prefix = '$', case_insensitive=True, owner_id='341273212656680960')
bot.config_token = key["token"]
# bot.config_token = read_token()

mydb = relink_mydb()
mycursor = mydb.cursor()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Cyyou! OCR Code: SgEAh66"))

@bot.command()
async def test(ctx, *, message=None):
    """
    Test
    """
    try:
        print(message)
        sql = "select uid, username, newpoints, postnum, threadnum from `tws_users` where username = '" + message + "';"

        mycursor.execute(sql)
        buf = mycursor.fetchone()

        embed = discord.Embed(
            title = "Title",
            colour = discord.Colour.red()
        )

        embed.set_image(url="https://www.teeworlds.cn/uploads/avatars/avatar_"+str(buf[0])+".jpg")
        embed.set_author(
            name=str(buf[1]),
            url="https://www.teeworlds.cn/user-"+str(buf[0])+".html",
            icon_url=""
        )
        embed.set_footer(text="RedTea.")
        
        embed.add_field(name="UID", value=str(buf[0]))
        embed.add_field(name="Username", value=str(buf[1]))
        embed.add_field(name="Points",value=str(buf[2]))
        embed.add_field(name="Post Num", value=str(buf[3]), inline=True)
        embed.add_field(name="Thread Num", value=str(buf[4]), inline=True)
        embed.add_field(name="Status", value="Done!")
        embed.add_field(name="Post Num", value=str(buf[3]), inline=True)
        embed.add_field(name="Thread Num", value=str(buf[4]), inline=True)
        embed.add_field(name="", value="")
        embed.add_field(name="Thread Num", value=str(buf[4]), inline=True)
        embed.add_field(name="Post Num", value=str(buf[3]), inline=True)
        
        await client.say(embed=embed)

    except:
        mydb = relink_mydb()
        
        await ctx.send(f'{ctx.author.mention} 无法查询')

    

@bot.command(aliases=['search'])
async def searchu(ctx, *, message=None):
    """
    Search in UID(num)
    """
    try:
        # mydb.ping()

        sql = "select uid, username, newpoints, postnum, threadnum from `tws_users` where uid = " + message + ";"

        mycursor.execute(sql)
        buf = mycursor.fetchone()
        await ctx.send(f'{ctx.author.mention}\n```UID: {buf[0]}\nUser: {buf[1]}\nPoints: {buf[2]}\nPost Num: {buf[3]}\nThread Num: {buf[4]}```')
    except:
        mydb = relink_mydb()
        await ctx.send(f'{ctx.author.mention} 无法查询')

@bot.command()
async def searchn(ctx, *, message=None):
    """
    Search in userName(str)
    """
    try:
        sql = "select uid, username, newpoints, postnum, threadnum from `tws_users` where username = '" + message + "';"

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
