from random import choice, randint
from datetime import datetime

from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
import discord

from urllib.request import urlopen;
import urllib
import json

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
serverAPIHTML = 'https://api.status.tw/2.0/server/list/'

class Cmd(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='GetINFServer', aliases=['getinfserver', 'gis'])
    async def _GetServerList(self, ctx):
        req = urllib.request.Request(url=serverAPIHTML + '?gamemode=InfClassR', headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        for server in serverList['servers']:
            if( server['country'] == 'China' and server['num_players'] > 0):
                info = f"```{server['name']}\n{server['map']}\n{server['server_ip']}\nPlayers:\n| "

                for player in server['players']:
                    info += player['name'] + ' | '

                info += "```"
                await ctx.send(info)

    @command(name='GetDDRServer', aliases=['getddrserver', 'gds'])
    async def _GetServerList(self, ctx):
        req = urllib.request.Request(url=serverAPIHTML + '?gamemode=DDraceNetwork', headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        for server in serverList['servers']:
            if( server['country'] == 'China' and server['num_players'] > 0):
                info = f"```{server['name']}\n{server['map']}\n{server['server_ip']}\nPlayers:\n| "

                for player in server['players']:
                    info += player['name'] + ' | '

                info += "```"
                await ctx.send(info)

    @command(name='GetServerList', aliases=['getserverlist', 'gsl'])
    async def _GetServerList(self, ctx):
        req = urllib.request.Request(url=serverAPIHTML, headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

        for server in serverList['servers']:
            if( server['country'] == 'China' and server['num_players'] > 0 and server['players'] != {}):
                embed = Embed(
                    colour = discord.Color.red(),
                    timestamp = datetime.now()
                )
                embed.set_footer(text='请求来自 ' + f'{ctx.author.display_name} ( {ctx.author} ) ', icon_url=f'{ctx.author.avatar_url}')
                embed.add_field(name=f"{server['name']}", value=f"`Server IP: {server['server_ip']}:{server['server_port']}`", inline=False)
                
                plNameStr = '`|'
                plNum = 0
            
                for player in server['players']:
                    # if(player == server['plsyers'][-1]):
                    #     plNameStr += f"{player['name']}`"
                    # else:
                    plNameStr += f" {player['name']} |"
                    
                    plNum += 1

                plNameStr += '`'

                embed.add_field(name=f'玩家列表( {plNum} 位 )', value=f"{plNameStr}", inline=False)

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