import os
from dotenv import load_dotenv
from pathlib import Path

import discord
from discord.ext import commands
import asyncio

cwd = Path(__file__).parents[0]
cwd = str(cwd)

intents = discord.Intents.default()
intents.members = True
intents.message_content =True

bot = commands.Bot(command_prefix='!', intents=intents, activity = discord.Game(name='!help | V2.1.0'), 
                    help_command=None)

# Cargo el token de Discord
load_dotenv('.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print('The bot is ready\n------')

async def load_extensions():
    for filename in os.listdir(cwd+"/cogs"):
        if filename.endswith(".py") and not filename.startswith('__'):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())