from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = '$'
OWNER_IDS = [341273212656680960]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def run(self, version):
        self.VERSION = version
        with open('./lib/bot/token.tk', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()
            
        print('running bot...')
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('Bot connected')

    async def on_disconnect(self):
        print('Bot disconnected')

    async def on_ready(self):
        pass

    async def on_message(self, message):
        pass

bot = Bot()