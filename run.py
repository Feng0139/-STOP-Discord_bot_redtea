import discord

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
    activity_game = discord.game("Cyyou! OCR")
    await client.change_presence(status=discord.Status.dnd, activity=activity_game)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$create_time'):
        await message.channel.send('2020/04/01 22:55 Done!')
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(token)
