from typing import Coroutine
import disnake
from disnake.ext import commands
from random import randint

import asyncio
import json
from REQ_database import DataBase

async def deleteAfter(message:object, time:int) -> None:
    await asyncio.sleep(time)
    await message.delete()
    
async def userData(ID:int):
    try:
        with open(f'../bots/content/user/{ID}.json') as file:
            userData = json.load(file)
            file.close() 
    except:
        loadUserData = {
            "main_load":{
                "RANK":[],
                "ACHIVM":[],
                "TITLE":[]
                }
            }
    
    user_CP = DataBase.Info(user_id=ID).user()
    user_M = DataBase.Info(user_id=ID).money()
    user_S = DataBase.Info(user_id=ID).any_table(table='user_wins_max')
    # user_diplomaty = RPG_DataBase.Info(user_id=ID).dip()
    # user_money = RPG_DataBase.Info(user_id=ID).money()
    
    userData = {
        "main":{
            "LVL":user_CP[1],
            "EXP":user_CP[2],
            "REP":user_CP[3],
            "RANK":userData["main_load"]["RANK"],
            "ACHIVM":userData["main_load"]["ACHIVM"],
            "TITLE":userData["main_load"]["TITLE"],
            # "CLAN": user_diplomaty["CLAN_ID"],
            # "GROUP": user_diplomaty["GROUP_ID"]
            },
        "money":{
            # "ES":user_money[]
            },
        "user_inventory":{
            
            }
        }



    # always back 'userData' type=dict
    return userData