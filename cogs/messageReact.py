import discord
from discord.ext import  commands
from PIL import Image, ImageDraw
import requests

class MessageReact(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('MessageReact Cog has been loaded\n------')

    # Manda emotes cuando mandan algun mensaje en especifico
    @commands.Cog.listener('on_message')
    async def keke(self, message):
        if message.content.startswith('keke'):
            await message.reply(f'<a:peepoRunKekeV2:874828175547449405>'
                                '<a:peepoRunKekeV2:874828175547449405>'
                                '<a:peepoRunKekeV2:874828175547449405>', mention_author=False)
        
    @commands.Cog.listener('on_message')
    async def uwu(self, message):
        if message.content.startswith('UwU'):
            await message.reply('¿”UwU"? ¿Por qué dices UwU? ¿Cuál es el propósito?'
                                ' ¿Te me estás insinuando? ¿Quieres que te bese apasionadamente?', mention_author=False)
    
    @commands.Cog.listener('on_message')
    async def makelele(self, message):
        if message.content.startswith('makelele'):
            await message.reply('https://i.imgur.com/IQisILF.mp4', mention_author=False)                                

async def setup(bot):
    await bot.add_cog(MessageReact(bot))