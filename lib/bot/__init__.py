from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Embed

PREFIX = '$'
OWNER_IDS = [341273212656680960]
COGS = [path.split("\\")[-1][:-3] for path in glob('./lib/cogs/*.py')]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        try:
            for cog in COGS:
                print(f'{cog}')
                if cog.find('./lib/cogs/'):
                    cog.replace('./lib/cogs/', '')
                    print(f'{cog}')
                self.load_extension(f'lib.cogs.{cog}')
                print(f'{cog} cog loaded')

            print('setup complete')
        except:
            print('SETUP ERROR')

    def run(self, version):
        self.VERSION = version
        with open('./lib/bot/token.tk', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print('running setup...')
        self.setup()

        print('running bot...')
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('bot connected')

    async def on_disconnect(self):
        print('bot disconnected')

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.stdout = self.get_channel(727828478719688725)

            embed  = Embed(
                Colour = 0xFF0000,
                timestamp = datetime.now()
            )
            embed.add_field(name="Now!", value="Online!!!")

            await self.stdout.send(embed=embed)

        else:
            print('bot reconnected')

    async def on_message(self, message):
        pass

bot = Bot()