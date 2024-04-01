from .module import RequestDataBase as Rdb
import random
import time
import disnake
from disnake.ext import commands

db = Rdb.DataBase

class EmotionalBase:
    def __init__(self, bot=commands.cog):
        self.bot = bot
    
    class Love:
        def __init__(self, message, user: int= None, db = Rdb.DataBase):
            self.message= message
            self.user= user
            self.db= db
    
        def react(self):
            pass



    class Mood:
        def __init__(self, user: int = None, db = Rdb.DataBase):
            self.user= user
            self.db= db

class EmotionalPony(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        pass

    

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(EmotionalPony(bot))
    print(f'Запуск модуля Emotional.system')