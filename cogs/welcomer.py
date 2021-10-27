from PIL.ImageFont import ImageFont
import discord
from discord.ext import  commands
from discord.utils import get
from PIL import Image, ImageDraw, ImageFont
import requests

class Welcomer(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Welcomer Cog has been loaded\n------')

    # Mensaje y foto cuando alguien entra nuevo al server
    @commands.Cog.listener()
    async def on_member_join(self, member):
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
        banner = Image.open('data/portada.png').convert('RGBA')
        overlay = Image.new('RGBA', banner.size, 0)
        overlay.paste(avatar, (785, 85))
        banner.alpha_composite(overlay)

        # Crea una imagen para cada usuario por si se unen dos a la vez
        welcome_file_path = f'data/welcome_{member.name}.jpg'
        banner.convert('RGB').save(welcome_file_path)

        # Escribe el nombre del usuario en el banner
        user_name = member.name
        font = ImageFont.truetype('data/arial.ttf', 100)
        img = Image.open(welcome_file_path)
        text = ImageDraw.Draw(img)
        text.text((735, 600), f'@{user_name}', (255, 0, 0), font=font)
        img.save(welcome_file_path)

        # Envia la imagen y un mensaje de bienvenida
        channel = self.bot.get_channel(899273141841432606)
        await channel.send(file=discord.File(welcome_file_path))
        await channel.send(f'¡Acaba de llegar {member.mention} !')

        # Asigna un rol en especifico
        guild = self.bot.get_guild(866065923562405939)
        role = get(guild.roles, id=866416360828829756)
        await member.add_roles(role)

        # Actualiza el nombre del canal con el nuevo numero de miembros
        channel_members = self.bot.get_channel(899361663550120016)
        await channel_members.edit(name = f'𝐌𝐢𝐞𝐦𝐛𝐫𝐨𝐬: {guild.member_count}')

    # Actualiza el nombre del canal con el nuevo numero de miembros
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        channel = self.bot.get_channel(899361663550120016)
        await channel.edit(name = f'𝐌𝐢𝐞𝐦𝐛𝐫𝐨𝐬: {guild.member_count}')

def setup(bot):
    bot.add_cog(Welcomer(bot))