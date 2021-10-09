import os
from dotenv import load_dotenv

import random

import discord
from discord import channel
from discord.ext import commands
from discord.utils import get

from PIL import Image, ImageDraw
from io import BytesIO
import requests

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv('.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

#Mensaje de encendido
@bot.event
async def on_ready():
	print('The bot is ready!')

#Citas de Stiven con el comando !stiven
@bot.command(name='stiven', help='- Citas del dios Stiven')
async def stiven(ctx):
    stiven_quotes = [
        'Viva el barza!',
        'Messi se queda',
        'Messi es un 10 por ciento del barza solo',
        'Dejar las pajas',
        'odio a lucas',
        'Pero el barça es tremenda mierda',
        'Puta PSG',
        'me la puso dura la postcreditos',
        'Pues gran resital de gavi y de yeremy pino ganando a la actual campeona de la euro',
    ]

    response = random.choice(stiven_quotes)
    await ctx.send(response)

#Borra N mensajes del chat con el comando !clear N
@bot.command(pass_context=True, name='clear', help='- Borra N mensajes del chat (Máximo 100 de una vez)')
@commands.has_permissions(kick_members=True)
async def clear(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Chat borrado por {}'.format(ctx.author.mention))
        await ctx.message.delete()

    #Comprueba que el usuario tenga los permisos necesarios
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos espabilado.")

#Mensaje y foto cuando alguien entra nuevo al server
@bot.event
async def on_member_join(member):
    # Abre el avatar y lo tansforma a RGB
    avatar_bytes = requests.get(member.avatar_url, stream=True).raw
    avatar = Image.open(avatar_bytes).convert('RGB')

    # Rodondea el avatar
    alpha = Image.new('L', avatar.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.ellipse([(0, 0), avatar.size], fill=255)
    avatar.putalpha(alpha)

    avatar = avatar.resize((350, 350))

    # Abre la portada y pega el avatar
    banner = Image.open('portada.png').convert('RGBA')
    overlay = Image.new('RGBA', banner.size, 0)
    overlay.paste(avatar, (800, 85))
    banner.alpha_composite(overlay)

    # Crea una imagen para cada usuario por si se unen dos a la vez
    welcome_file_path =f'welcome_{member.name}.jpg'
    banner.convert('RGB').save(welcome_file_path)

    # Envia la imagen y un mensaje de bienvenida
    channel = bot.get_channel(736523939337076759)
    await channel.send(file=discord.File(welcome_file_path))
    await channel.send(f'¡Acaba de llegar {member.mention} !')

#Avisa de que Jota y uCes estan en directo con el comando !jota y !uces
@bot.command(name='jota', help='- Avisa de que Jota está en directo')
@commands.has_permissions(kick_members=True)
async def jota(ctx):
    await ctx.send('@everyone Jota está en directo! https://www.twitch.tv/jdriiix')

@bot.command(name='uces', help='- Avisa de que uCes está en directo')
@commands.has_permissions(kick_members=True)
async def uces(ctx):
    await ctx.send('@everyone uCes está en directo! https://www.twitch.tv/uces_')

#Manda un mensaje con una sugerencia con el comando !sugerir 'Mensaje'
@bot.command(help='- Escribe una sugerencia con el formato !sugerir [Sugerencia]')
async def sugerir(ctx, *, question=None):
    if question == None:
        await ctx.send('Escribe la sugerencia.')
        return

    pollEmbed = discord.Embed(title = f'Sugerencia de {ctx.author}', description = f'{question}')

    await ctx.message.delete()
    poll_msg = await ctx.send(embed = pollEmbed)

    await poll_msg.add_reaction('⬆')
    await poll_msg.add_reaction('⬇')

#Manda emotes cuando mandan algun mensaje en especifico
@bot.event
async def on_message(message):
    if message.content.startswith('keke'):
        await message.reply(f'<a:peepoRunKekeV2:874828175547449405>' \
                             '<a:peepoRunKekeV2:874828175547449405>' \
                             '<a:peepoRunKekeV2:874828175547449405>', mention_author=False)

    await bot.process_commands(message)

@bot.listen()
async def on_message(message):
    if message.content.startswith('UwU'):
        await message.reply('¿”UwU"? ¿Por qué dices UwU? ¿Cuál es el propósito?' \
                            ' ¿Te me estás insinuando? ¿Quieres que te bese apasionadamente?', mention_author=False)

#Comando suerte
@bot.command(name='suerte', help='- Lanza un dado de 6 caras')
async def suerte(ctx):
    caras = ['1', '2', '3', '4', '5', '6',]

    response = random.choice(caras)
    await ctx.send(response)

#Ruleta rusa
@bot.command(name='ruleta', help='- Juega a la ruleta rusa')
async def ruleta(ctx):
    recamara = ['CLICK', 'CLICK', 'CLICK', 'CLICK', 'CLICK', 'BANG!',]

    response = random.choice(recamara)
    await ctx.send(response)

bot.run(DISCORD_TOKEN)