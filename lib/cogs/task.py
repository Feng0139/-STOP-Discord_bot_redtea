from discord.ext.commands import Cog, commands
from discord.ext import tasks

from urllib.request import urlopen;
import urllib
import json

class Task(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.serverList = []
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        self.serverAPIHTML = 'https://api.status.tw/2.0/server/list/'

        self.UpdataServerList.start()

    @tasks.loop(minutes=1)
    async def UpdataServerList(self):
        req = urllib.request.Request(url=serverAPIHTML, headers=headers)
        serverListHTML = urlopen(req).read()
        serverList = json.loads(serverListHTML.decode('utf-8'))

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('task')
        # await self.bot.stdout.send("Fun cog ready.")
        # print(' fun cog ready')

def setup(bot):
    bot.add_cog(Task(bot))