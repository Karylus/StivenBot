import discord
from discord.ext import commands
from discord.utils import get
import asyncio

from gtts import gTTS


class ReadMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ReadMessage Cog has been loaded\n------')

    @commands.command()
    async def conectar(self, ctx, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel

            except AttributeError:
                await self.cog_command_error(ctx, 'No hay ningun canal para unirme. Por favor entra en un canal de voz.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise self.cog_command_error(f'Uniendose al canal: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise self.cog_command_error(f'Uniendose al canal: <{channel}> timed out.')

        await ctx.send(f'Conectado a: **{channel}**', delete_after=20)
    
    # Guarda un texto en un archivo y luego lo lee en un canal de voz
    @commands.command()
    async def lee(self, ctx, text=None):
        if not text:
            # Nada que decir
            await ctx.send(f'Oye {ctx.author.mention}, que quieres que diga?')
            return

        vc = ctx.voice_client

        if not vc:
            # No esta en un canal de voz
            await ctx.send('Tengo que estar un canal de voz para leer, usar el comando !conectar.')
            return

        tts = gTTS(text=text, lang='pt')
        tts.save('data/texto.mp3')

        try:
            # Reproduce el audio en el canal de voz
            vc.play(discord.FFmpegPCMAudio('data/texto.mp3'))

            # Cambia el volumen a 1
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = 1

        except TypeError as e:
            await ctx.send(f'TypeError exception:\n`{e}`')

async def setup(bot):
    await bot.add_cog(ReadMessage(bot))
