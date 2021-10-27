import os
from dotenv import load_dotenv
from pathlib import Path

import discord
from discord.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, activity = discord.Game(name='!help | V2.0.0'), \
                    help_command=None)

# Cargo el token de Discord
load_dotenv('.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print('The bot is ready\n------')

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith('.py') and not file.startswith('__'):
            bot.load_extension(f'cogs.{file[:-3]}')

    bot.run(DISCORD_TOKEN)