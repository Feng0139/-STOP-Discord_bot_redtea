from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.ext import commands
from discord import Embed
import discord

from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord.errors import Forbidden, HTTPException

PREFIX = '$'
OWNER_IDS = [341273212656680960]
COGS = [path.split("\\")[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class Ready(object):
    def __init__(self):
        for cog in COGS:
            temp = cog.replace('./lib/cogs/', '')
            print(f'Ready INIT: {cog} && {temp}')
            setattr(self, temp, False)
    
    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f' {cog} cog ready')

    def all_ready(self):
        return all([getattr(self, cog.replace('./lib/cogs/', '')) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        try:
            for cog in COGS:
                temp = cog.replace('./lib/cogs/', '')
                self.load_extension(f'lib.cogs.{temp}')
                print(f'{temp} cog loaded') 

            print('setup complete')
        except:
            print('!!!SETUP ERROR!!!')

    def run(self, version):
        self.VERSION = version
        with open('./lib/bot/token.tk', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print('running setup...')
        self.setup()

        print('running bot...')
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print(' bot connected')

    async def on_disconnect(self):
        print('bot disconnected')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            # await args[0].send('在执行命令的时候发生了一些错误.')
        else:
            channel = self.get_channel(510468583290175491)
            # await channel.send('RedTea bot 发生了一些未知错误.')

        raise

    async def on_command_error(self, ctx, exc):
        embed = Embed(
            colour = discord.Color.red(),
            timestamp = datetime.now()
        )
        embed.set_thumbnail(url=self.guild.icon_url)
        
        if any([isinstance(error, exc) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            embed.add_field(name='Error',value='有一个或多个必填的值是空的.')

        elif isinstance(exc.original, HTTPException):
            embed.add_field(name='Error',value='无法发送消息.')

        elif isinstance(exc.original, Forbidden):
            embed.add_field(name='Error',value='没有权限执行.')

        else:
            raise exc.original

        await ctx.send(embed=embed)

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(341447602115444746)
            self.stdout = self.get_channel(727828478719688725)

            await self.change_presence(activity=discord.Game("Command: $help"), status=discord.Status.dnd)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            # embed  = Embed(
            #     colour = discord.Color.red(),
            #     timestamp = datetime.now()
            # )
            # embed.add_field(name="Now!", value="Online!!!")
            # embed.set_thumbnail(url=self.guild.icon_url)
            # await self.stdout.send(embed=embed)
            print(' bot ready')
        else:
            print('bot reconnected')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()