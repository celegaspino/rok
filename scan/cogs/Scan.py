import discord
import asyncio
import pyperclip
import os
import sys

from discord.ext import commands, tasks

#from scan.Utils import Utils
#from scan.DKP import DKP
from Utils import Utils
from DKP import DKP

class Scan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.scan_ready = True
        self.scan_manager = True

    async def on(self):
        if not self.scan_ready:
            return

        self.scan_manager = True

    async def off(self):
        if not self.scan_ready:
            return

        self.scan_manager = False

    async def get_status(self):
        return self.scan_manager

    @commands.command(pass_context=True)
    async def scan(self, ctx):
        if not self.scan_manager:
            await self.bot_off(ctx)
            return        

        if not self.scan_ready:
            embed = discord.Embed(
                title='',
                description=f'Scan in progress...',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        self.scan_ready = False
        embed = discord.Embed(
            title='',
            description=f'Beginning Scan...',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

        await Utils.open_app()
        await Utils.wait_app()

        await Utils.get_rankings()
        await DKP.traverse_rankings(300)

        await Utils.close_app()
        embed = discord.Embed(
            title='',
            description=f'Scan complete',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

        self.scan_ready = True

    @commands.command(pass_context=True, aliases=['rankid'])
    async def id(self, ctx, x: str=None, y: str=None):
        if not self.scan_manager:
            await self.bot_off(ctx)
            return  

        if not self.preliminary_check(x, y):
            return

        dkp = await DKP.get_ranking_id(x)

        embed = discord.Embed(
            title='',
            description=f'Rank : {dkp['rank']}\nId : {dkp['id']}\nName : {dkp['name']}\nPower : {dkp['power']}\nKill Points : {dkp['kp']}\nDeaths : {dkp['deaths']}\nT4 Kills : {dkp['t4']}\nT5 Kills : {dkp['t5']}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def rank(self, ctx, x: str=None, y: str=None):
        if not self.scan_manager:
            await self.bot_off(ctx)
            return  

        if not self.preliminary_check(x, y):
            return

        dkp = await DKP.get_ranking_rank(x)
        dkp = dkp.split(',')

        embed = discord.Embed(
            title='',
            description=f'Id : {dkp['id']}\nName : {dkp['name']}\nPower : {dkp['power']}\nKill Points : {dkp['kp']}\nDeaths : {dkp['deaths']}\nT4 Kills : {dkp['t4']}\nT5 Kills : {dkp['t5']}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    def preliminary_check(self, x, y):
        if (not x == None and x.isdigit()) and y == None:
            return True

        if not y == None:
            return False

        return False

    @commands.command(pass_context=True)
    async def file(self, ctx, x: str=None):
        if not self.scan_manager:
            await self.bot_off(ctx)
            return

        if not x == None:
            return

        if not self.scan_ready:
            embed = discord.Embed(
                title='',
                description=f'Scan in progress...',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title='',
            description=f'Retrieving file...',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

        dir = Utils.join('data')
        files = os.listdir(dir)
        file_path = Utils.join('data', files[0])
        
        file = discord.File(file_path)
        await ctx.send('', file=file)

    async def bot_off(self, ctx):
        embed = discord.Embed(
            title='',
            description=f'Bot is off',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed) 

async def setup(bot):
    await bot.add_cog(Scan(bot))