from typing import Coroutine
import disnake
from disnake.ext import commands
from random import randint

class RPG(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.command(name='fight', aliases=['f'])
    async def fight(self, ctx):
        pass

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bob = RPG(bot)
    bot.add_cog(bob)
    print(f'Запуск модуля RPG.system')