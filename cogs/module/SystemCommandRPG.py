import disnake
from disnake.ext import commands
from random import randint

import asyncio
import json
import time

from .REQ_database import DataBase
from random import choices, choice

db = DataBase

class Exception(Exception): pass

class RpgCommand(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_button_click')
    async def fightListenerButtonsSwap(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'action_player':
            buttons = await getButtonsAction()
            await inter.response.edit_message(components=buttons)

        if inter.component.custom_id == 'item_player':
            buttons = await getButtonsItem()
            await inter.response.edit_message(components=buttons)

        if inter.component.custom_id in ['back_from_action', 'back_from_items']:
            buttons = await getButtonsFight()
            await inter.response.edit_message(components=buttons)
    
    @commands.Cog.listener('on_button_click')
    async def fightEndMovePlayer(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'attack_player':
            await inter.response.defer()
        if inter.component.custom_id == 'escape_player':
            await inter.response.defer()


async def createMetadata(message_id) -> dict:
    temporal = {
                "id":'S0',
                "next":"S0",
                "route_select":False,
                "exit":False,
                "message_id":message_id,

                "buffer":1
                }
    return temporal

#? Command for delete different embeds through time
async def deleteAfterEmbed(json_name:str, message:object, time:int) -> bool:
    try:
        await asyncio.sleep(time)
        with open(f"../bots/config/{json_name}", encoding='UTF-8') as file:
            data = json.load(file)
            del data[f'{message.id}']
            file.close()
        with open(f'../bots/config/{json_name}', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(data, indent=3, ensure_ascii=False))
            file.close()
        embed = disnake.Embed(title='Информация',description='```Окно закрыто системой.```')
        await message.edit(components=None, embed=embed)
        return True
    except:
        print('Code 2 >>> In method "deleteAfterEmbed" tiny problem.')

#? command for delete message after enter time
async def deleteAfter(message:object, time:int) -> None:
    await asyncio.sleep(time)
    await message.delete()

async def endDialogScene(message:int):
    await message.edit(components=None)

async def dialogWithoutSelect(text:list, tempo:int, message:object, end_button:object) -> None:
        for index, item in enumerate(text):
            if index != len(text)-1:
                embed = disnake.Embed(description=item)
                await message.edit(embed=embed, components=None)
                await asyncio.sleep(tempo)
            else:
                embed = disnake.Embed(description=item)
                await message.edit(embed=embed, components=end_button)

#? command for load dictonary user data, what need to statistic embed
async def userData(uid:int) -> dict:
    try:
        with open(f'../bots/content/user/{uid}.json', encoding='UTF-8') as file:
            userDataJ = json.load(file)
            file.close() 
    except:
        loadUserData = {
            "main_load":{
                "RANK":{},
                "ACHIVM":{},
                "TITLE":{}
                },
            "PERK":{
                "ACTIVE":{},
                "PASSIVE":{},
                "SPECIAL":{}
                }
            }
        with open(f'../bots/content/user/{uid}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(loadUserData, indent=3, ensure_ascii=False))
            file.close()
        with open(f'../bots/content/user/{uid}.json', 'r', encoding='UTF-8') as file:
            userDataJ = json.load(file)
            file.close()
        
    
    user_CP = DataBase.Info(user_id=uid).takeFromRPG(table='user_main_info')
    user_M = DataBase.Info(user_id=uid).takeFromRPG(table='user_money')
    user_S = DataBase.Info(user_id=uid).takeFromSystem(table='user_wins_max')
    user_INV = DataBase.Info(user_id=uid).takeFromRPG(table='user_active_inventory')
    user_DIP = DataBase.Info(user_id=uid).takeFromRPG(table='user_diplomaty')
    user_PR = DataBase.Info(user_id=uid).takeFromRPG(table='user_parametr')
    user_E = DataBase.Info(user_id=uid).takeFromRPG(table='user_equipment')

    userData = {
        "main":{
            "LVL":user_CP[1],
            "EXP":user_CP[2],
            "REP":user_CP[3],
            "RANK":userDataJ["main_load"]["RANK"],
            "ACHIVM":userDataJ["main_load"]["ACHIVM"],
            "TITLE":userDataJ["main_load"]["TITLE"],
            "CLAN": user_DIP[2],
            "GROUP": user_DIP[1]
            },
        "money":{
            "ESSENCE":user_M[1],
            "SHARD":user_M[2],
            "SOUL":user_M[3],
            "CRISTALL_SOUL":user_M[4],
            "COU":user_M[5],
            "VCOIN":user_M[6],
            "ACOIN":user_M[7],
            "TCOIN":user_M[8]
            },
        "equipment":{
            "HEAD":user_E[1],
            "FINGER_1":user_E[2],
            "FINGER_2":user_E[3],
            "NEAK":user_E[4],
            "HAND_L":user_E[5],
            "HAND_R":user_E[6],
            "BODY":user_E[7],
            "LEGS":user_E[8],
            "EMP_HEAD":user_E[9],
            "EMP_CHEST":user_E[10],
            "EMP_BELLY":user_E[11],
            "EMP_RHAND":user_E[12],
            "EMP_LHAND":user_E[13]
            },
        "parametr":{
            "HP":user_PR[1],
            "ATK":user_PR[2],
            "DEF":user_PR[3],
            "STR":user_PR[4],
            "LUCK":user_PR[5],
            "CRIT":user_PR[6],
            "CCRIT":user_PR[7],
            "ULT":user_PR[8],
            "REG":user_PR[9],
            "SS":user_PR[10],
            "FLX":user_PR[11],
            "STL":user_PR[12],
            "SEN":user_PR[13],
            "VIT":user_PR[14],
            "INS":user_PR[15],
            "CTR":user_PR[16],
            "GEN":user_PR[17],
            "FR":user_PR[18],
            "ER":user_PR[19],
            "AQ":user_PR[20],
            "WD":user_PR[21],
            "HL":user_PR[22],
            "WG":user_PR[23],
            "LG":user_PR[24],
            "DR":user_PR[25],
            "ST":user_PR[26]
            },
        "inventory":{
            "SLOT1":user_INV[1],
            "SLOT2":user_INV[2],
            "SLOT3":user_INV[3],
            "SLOT4":user_INV[4],
            "SLOT5":user_INV[5]
            },
        "perk":{
            "ACTIVE":userDataJ['PERK']['ACTIVE'],
            "PASSIVE":userDataJ['PERK']['PASSIVE'],
            "SPECIAL":userDataJ['PERK']['SPECIAL']
            },
        "dip":{
            "SUNSET":user_DIP[3],
            "TAYBLASS":user_DIP[4],
            "DARKBOOK":user_DIP[5],
            "FREESOVET":user_DIP[6],
            "FAME":user_DIP[7],
            "PET":user_DIP[8]
            }
        }



    # always back 'userData' type=dict
    return userData

async def getButtonsFight():
    '''it`s a just button for fight, nothing like that'''
    buttons = [
        disnake.ui.Button(style=disnake.ButtonStyle.danger, label='Атака', custom_id='attack_player'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='Цель', custom_id='select_target'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='Действие', custom_id='action_player'),
        disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='Предметы', custom_id='item_player'),
        disnake.ui.Button(style=disnake.ButtonStyle.gray, label='Побег', custom_id='escape_player')
        ]
    return buttons
async def getButtonsAction():
    # TODO: Добавить множественные проверки на наличие кнопок, по типу: Есть ли у пользователя возможности вора, по краже, или возможность целевого вампиризма. Желательно сделать это сразу, а также вывести списком возможные действия которые способен будет делать игрок
    buttons = [
        disnake.ui.Button(style=disnake.ButtonStyle.danger, label='A', custom_id='a'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='B', custom_id='b'),
        disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='C', custom_id='c'),
        disnake.ui.Button(style=disnake.ButtonStyle.gray, label='D', custom_id='d'),
        disnake.ui.Button(style=disnake.ButtonStyle.danger, label='F', custom_id='f'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='G', custom_id='g'),
        disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='I', custom_id='i'),
        disnake.ui.Button(style=disnake.ButtonStyle.gray, label='H', custom_id='h'),
        disnake.ui.Button(style=disnake.ButtonStyle.gray, label='Назад-1', custom_id='back_from_action')
        ]
    return buttons
async def getButtonsItem():
    buttons = [
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='1', custom_id='use_1_item'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='2', custom_id='use_2_item'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='3', custom_id='use_3_item'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='4', custom_id='use_4_item'),
        disnake.ui.Button(style=disnake.ButtonStyle.green, label='5', custom_id='use_5_item'),
        disnake.ui.Button(style=disnake.ButtonStyle.gray, label='Назад-2', custom_id='back_from_items')
        ]
    return buttons


async def CTX_ToDumpPickle(ctx):
    pass
async def createFightData(players:list):
    fightData = {
        "meta":{
            "itter":0
            }
        }
    for item in players:
        fightData[players.name] = {
            "move":None,
            "item":None
            }



#? Main function a interaction with lotery system
async def checkButtonsLotery(essence, priceTiket) -> 1 | 5 | 10:
    ''' This function return disnake.ui.Button(label='5|10')'''
    buttons = []

    if abs(essence) // priceTiket != 0: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id='lotery_1'))
    else: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id='lotery_1', disabled=True))

    if essence // priceTiket >= 5: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='5',custom_id='lotery_5'))
    else:buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='5',custom_id='lotery_5', disabled=True))

    if essence // priceTiket >= 10: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='10', custom_id='lotery_10'))
    else: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='10', custom_id='lotery_10', disabled=True))

    return buttons
async def rareColor(Rank) -> disnake.Colour:
    if Rank == 'EX': return disnake.Colour.teal()
    if Rank == 'S': return disnake.Colour.red()
    if Rank == 'A': return disnake.Colour.yellow()
    if Rank == 'B': return disnake.Colour.dark_purple()
    if Rank == 'C': return disnake.Colour.blue()
    if Rank == 'D': return disnake.Colour.green()
    if Rank == 'E': return disnake.Colour.default()
    if Rank == 'F': return disnake.Colour.dark_gray()
async def RollLotery(user, priceTiket, count:int = 1, sys:bool=False) -> map:
    if not 1 <= count <= 10: raise Exception('range count can be 1<count<10')

    with open('../bots/content/lotery/lowLotery.json', encoding='UTF-8') as file:
            load = json.load(file)
            box = load['items']
            compliments = load['compliments']
            del load
        
    async def getLoot(box):
        '''           ?↓   Ex↓     S↓    A↓     B↓     C↓    D↓    E↓     F↓'''
        lootChance = [0, 0.0001, 0.001, 0.005, 0.035, 0.07, 0.12, 0.199, 0.65]
        associateBox = []
        for item in box:
            associateBox.append(item)
        RankLoot = choices(associateBox, weights=lootChance)[0]
        rareColorRank = await rareColor(RankLoot)
        ids_loot = choice(range(1, len(box[f'{RankLoot}'])))
        winable = box[f'{RankLoot}'][f'{ids_loot}']
        RankLoot = f'{RankLoot}-{ids_loot}'
        loot = (RankLoot, winable, rareColorRank)
        del associateBox, box, RankLoot, winable, ids_loot
        DataBase.Poke(user=user).add(value=1, column='COUNTROLL')
        return loot

    if count != 1:
        loot = []
        for _ in range(count):
            loot.append(await getLoot(box=box))
    else:
        loot = [await getLoot(box=box)]

    if not sys:
        value = count*priceTiket
        
        if not DataBase.Money(user=user, value=value).sub():
            raise Exception('Где-то не сработали блокировки')
    
    if count == 1:
        compliment = choice(compliments[f'{loot[0][0].split('-')[0]}'])
    else:
        compliment = choice(compliments['mass'])
    
    user = await userData(uid=user)
    essence = user['money']['ESSENCE']
    buttons = await checkButtonsLotery(essence=essence, priceTiket=priceTiket)
    return {"loot":loot, "compliment":compliment, "buttons":buttons}
async def savePokemon(loot, uid:int) -> None:
    try:
        with open(f'../bots/content/lotery/users_bag/{uid}.json', 'r', encoding='UTF-8') as file:
            progress = json.load(file)

        for item in loot:
            order = {"?":-1,"EX":0, "S":1, "A":2, "B":3, "C":4, "D":5, "E":6, "F":7}
            for item_ in order: 
                if item[0].startswith(item_): rank = order[item_]

            namePokemon = item[1]['name']
            if namePokemon not in progress:
                progress[namePokemon] = {
                    "rank":[item[0], rank],
                    "count":1
                    }
            else:
                progress[namePokemon]['count'] += 1

        with open(f'../bots/content/lotery/users_bag/{uid}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(progress, indent=2, ensure_ascii=False))
    except: 
        progress = {}
        for item in loot:
            order = {"EX":0, "S":1, "A":2, "B":3, "C":4, "D":5, "E":6, "F":7}
            for item_ in order: 
                if item[0].startswith(item_): rank = order[item_]

            namePokemon = item[1]['name']
            if namePokemon not in progress:
                progress[namePokemon] = {
                    "rank":[item[0], rank],
                    "count":1
                    }
            else:
                progress[namePokemon]['count'] += 1

        with open(f'../bots/content/lotery/users_bag/{uid}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(progress, indent=2, ensure_ascii=False))

#? Work pokemon
async def checkValideWorkedFile(user:int):
    try:
        with open(f'../bots/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file: load = json.load(file)
        return load
    except:
        with open(f'../bots/content/lotery/user_pet_in_work/{user}.json', 'w', encoding='UTF-8') as file: 
            slots = {"SLOT1":None, "SLOT2":None, "SLOT3":None}
            file.write(json.dumps(slots, indent=2, ensure_ascii=False))
        with open(f'../bots/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file: load = json.load(file)
        return load

async def checkHavePokemonInBag(pokemon:str, user):
    '''Give only name'''
    workfile, cashincome = await getWorkPokemon(user=user, sys=False)
    for item in workfile:
        try: 
            if str(pokemon.lower()) == str(workfile[item]['name'].lower()): return True
        except: pass
    return False
async def giveUserBag(user) -> map:
    with open(f'../bots/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
        userBag = json.load(file)
    return userBag

async def findPokemonInUserBag(pokemon:str, user) -> bool:
    '''Give a name or ID pokemon'''
    with open(f'../bots/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
        userBag = json.load(file)
    for item in userBag:
        if item.lower() == pokemon.lower(): return True
        if userBag[item]['rank'][0] == pokemon: return True
    return False

async def findPokemonInDatebase(ID:str):
    with open('../bots/content/lotery/lowLotery.json', encoding='UTF-8') as file:
        load = json.load(file)
        pokemons = load['items']
        del load
    
    rank, numItem = ID.split('-')
    return pokemons[rank][numItem]
async def findPokemonInDatabaseLikeName(name) -> map | bool:
    with open('../bots/content/lotery/lowLotery.json', 'r', encoding='UTF-8') as file:
        load = json.load(file)
        pokemons = load['items']
        del load
    
    for item in pokemons:
        for low in pokemons[item]:
            if pokemons[item][low]['name'].lower() == name.lower(): return pokemons[item][low], (item, low)
    return False

async def saveWorkFile(workfile, user):
    with open(f'../bots/content/lotery/user_pet_in_work/{user}.json', 'w', encoding='UTF-8') as file: 
        file.write(json.dumps(workfile, indent=3, ensure_ascii=False))
    return True
async def saveBagUserFile(userFile, user) -> bool:
    try:
        with open(f'../bots/content/lotery/users_bag/{user}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(userFile, indent=3, ensure_ascii=False))
        return True
    except: return False

async def setWorkPokemon(pokemon_id:str, user, slot:1|2|3) -> bool:
    findPoke = await findPokemonInDatebase(ID=pokemon_id)
    workFile = await checkValideWorkedFile(user=user)
    checkHave = await checkHavePokemonInBag(findPoke['name'], user=user)
    if checkHave: return False
    workFile[f'SLOT{slot}'] = {
            "name":findPoke['name'],
            "time":round(time.time()),
            "cashIncome":findPoke['income']
        }
    await saveWorkFile(workFile, user)
    return True    
async def getWorkPokemon(user, sys:bool) -> tuple:
    workerPokemon = await checkValideWorkedFile(user=user)
    cashIncome = await calculateValueWorkPokemon(user=user, sys=sys)
    return workerPokemon, cashIncome
async def calculateValueWorkPokemon(user, sys=False):
    workFile = await checkValideWorkedFile(user)
    slotsItem = ['SLOT1', 'SLOT2', 'SLOT3']
    incomeList = {}
    timeNow = round(time.time())
    timeSleep = 0
    for item in slotsItem:
        try:
            timeSleep = (timeNow-workFile[item]['time'])//3600
            if timeSleep > 10: timeSleep = 10
            incomeList[item] = {
                "name":workFile[item]['name'],
                "pastTense":timeSleep,
                "income":timeSleep*workFile[item]['cashIncome']}
            if sys and timeSleep > 0: 
                await stampTimePokemon(user=user, slot=item[4])
        except:
            incomeList[item] = None
    slots = {
        "SLOT1":incomeList['SLOT1'],
        "SLOT2":incomeList['SLOT2'],
        "SLOT3":incomeList['SLOT3']
        }
    
    del workFile, slotsItem, incomeList, timeNow
    return slots
async def stampTimePokemon(user, slot:1|2|3):
    workfile = await checkValideWorkedFile(user=user)
    workfile[f'SLOT{slot}']['time'] = round(time.time())
    await saveWorkFile(workfile=workfile, user=user)
async def checkStrikeWork(strike) -> float:
    if 10 > strike: return 1.0
    if 25 > strike: return 2.5
    if 50 > strike: return 5.0
    if 75 > strike: return 7.5
    if 100 > strike: return 10.0
    return 15.0

#? Function what they allow sell or buy on time market pokemon
async def sellPokemon(pokemon:list, user) -> bool:
    with open(f'../bots/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
        userBag = json.load(file)
    with open(f'../bots/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file:
        userWorPoke = json.load(file)

    pokeCountList = []
    listCorrectSells = []
    async def sell(pokemon):
        checkHavePoke = await findPokemonInUserBag(pokemon['name'], user=user)
        if checkHavePoke:
            pokemonCount = userBag[pokemon['name']]['count']
            del userBag[pokemon['name']]
            for item in userWorPoke:
                try:
                    if userWorPoke[item]['name'] == pokemon['name']:
                        userWorPoke[item] = None
                except: pass
            await saveBagUserFile(userFile=userBag, user=user)
            await saveWorkFile(workfile=userWorPoke, user=user)
            sellIncome = round(pokemon['price'] * 0.75) * pokemonCount
            if db.Money(user=user, value=sellIncome).add(): 
                listCorrectSells.append(True)
                return pokeCountList.append(pokemonCount)
        else: 
            listCorrectSells.append(False)
            return pokeCountList.append(None)
    
    # try:
    for item in pokemon:
        await sell(item)
    return (listCorrectSells, pokeCountList)
    # except: 
    #     print('exit 2')
    #     return (False, None)

async def GetTiketPrice(user) -> int:
    userLVL = db.Info(user_id=user).takeFromRPG(table='user_main_info')[1]
    userCountRoll = db.Info(user_id=user).takeFromRPG(table='user_money_poke')[3]
    userBag = await giveUserBag(user=user)

    if userLVL <= 0: userLVL = 0

    return 500 + (100 * (userLVL//2)) + (100 * (userCountRoll//100)) + (100 * (len(userBag)//4))


#? get a property of pokemon
async def getPropertyPokemonBase(pokemon):
    pass
async def getPropertyPokemonBase(pokemon, user):
    pass

#? Function what thay allow a upgrade pokemon
async def upgradePokemonTo(pokemon_id, user) -> bool:
    pass


#? Function craft/uncraft system. just a convert cash
async def getChance() -> float:
    pass
async def craftCurrency(cash_name, value, user) -> bool:
    pass
async def unCraftCurrency(cash_name, value, user) -> bool:
    pass


# unstatic load module, it`s just for simplicity
def setup(bot:commands.Bot):
    bot.add_cog(RpgCommand(bot))