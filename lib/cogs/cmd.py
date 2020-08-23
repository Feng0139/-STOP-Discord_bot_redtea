from random import choice, randint
from datetime import datetime

from discord.ext.commands import Cog, command
from discord import Embed
import discord

from urllib.request import urlopen;
import urllib
import json

from lib.cogs.task import serverList

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
serverAPIHTML = 'https://api.status.tw/2.0/server/list/'

################### Normal
# https://api.status.tw/2.0/server/list/?ip=14.29.99.49     TOM PVP
# https://api.status.tw/2.0/server/list/?ip=106.14.194.1    David PVP
# https://api.status.tw/2.0/server/list/?ip=47.101.147.245  Arch 上海
# 
DDNetCHN1 = '?ip=139.9.34.133'    # DDNet CHN1 广州
DDNetCHN2 = '?ip=47.102.202.103'  # DDNet CHN2 上海
DDNetCHN3 = '?ip=39.105.39.69'    # DDNet CHN3 北京
DDNetCHN4 = '?ip=39.106.226.96'   # DDNet CHN4 北京
DDNetCHN5 = '?ip=111.177.18.6'    # DDNet CHN5 襄阳
DDNetCHN6 = '?ip=47.102.203.158'  # DDNet CHN6 上海


class Cmd(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='SearchPlayer', aliases=['searchplayer', 'sp'])
    async def _SearchPlayer(self, ctx, *, arg):
        embed = Embed(
        colour = discord.Color.red(),
        timestamp = datetime.now()
        )
        embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')

        if(arg == None):
            embed.add_field(name='查询失败，参数为空。', value='例：`$sp CarolVlCznYu`')
            await ctx.send(embed=embed)
            return
    
        plNameStr = '`|'

        req = urllib.request.Request(url=serverAPIHTML, headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        if (serverList['servers'] != []):
            for server in serverList['servers']:
                if( server['country'] == 'China' and server['players'] != []):
                    for player in server['players']:
                        if (player['name'] == arg):
                            plNum = 0
                        
                            for player in server['players']:
                                plNameStr += f" {player['name']} |"
                                plNum += 1

                            plNameStr += '`'

                            embed.add_field(name=f"{server['name']}", value=f"`Server IP:` `{server['server_ip']}:{server['server_port']}`", inline=False)
                            embed.add_field(name="游戏版本", value=f"`{server['version']}`")
                            embed.add_field(name="游戏模式", value=f"`{server['gamemode']}`")
                            embed.add_field(name=f"当前地图", value=f"`{server['map']}`")
                            embed.add_field(name=f'玩家列表( {plNum} 位 )', value=f"{plNameStr}", inline=False)
                            await ctx.send(embed=embed)
                            return
            embed.add_field(name='查询的玩家不在线或者不在 CHN 服务器当中。', value='')
            await ctx.send(embed=embed)
            return
        else:
            embed.add_field(name='查询失败，服务器列表为空。', value='请稍等一会后再次查询.')

        await ctx.send(embed=embed)

    @command(name='GetAllPlayer', aliases=['getallplayer', 'gap'])
    async def _GetAllPlayer(self, ctx):
        if(serverList['servers'] != []):
            plAllNum = 0        # 所有玩家数量
            plServer = 0        # 读取到的服务器数量（含玩家）

            for server in serverList['servers']:
                if( server['country'] == 'China' and server['players'] != []):
                    plServer += 1
                    for player in server['players']:
                        plAllNum += 1

            embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
            )
            embed.set_author(name=f'已查询到共有 {plAllNum} 位玩家在 {plServer} 个 CHN 服务器中...')
            embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

    @command(name='GetINFServer', aliases=['getinfserver', 'gis'])
    async def _GetINFServer(self, ctx):
        req = urllib.request.Request(url=serverAPIHTML + '?gamemode=InfClassR', headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        servers = 0
        if(serverList['servers'] != []):
            for server in serverList['servers']:
                if( server['country'] == 'China' and server['players'] != []):
                    servers += 1
                    plNameStr = '`|'
                    plNum = 0
                
                    for player in server['players']:
                        plNameStr += f" {player['name']} |"
                        plNum += 1

                    if (plNum <= 0):
                        server -= 1
                        continue
                    
                    plNameStr += '`'

                    embed = Embed(
                    colour = discord.Color.red(),
                    timestamp = datetime.now()
                    )
                    embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
                    embed.add_field(name=f"{server['name']}", value=f"`Server IP:` `{server['server_ip']}:{server['server_port']}`", inline=False)
                    embed.add_field(name="游戏版本", value=f"`{server['version']}`")
                    embed.add_field(name="游戏模式", value=f"`{server['gamemode']}`")
                    embed.add_field(name=f"当前地图", value=f"`{server['map']}`")
                    embed.add_field(name=f'玩家列表( {plNum} 位 )', value=f"{plNameStr}", inline=False)
                    await ctx.send(embed=embed)

        if (servers <= 0):
            embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
            )
            embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name=f"未查询到有玩家存在的服务器", value='')
            await ctx.send(embed=embed)

    @command(name='GetDDRServer', aliases=['getddrserver', 'gds'])
    async def _GetDDRServer(self, ctx, *, arg):
        tempHtml = serverAPIHTML
        if arg != None:
            num = int(arg.split('CHN')[1])
            if num == 1:
                tempHtml += DDNetCHN1 + '&gamemode=DDraceNetwork'
            elif num == 2:
                tempHtml += DDNetCHN2 + '&gamemode=DDraceNetwork'
            elif num == 3:
                tempHtml += DDNetCHN3 + '&gamemode=DDraceNetwork'
            elif num == 4:
                tempHtml += DDNetCHN4 + '&gamemode=DDraceNetwork'
            elif num == 5:
                tempHtml += DDNetCHN5 + '&gamemode=DDraceNetwork'
            elif num == 6:
                tempHtml += DDNetCHN6 + '&gamemode=DDraceNetwork'
        else:
            tempHtml += '?gamemode=DDraceNetwork'
        
        req = urllib.request.Request(url=tempHtml, headers=headers)
        
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        servers = 0
        if(serverList['servers'] != []):
            for server in serverList['servers']:
                if( server['country'] == 'China' and server['players'] != []):
                    servers += 1
                    plNameStr = '`|'
                    plNum = 0
                
                    for player in server['players']:
                        plNameStr += f" {player['name']} |"
                        plNum += 1

                    if (plNum <= 0):
                        server -= 1
                        continue
                    
                    plNameStr += '`'

                    embed = Embed(
                    colour = discord.Color.red(),
                    timestamp = datetime.now()
                    )
                    embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
                    embed.add_field(name=f"{server['name']}", value=f"`Server IP:` `{server['server_ip']}:{server['server_port']}`", inline=False)
                    embed.add_field(name="游戏版本", value=f"`{server['version']}`")
                    embed.add_field(name="游戏模式", value=f"`{server['gamemode']}`")
                    embed.add_field(name=f"当前地图", value=f"`{server['map']}`")
                    embed.add_field(name=f'玩家列表( {plNum} 位 )', value=f"{plNameStr}", inline=False)
                    await ctx.send(embed=embed)

        if (servers <= 0):
            embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
            )
            embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name=f"未查询到有玩家存在的服务器", value='')
            await ctx.send(embed=embed)
        
    @command(name='GetServerList', aliases=['getserverlist', 'gsl'])
    async def _GetServerList(self, ctx):
        req = urllib.request.Request(url=serverAPIHTML, headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        servers = 0
        if(serverList['servers'] != []):
            for server in serverList['servers']:
                if( server['country'] == 'China' and server['players'] != []):
                    servers += 1
                    plNameStr = '`|'
                    plNum = 0
                
                    for player in server['players']:
                        plNameStr += f" {player['name']} |"
                        plNum += 1

                    if (plNum <= 0):
                        server -= 1
                        continue
                    
                    plNameStr += '`'

                    embed = Embed(
                    colour = discord.Color.red(),
                    timestamp = datetime.now()
                    )
                    embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
                    embed.add_field(name=f"{server['name']}", value=f"`Server IP:` `{server['server_ip']}:{server['server_port']}`", inline=False)
                    embed.add_field(name="游戏版本", value=f"`{server['version']}`")
                    embed.add_field(name="游戏模式", value=f"`{server['gamemode']}`")
                    embed.add_field(name=f"当前地图", value=f"`{server['map']}`")
                    embed.add_field(name=f'玩家列表( {plNum} 位 )', value=f"{plNameStr}", inline=False)
                    
                    await ctx.send(embed=embed)
        if (servers <= 0):
            embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
            )
            embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
            embed.add_field(name=f"未查询到有玩家存在的服务器", value='')
            await ctx.send(embed=embed)


    @command(name='roll', aliases=['dice', 'r'])
    async def _roll(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split('d'))

        embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
        )
        embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
        #embed.set_author(name=f'{ctx.author.display_name} ( {ctx.author} )', icon_url=f'{ctx.author.avatar_url}')
        
        if dice < 40 and value <= 100 and dice > 0 and value > 0:
            rolls = [randint(1, value) for i in range(dice)]
            embed.add_field(name=f'{die_string} = {sum(rolls)}',value='( ' + ' + '.join([str(r) for r in rolls]) + ' )')
        else:
            embed.add_field(name='Error',value='骰子数量不超过 40, 骰子值不超过 100.\n同时两者都不小于 0.')
            embed.set_footer(text='Tips: $roll 1d6')
        
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