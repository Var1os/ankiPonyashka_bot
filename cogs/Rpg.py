from typing import Coroutine
import disnake
from disnake.ext import commands
from random import randint

from .module.SystemCommandRPG import *
import asyncio
import json


class RPG(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    # TODO: need think how do this
    @commands.command(name='fight', aliases=['f'])
    async def fight(self, ctx):
        pass
    
    
    @commands.Cog.listener('on_button_click')
    async def r_stat(self, inter:disnake.MessageInteraction):
        if inter.component.custom_id not in []:
            return
    
    @commands.command(name='r_stat') #! Aliases add more variation
    async def r_stat(self, ctx):
        
        pass




# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bob = RPG(bot)
    bot.add_cog(bob)
    print(f'Запуск модуля RPG.system')