'''
+ перемикання постійної озвучки та тільки за командою
+ створення черги
+ повідомлення на приєднання нового учасника до гч
- відтворення бажаних звуків
- зупинка відтворення поточного повідомлення
- тихий мод
'''

from tts import get_speech
from EMOJI_LIB import show_all_em
import discord
from discord.ext import commands
import asyncio
import os

FFMPEG_PATH = "ffmpeg-2023-10-04-git-9078dc0c52-full_build/ffmpeg-2023-10-04-git-9078dc0c52-full_build/bin/ffmpeg.exe"
text_queue = []
always_lib = []
active = False

# with open("token.txt", "r") as file:
#     TOKEN = file.read().strip()
#     print("Token: отримано")

with open("always_voiced.txt", "r") as file:
    always_lib = file.read().split(",")
    print("always_voiced: отримано перелік людей")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Додати це для моніторингу голосових станів

bot = commands.Bot(command_prefix='.', intents=intents)


async def main_sound(ctx, text):
    speech = get_speech(text)
    audio_source = discord.FFmpegPCMAudio(speech, pipe=True, executable=FFMPEG_PATH)
    ctx.voice_client.play(audio_source, after=lambda e: print(f'Audio finished: {e}') if e else None)

async def process_queue(ctx):
    """Обробляє чергу для озвучування."""
    global active
    active = True
    while True:
        if text_queue:
            if ctx.guild.voice_client:
                await main_sound(ctx, text_queue[0])
                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1)  # Затримка в 1 секунду
                text_queue.pop(0)
            else:
                await ctx.send('Бот не підключений до голосового каналу.')
        else:
            await asyncio.sleep(1)  # Затримка в 1 секунду, якщо черга порожня

@bot.event
async def on_ready():
    print(f'Авторизовано як {bot.user.name}.')

@bot.event
async def on_voice_state_update(member, before, after):
    """Обробка події приєднання до голосового каналу."""
    if before.channel is None and after.channel is not None:
        channel = after.channel
        if bot.user in channel.members:
            text_queue.insert(0, f'Щойно {member.display_name} приднався до вас!')

@bot.command()
async def т(ctx, *, text: str):
    """Команда для підключення бота до голосового каналу та додавання тексту до черги."""
    if ctx.author.voice or ctx.guild.voice_client:
        channel = ctx.author.voice.channel
        if not ctx.guild.voice_client:
            # Підключаємо бота до голосового каналу
            await channel.connect()
            # await ctx.send(f'Підключено до голосового каналу {channel.name}.')
        
        text_queue.append(f"{ctx.author.display_name} каже: {text}")
        if not active:
            await process_queue(ctx)  # Запускаємо обробку черги
    else:
        await ctx.send('Вам потрібно бути в голосовому каналі, щоб я міг під\'єднатись.')

@bot.command()
async def завжди(ctx):
    global always_lib
    if str(ctx.author) not in always_lib:
        always_lib.append(str(ctx.author))
        with open("always_voiced.txt", "w") as file:
            file.write(",".join(always_lib))
        await ctx.send(f"Повідомлення {ctx.author} будуть озвучуватись завжди.")

@bot.command()
async def ніколи(ctx):
    global always_lib
    if str(ctx.author) in always_lib:
        always_lib.remove(str(ctx.author))
        with open("always_voiced.txt", "w") as file:
            file.write(",".join(always_lib))
        await ctx.send(f"Повідомлення {ctx.author} не будуть озвучуватись.")

@bot.command()
async def емоджі(ctx):
    await ctx.send(show_all_em())

@bot.command()
async def виходь(ctx):
    """Команда для відключення бота від голосового каналу."""
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        await ctx.send('ну і добре, піду 💢')
        speech = get_speech('ну і добре, піду 💢')
        audio_source = discord.FFmpegPCMAudio(speech, pipe=True, executable=FFMPEG_PATH)
        ctx.voice_client.play(audio_source)
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        await ctx.voice_client.disconnect()
        global text_queue
        text_queue = []
    else:
        await ctx.send('Я не в голосовому каналі.')

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.author.voice and str(message.author) in always_lib:
            channel = message.author.voice.channel
            if not message.guild.voice_client:
                await channel.connect()
            
            # Команда для підключення бота до голосового каналу та додавання тексту до черги.
            mess = str(message.content)
            if not mess.startswith("."):
                text_queue.append(f"{message.author.display_name} каже: {mess}")
            global active
            if not active:
                await process_queue(await bot.get_context(message))  # Запускаємо обробку черги з контекстом
            if mess in text_queue:
                return
    
    # Передаємо обробку команд боту
    await bot.process_commands(message)

bot.run(os.environ.get('TOKEN'))
