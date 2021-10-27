import discord
from discord.ext import  commands, tasks
from discord.utils import get
import os
from dotenv import load_dotenv

import requests
import json
from twitchAPI.twitch import Twitch

class TwitchAlerts(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Cargo la API de Twitch
    load_dotenv('.env')
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

    # Devuelve true si un usuario esta online en Twitch
    def checkuser(self, streamer_name):
        try:
            stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name,
                                headers=self.headers)
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

    async def has_notif_already_sent(self, channel, user):
        async for message in channel.history(limit=200):
            if f'{user} está en directo ' in message.content:
                return message
        else:
            return False
    
    # Evento que se encarga de comprobar y avisar si hay alguien en directo de la lista de streamers
    @commands.Cog.listener()
    async def on_ready(self):
        # Define el loop para que se ejecute cada 20 segundos
        @tasks.loop(seconds=20)
        async def live_notifs_loop(self):
            with open('data/streamers.json', 'r') as file:
                streamers = json.loads(file.read())

            try:
                if streamers is not None:
                    guild = self.bot.get_guild(736523939102195746)
                    channel = self.bot.get_channel(845683127870423070)
                    role = get(guild.roles, id=898999981770412124)

                    # Hace loop en json para obtener el nombre de Twitch y el de discord
                    for user_id, twitch_name in streamers.items():
                        selected_member = ""
                        async for member in guild.fetch_members(limit=None):

                            # Si un miembro esta en el json pero no esta en directo, elimina el rol
                            if member.id == int(user_id):
                                selected_member = member

                        # Comprueba si el miembro esta en directo
                        status, stream_data = self.checkuser(twitch_name)
                        user = self.bot.get_user(int(user_id))

                        if status is True:
                            # Comprueba si se ha mandado el mensaje de aviso
                            message = await self.has_notif_already_sent(channel, user)
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

                            print(f"{user} started streaming. Sending a notification.\n------")
                            
                            continue

                        # Si no esta en vivo:
                        elif stream_data is not None:
                            # Coge todos los miembros del server y elimina el rol
                            if selected_member != "":
                                await selected_member.remove_roles(role)

                            # Comprueba si se ha enviado el mensaje y lo borra
                            message = await self.has_notif_already_sent(channel, user)
                            if message is not False:
                                print(
                                    f"{user} stopped streaming. Removing the notification.\n------")
                                await message.delete()

            except TypeError as e:
                print(e)
                raise e

        # Empieza el loop
        live_notifs_loop.start(self)

def setup(bot):
    bot.add_cog(TwitchAlerts(bot))