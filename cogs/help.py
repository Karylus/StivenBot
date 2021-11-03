import discord
from discord.ext import  commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help Cog has been loaded\n------')

    # Comando help propio que sustituye al default
    @commands.command()
    async def help(self, ctx):
        embed=discord.Embed(title='GitHub', url='https://github.com/Karylus/StivenBot', color=0xfdc700)
        embed.set_author(name='Comando Ayuda')
        embed.set_thumbnail(url='https://i.imgur.com/u56OFyl.jpeg')
        embed.add_field(name='stiven', value='Citas del dios Stiven', inline=False)
        embed.add_field(name='sugerir', value='Manda una sugerencia con el formato: '
                        '\n--> !sugerir [Sugerencia]', inline=False)
        embed.add_field(name='suerte', value='Tira un dado de 6 caras', inline=False)
        embed.add_field(name='ruleta', value='Juega a la ruleta rusa', inline=False)
        embed.add_field(name='encuesta', value='Crea una encuesta (Max 10 opciones) con el formato:' \
                        '\n--> !encuesta "Pregunta" "Opc0" ... "Opc9"', inline=False)
        embed.add_field(name='lee', value='Lee el mensaje que quieras en un canal de voz con el formato: ' \
                        '\n--> !lee "Mensaje"', inline=False)
        embed.add_field(name='Prefijo', value='!', inline=True)
        embed.add_field(name='Versión', value='V2.1.0', inline=True)
        embed.set_footer(text='Bot creado por Karylus#0007')

        await ctx.send(embed=embed)

    # Comando help propio que sustituye al default (Admin)
    @commands.command()
    async def helpadmin(self, ctx):
        embed=discord.Embed(title='GitHub', url='https://github.com/Karylus/StivenBot', color=0xfdc700)
        embed.set_author(name='Comando Ayuda (Admin)')
        embed.set_thumbnail(url='https://i.imgur.com/u56OFyl.jpeg')
        embed.add_field(name='clear "N"', value='Elimina "N" mensajes del chat (Max. 100)', inline=False)
        embed.add_field(name='añadirtwitch "nombreTwitch"', value='Se relaciona el ID de discord que ha mandado el mensaje' \
                        ' con el nombre de Twitch, lo tiene que usar la persona del Twitch', inline=False)
        embed.add_field(name='mute', value='Mutea a un usuario con el formato:' \
                        '\n--> !mute @usuario [Motivo]', inline=False)
        embed.add_field(name='unmute', value='Desmutea a un usuario con el formato:' \
                        '\n--> !unmute @usuario', inline=False)
        embed.add_field(name='Prefijo', value='!', inline=True)
        embed.add_field(name='Versión', value='V2.1.0', inline=True)
        embed.set_footer(text='Bot creado por Karylus#0007')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))