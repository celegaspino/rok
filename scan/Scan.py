import discord
## pip install discord.py
## pip install audioop-lts
## pip install python-dotenv

from dotenv import load_dotenv
from discord.ext import commands

import os

load_dotenv()
token = os.getenv('token')

class Scan(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='',
            case_insensitive=True,
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def setup_hook(self):
        if not 'cogs.Scan' in self.extensions:
            await self.load_extension('cogs.Scan')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            pass

Scan().run(token)