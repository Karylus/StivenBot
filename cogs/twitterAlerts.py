import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv
import os

import tweepy

import datetime

class TwitterAlerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Cargo la API de Twitter
    load_dotenv('.env')
    consumer_id = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_id = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret = os.getenv('TWITTER_ACCESS_SECRET')

    auth = tweepy.OAuthHandler(consumer_id, consumer_secret)
    auth.set_access_token(access_id, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit = True)

    # Funcion que comprueba si se ha enviado ya un Tweet
    async def has_notif_already_sent(self, channel, tweets):
        async for message in channel.history(limit=200):
            if f'{str(tweets)}' in message.content:
                return message
        else:
            return False

    @commands.Cog.listener()
    async def on_ready(self):
        print('TwitterAlerts Cog has been loaded\n------')

        # Define el loop para que se ejecute cada 20 segundos
        @tasks.loop(seconds=20)
        async def live_notifs_loop(self):
            # Guardo el canal donde se va a enviar el mensaje
            channel = self.bot.get_channel(1004842070848061513)

            # Guarado el ultimo tweet o retweet
            status_list = self.api.user_timeline(
                user_id='1270407920979714048', count=1, tweet_mode='extended', exclude_replies=True)
            status = status_list[0]

            tweets = status.id

            # Si ya se ha mandado, no sigue el loop
            message = await self.has_notif_already_sent(channel, tweets)
            if message is not False:
                return

            if hasattr(status, 'retweeted_status'):
                retweeted = True
            else:
                retweeted = False

            # Si es un retweet manda un embed y si no, manda uno distinto
            if retweeted:
                name = status.author.name
                screen_name = status.author.screen_name
                orig_screen_name = status.retweeted_status.author.screen_name
                orig_name = status.retweeted_status.author.name

                # Creo el embed adaptado a que sea un retweet
                twitter_embed = discord.Embed(title=f'**{name} ha retweeteado:**',
                                              url='https://twitter.com/twitter/statuses/' +
                                              str(tweets),
                                              description=f'{status.retweeted_status.full_text}',
                                              color=0x00b1e9,
                                              timestamp=datetime.datetime.utcnow()
                )
                twitter_embed.set_author(name=f'{name} (@{screen_name})',
                                         url=f'https://twitter.com/{screen_name}',
                                         icon_url=f'https://unavatar.io/twitter/{screen_name}'
                )
                twitter_embed.set_thumbnail(url=f'https://unavatar.io/twitter/{orig_screen_name}')
                twitter_embed.set_footer(text=f'Twitter',
                                         icon_url='https://i.imgur.com/sSZWFlX.png'
                )
                twitter_embed.add_field(name='Retweeted',
                                        value=f'[{orig_name} (@{orig_screen_name})](https://twitter.com/{orig_screen_name})',
                                        inline=True
                )

                # Si tiene foto, la añade al embed
                if 'media' in status.retweeted_status.entities:
                    for image in status.retweeted_status.entities['media']:
                        image_url = image['media_url']

                    twitter_embed.set_image(url = f'{image_url}')

                # Manda el embed con un mensaje para avisar
                await channel.send(f'@everyone Hay un nuevo Tweet de {name}: https://twitter.com/twitter/statuses/' + str(tweets),
                                   embed=twitter_embed
                )

            else:
                name = status.author.name
                screen_name = status.author.screen_name

                # Creo el embed adaptado a que sea un tweet
                twitter_embed = discord.Embed(title=f'**{name} ha tweeteado:**',
                                              url='https://twitter.com/twitter/statuses/' +
                                              str(tweets),
                                              description=f'{status.full_text}',
                                              color=0x00b1e9,
                                              timestamp=datetime.datetime.utcnow()
                )
                twitter_embed.set_author(name=f'{name} (@{screen_name})',
                                         url=f'https://twitter.com/{screen_name}',
                                         icon_url=f'https://unavatar.io/twitter/{screen_name}'
                )
                twitter_embed.set_thumbnail(url=f'https://unavatar.io/twitter/{screen_name}')
                twitter_embed.set_footer(text=f'Twitter',
                                         icon_url='https://i.imgur.com/sSZWFlX.png'
                )

                # Si tiene foto, la añade al embed
                if 'media' in status.entities:
                    for image in status.entities['media']:
                        image_url = image['media_url']

                    twitter_embed.set_image(url = f'{image_url}')

                # Manda el embed con un mensaje para avisar
                await channel.send(f'@everyone Hay un nuevo Tweet de {name}: https://twitter.com/twitter/statuses/' + str(tweets),
                                   embed=twitter_embed
                )

        # Empieza el loop
        live_notifs_loop.start(self)

        if not live_notifs_loop.is_running():
            live_notifs_loop.restart(self)

async def setup(bot):
    await bot.add_cog(TwitterAlerts(bot))