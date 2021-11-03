import discord
from discord.ext import  commands

import random

import json

class Commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Commands Cog has been loaded\n------')

    # Citas de Stiven guardadas en frasesStiven.txt
    @commands.command(name='stiven')
    async def stiven(self, ctx):
        with open('data/frasesStiven.txt', 'r') as file:
            read = file.read()
            array = read.split('\n')
            quote = random.choice(array)

        await ctx.channel.send(quote)
    
    # Borra N mensajes del chat con el comando !clear N
    @commands.command(pass_context=True, name='clear')
    @commands.has_permissions(kick_members=True)
    async def clear(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Chat borrado por {}'.format(ctx.author.mention))
        await ctx.message.delete()
    
    # Comprueba que el usuario tenga los permisos necesarios
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No tienes permisos espabilado.")
    
    # Comando suerte con un D6
    @commands.command(name='suerte')
    async def suerte(self, ctx):
        caras = ['1', '2', '3', '4', '5', '6', ]
        response = random.choice(caras)
        await ctx.send(response)
    
    # Ruleta rusa
    @commands.command(name='ruleta')
    async def ruleta(self, ctx):
        recamara = ['CLICK', 'CLICK', 'CLICK', 'CLICK', 'CLICK', 'BANG!', ]
        response = random.choice(recamara)
        await ctx.send(response)
    
    # Comando para añadir los nombres de Twtich al json
    @commands.command(name='añadirtwitch', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def add_twitch(self, ctx, twitch_name):
        # Abre y lee el json
        with open('data/streamers.json', 'r') as file:
            streamers = json.loads(file.read())

        # Coge el ID del usuario pasado con el comando
        user_id = ctx.author.id
        # Asigna el nombre de twitch a su ID de discord
        streamers[user_id] = twitch_name

        # Añade los cambios al json
        with open('data/streamers.json', 'w') as file:
            file.write(json.dumps(streamers))
        # Avisa si ha funcionado.
        await ctx.send(f'Añadido {twitch_name} para {ctx.author} a la lista.')

    @add_twitch.error
    async def add_twitch_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("No tienes permisos espabilado.")
    
    # Manda un mensaje con una sugerencia con el comando !sugerir 'Mensaje'
    @commands.command()
    async def sugerir(self, ctx, *, question=None):
        if question == None:
            await ctx.send('Escribe la sugerencia.')
            return

        pollEmbed = discord.Embed(
            title=f'Sugerencia de {ctx.author}', description=f'{question}',
            color=0xfdc700
        )

        await ctx.message.delete()
        poll_msg = await ctx.send(embed=pollEmbed)

        await poll_msg.add_reaction('⬆')
        await poll_msg.add_reaction('⬇')
    
    # Comando para hacer encuentas
    @commands.command(name='encuesta', pass_contex=True)
    async def encuesta(self, ctx, question, *options: str):
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
    
    # Mutea a un usuario nombrado y aporta un motivo
    @commands.command(name='mute', pass_context = True)
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        if not mutedRole:
            mutedRole = await guild.create_role(name='Muted')

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        embed = discord.Embed(title='Muteado', 
                              description=f'{member.mention} ha sido muteado', 
                              color=0xfdc700
        )
        embed.add_field(name='Razón:', value=reason, inline=False)

        await ctx.send(embed=embed)

        await member.add_roles(mutedRole, reason=reason)
    
    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('No tienes permisos espabilado.')
    
    # Desmutea a un usuario
    @commands.command(name='unmute')
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

        await member.remove_roles(mutedRole)

        embed = discord.Embed(title='Desmuteado', 
                              description=f'Se ha desmuteado a: {member.mention}',
                              color=0xfdc700
        )
        await ctx.send(embed=embed)
    
    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('No tienes permisos espabilado.')

def setup(bot):
    bot.add_cog(Commands(bot))