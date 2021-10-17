import os
from dotenv import load_dotenv

import random

import discord
from discord.ext import commands, tasks
from discord.utils import get

from PIL import Image, ImageDraw
from io import BytesIO
import requests

import json
from twitchAPI.twitch import Twitch
from discord import Streaming

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, activity = discord.Game(name='!help | V1.5.5'), \
                    help_command=None)

# Cargo el token de Discord
load_dotenv('.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Cargo el token de Twitch
client_id = os.getenv('CLIENT_ID_TWITCH')
client_secret = os.getenv('CLIENT_SECRET_TWITCH')
body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json()
headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}

# Comando help propio que sustituye al default
@bot.command()
async def help(ctx):
    embed=discord.Embed(title='GitHub', url='https://github.com/Karylus/StivenBot', color=0xfdc700)
    embed.set_author(name='Comando Ayuda')
    embed.set_thumbnail(url='https://i.imgur.com/u56OFyl.jpeg')
    embed.add_field(name='stiven', value='Citas del dios Stiven', inline=False)
    embed.add_field(name='sugerir', value='Manda una sugerencia con el formato -> !sugerir [Sugerencia]', inline=False)
    embed.add_field(name='suerte', value='Tira un dado de 6 caras', inline=False)
    embed.add_field(name='ruleta', value='Juega a la ruleta rusa', inline=False)
    embed.add_field(name='encuesta "Pregunta" "Opc0" ... "Opc10"', value='Crea una encuesta (Max 10 opciones)', inline=False)
    embed.add_field(name='clear "N" [ADMIN]', value='Elimina "N" mensajes del chat (Max. 100)', inline=False)
    embed.add_field(name='jota [ADMIN]', value='Avisa de que Jota está en directo', inline=False)
    embed.add_field(name='uces [ADMIN]', value='Avisa de que uCes_ está en directo', inline=False)
    embed.add_field(name='añadirtwitch "nombreTwitch" [ADMIN]', value='Añade el "nombreTwitch" para el usuario en la lista de streamers', inline=False)
    embed.add_field(name='Prefijo', value='!', inline=True)
    embed.add_field(name='Versión', value='V1.5', inline=True)
    embed.set_footer(text='Bot creado por Karylus#0007')

    await ctx.send(embed=embed)

# Lee citas de Stiven de 'frasesStiven.txt' con el comando !stiven
@bot.command(name='stiven')
async def stiven(ctx):
    with open('frasesStiven.txt', 'r') as f:
        read = f.read()
        array = read.split('\n')
        quote = random.choice(array)

    await ctx.channel.send(quote)

# Borra N mensajes del chat con el comando !clear N
@bot.command(pass_context=True, name='clear')
@commands.has_permissions(kick_members=True)
async def clear(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send('Chat borrado por {}'.format(ctx.author.mention))
    await ctx.message.delete()

    # Comprueba que el usuario tenga los permisos necesarios
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos espabilado.")

# Mensaje y foto cuando alguien entra nuevo al server
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
    welcome_file_path = f'welcome_{member.name}.jpg'
    banner.convert('RGB').save(welcome_file_path)

    # Envia la imagen y un mensaje de bienvenida
    channel = bot.get_channel(736523939337076759)
    await channel.send(file=discord.File(welcome_file_path))
    await channel.send(f'¡Acaba de llegar {member.mention} !')

    # Asigna un rol en especifico
    guild = bot.get_guild(736523939102195746)
    role = get(guild.roles, id=736523939102195747)
    await bot.add_roles(member, role)

# Avisa de que Jota y uCes estan en directo con el comando !jota y !uces
@bot.command(name='jota')
@commands.has_permissions(kick_members=True)
async def jota(ctx):
    await ctx.send('@everyone Jota está en directo! https://www.twitch.tv/jdriiix')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos espabilado.")

@bot.command(name='uces')
@commands.has_permissions(kick_members=True)
async def uces(ctx):
    await ctx.send('@everyone uCes está en directo! https://www.twitch.tv/uces_')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos espabilado.")

# Manda un mensaje con una sugerencia con el comando !sugerir 'Mensaje'
@bot.command()
async def sugerir(ctx, *, question=None):
    if question == None:
        await ctx.send('Escribe la sugerencia.')
        return

    pollEmbed = discord.Embed(
        title=f'Sugerencia de {ctx.author}', description=f'{question}',
        color=0xfdc700)

    await ctx.message.delete()
    poll_msg = await ctx.send(embed=pollEmbed)

    await poll_msg.add_reaction('⬆')
    await poll_msg.add_reaction('⬇')

# Manda emotes cuando mandan algun mensaje en especifico
@bot.event
async def on_message(message):
    if message.content.startswith('keke'):
        await message.reply(f'<a:peepoRunKekeV2:874828175547449405>'
                            '<a:peepoRunKekeV2:874828175547449405>'
                            '<a:peepoRunKekeV2:874828175547449405>', mention_author=False)
    await bot.process_commands(message)

@bot.listen()
async def on_message(message):
    if message.content.startswith('UwU'):
        await message.reply('¿”UwU"? ¿Por qué dices UwU? ¿Cuál es el propósito?'
                            ' ¿Te me estás insinuando? ¿Quieres que te bese apasionadamente?', mention_author=False)

# Comando suerte con un D6
@bot.command(name='suerte')
async def suerte(ctx):
    caras = ['1', '2', '3', '4', '5', '6', ]
    response = random.choice(caras)
    await ctx.send(response)

# Ruleta rusa
@bot.command(name='ruleta')
async def ruleta(ctx):
    recamara = ['CLICK', 'CLICK', 'CLICK', 'CLICK', 'CLICK', 'BANG!', ]
    response = random.choice(recamara)
    await ctx.send(response)

# Devuelve true si un usuario esta online en Twitch
def checkuser(streamer_name):
    try:
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name,
                              headers=headers)
        if streamer_name is not None and str(stream) == '<Response [200]>':
            stream_data = stream.json()

            if len(stream_data['data']) == 1:
                return True, stream_data
            else:
                return False, stream_data
        else:
            stream_data = None
            return False, stream_data
    except Exception as e:
        print(e)
        stream_data = None
        return False, stream_data

async def has_notif_already_sent(channel, user):
    async for message in channel.history(limit=200):
        if f'{user} está en directo ' in message.content:
            return message
    else:
        return False

# Evento que se encarga de comprobar y avisar si hay alguien en directo de la lista de streamers
@bot.event
async def on_ready():
    # Define el loop para que se ejecute cada 20 segundos
    @tasks.loop(seconds=20)
    async def live_notifs_loop():
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())

        try:
            if streamers is not None:
                guild = bot.get_guild(736523939102195746)
                channel = bot.get_channel(845683127870423070)
                role = get(guild.roles, id=898999981770412124)

                # Hace loop en json para obtener el nombre de Twitch y el de discord
                for user_id, twitch_name in streamers.items():
                    selected_member = ""
                    async for member in guild.fetch_members(limit=None):

                        # Si un miembro esta en el json pero no esta en directo, elimina el rol
                        if member.id == int(user_id):
                            selected_member = member

                    # Comprueba si el miembre esta en directo
                    status, stream_data = checkuser(twitch_name)
                    user = bot.get_user(int(user_id))

                    if status is True:
                        # Comprueba si se ha mandado el mensaje de aviso
                        message = await has_notif_already_sent(channel, user)
                        if message is not False:
                            continue
                        # Coge todos los miembros del server y les añade el rol
                        if selected_member != "":
                            await selected_member.add_roles(role)
                        # Manda el mensaje y continua con el loop
                        twitch_embed = discord.Embed(
                                title=f":red_circle: **EN DIRECTO**\n{user.name} está en directo en Twitch! \n \n{stream_data['data'][0]['title']}",
                                color=0xac1efb,
                                url=f'\nhttps://www.twitch.tv/{twitch_name}'
                        )
                        twitch_embed.add_field(
                            name = '**Juego**',
                            value = stream_data['data'][0]['game_name'], 
                            inline = True
                        )
                        twitch_embed.add_field(
                            name = '**Viewers**',
                            value = stream_data['data'][0]['viewer_count'], 
                            inline = True
                        )
                        twitch_embed.set_author(
                            name = str(twitch_name),
                            icon_url = 'https://i.imgur.com/gcbtreZ.png'
                        )

                        twitch_embed.set_image(url = f'https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitch_name}-1280x720.jpg')

                        await channel.send(f'\n{user} está en directo Twitch! @everyone', embed=twitch_embed)

                        print(f"{user} started streaming. Sending a notification.")
                        
                        continue

                    # Si no esta en vivo:
                    elif stream_data is not None:
                        # Coge todos los miembros del server y elimina el rol
                        if selected_member != "":
                            await selected_member.remove_roles(role)

                        # Comprueba si se ha enviado el mensaje y lo borra
                        message = await has_notif_already_sent(channel, user)
                        if message is not False:
                            print(
                                f"{user} stopped streaming. Removing the notification.")
                            await message.delete()

        except TypeError as e:
            print(e)
            raise e

    # Empieza el loop
    live_notifs_loop.start()

# Comando para añadir los nombres de Twtich al json
@bot.command(name='añadirtwitch', pass_context=True)
@commands.has_permissions(kick_members=True)
async def add_twitch(ctx, twitch_name):
    # Abre y lee el json
    with open('streamers.json', 'r') as file:
        streamers = json.loads(file.read())

    # Coge el ID del usuario pasado con el comando
    user_id = ctx.author.id
    # Asigna el nombre de twitch a su ID de discord
    streamers[user_id] = twitch_name

    # Añade los cambios al json
    with open('streamers.json', 'w') as file:
        file.write(json.dumps(streamers))
    # Avisa si ha funcionado.
    await ctx.send(f'Añadido {twitch_name} para {ctx.author} a la lista.')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No tienes permisos espabilado.")

# Comando para hacer encuentas
@bot.command(name='encuesta', pass_contex=True)
async def encuesta(ctx, question, *options: str):
    if len(options) <= 1:
        await ctx.send('Introduce alguna opción para la encuesta')
        return

    if len(options) > 10:
        await ctx.send('No puedes hacer una encuesta de más de 10 opciones')
        return

    if len(options) == 2 and options[0] == 'si' and options[1] == 'no':
        reactions = ['✅', '❌']

    else:
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    description = []

    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)

    embed = discord.Embed(title=question, 
                          description=''.join(description), 
                          color=0xfdc700)
    react_message = await ctx.send(embed=embed)

    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)

    embed.set_footer(text='Poll ID: {}'.format(react_message.id))

    await react_message.edit(embed=embed)
    await ctx.message.delete()

# Cuando un miembro se une al server, actualiza un canal con el número de miembros que hay
@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = bot.get_channel(869697068258701373)
    await channel.edit(name = f'𝐌𝐢𝐞𝐦𝐛𝐫𝐨𝐬: {guild.member_count}')

# Cuando un miembro se va del server, actualiza un canal con el número de miembros que hay
@bot.event
async def on_member_remove(member):
    guild = member.guild
    channel = bot.get_channel(869697068258701373)
    await channel.edit(name = f'𝐌𝐢𝐞𝐦𝐛𝐫𝐨𝐬: {guild.member_count}')

print('The bot is ready!')
bot.run(DISCORD_TOKEN)