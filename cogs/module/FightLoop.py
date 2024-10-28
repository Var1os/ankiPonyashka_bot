import disnake
from disnake.ext import commands
from random import randint

import asyncio
import json
from .REQ_database import DataBase

# Заглушка для динамической подгрузки
class FightLoop(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


# players = {
#     "user_1", "user_1_pokemons", "user_1_items",
#     "user_2", "user_2_pokemons", "user_2_items"
#     }

# user_X_pokemons = {
#     "1":{
#         "rankCOM":"rank-orde-nums",
#         "live":True,

#         "target":None,
#         "move":None,

#         "effects":[],

#         "trait":{...},
#         "params":{...},
#         "slots":{...}

#         },
#     "2":{...},
#     "3":{...}
#     }



class MainLoop:
    def __init__(self, players) -> None:

        self.step = 0

        self.player_1 = {
            "id":players['user_1'],
            "pokemos":players['user_1_pokemons'],
            "items":players['user_1_items'],

            "loseBool":False
            }
        
        self.player_2 = {
            "id":players['user_2'],
            "pokemons":players['user_2_pokemons'],
            "items":players['user_2_items'],

            "loseBool":False
            }
    
    

    # Основная функция пересчета действий, позиций и урона
    def nextStep():
        pass






def setup(bot:commands.Bot):
    bot.add_cog(FightLoop(bot))