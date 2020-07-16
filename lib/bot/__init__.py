from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed

PREFIX = '$'
OWNER_IDS = [341273212656680960]
COGS = [path.split("\\")[-1][:-3] for path in glob('./lib/cogs/*.py')]

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

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(341447602115444746)
            self.stdout = self.get_channel(727828478719688725)

            embed  = Embed(
                colour = 0xCC0000,
                timestamp = datetime.now()
            )
            embed.add_field(name="Now!", value="Online!!!")
            embed.set_thumbnail(url=self.guild.icon_url)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            await self.stdout.send(embed=embed)
            print(' bot ready')
        else:
            print('bot reconnected')

    async def on_message(self, message):
        pass

bot = Bot()