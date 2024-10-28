import disnake
from disnake.ext import commands

import asyncio
import json
import time

from .REQ_database import DataBase
from random import choices, choice, randrange

from .SystemCommandRPG import userData

db = DataBase

def associateOrderRank(rank, reverse:bool=False) -> int|str:
    order = {"?":-1,"EX":0, "S":1, "A":2, "B":3, "C":4, "D":5, "E":6, "F":7}
    orderReverse = {-1:"?", 0:"EX", 1:"S", 2:"A", 3:"B", 4:"C", 5:"D", 6:"E", 7:"F"}

    if reverse: return orderReverse[rank]
    return order[rank]

#? Main function a interaction with lotery system
async def checkButtonsLotery(essence, priceTiket) -> list:
    ''' This function return disnake.ui.Button(label='5|10')'''
    buttons = []

    if abs(essence) // priceTiket != 0: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id='lotery_1'))
    else: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id='lotery_1', disabled=True))

    if essence // priceTiket >= 5: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='5',custom_id='lotery_5'))
    else:buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='5',custom_id='lotery_5', disabled=True))

    if essence // priceTiket >= 10: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='10', custom_id='lotery_10'))
    else: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='10', custom_id='lotery_10', disabled=True))

    if essence // priceTiket >= 50: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='50', custom_id='lotery_50'))
    else: buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label='50', custom_id='lotery_50', disabled=True))

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
async def RollLotery(user, priceTiket=100, count:int = 1, sys:bool=False) -> map:
    if not 1 <= count <= 100: raise Exception('range count can be 1 <= count <= 100')

    if not sys:
        value = count*priceTiket
        
        if not DataBase.Money(user=user, value=value).sub():
            raise Exception('Где-то не сработали блокировки')

    with open('../PonyashkaDiscord/content/lotery/lowLotery.json', encoding='UTF-8') as file:
            load = json.load(file)
            box = load['items']
            compliments = load['compliments']
            del load

    async def getLoot(box, userBag):
        '''           ?↓   Ex↓     S↓    A↓     B↓     C↓    D↓    E↓     F↓'''
        lootChance = [0, 0.0001, 0.001, 0.005, 0.035, 0.07, 0.12, 0.199, 0.65]
        order = ["?", "EX", "S", "A", "B", "C", "D", "E", "F"]

        # Определение ранга, что выигрвывает
        rankWin = choices(order, weights=lootChance)
        rareColorRank = await rareColor(rankWin)

        # создания списка одного выиграного ранга
        associateBox = []
        for item in box:
            if box[item]['rank'] == rankWin[0]: associateBox.append(item)

        # Выборка победителя (ID)
        ids = choice(associateBox)
        
        try:
            if len(userBag[f'{ids}'])+1 > 20: selled = True
            else: selled = False

        except KeyError as error:
            selled = False

        loot = (ids, box[ids], rareColorRank, selled, box[ids]['rank'])

        del associateBox, box, ids, rankWin, rareColorRank, selled

        if not sys: DataBase.Poke(user=user).add(value=1, column='COUNTROLL')
        return loot

    listTrait = ['duplicator', 'chronojump', 'goldrained', 'deadlyluck', 'berserk', 'greenhouse', 'shield', 'armored_permove', 'mole', 'lucky', 'perk_slot']
    listProperty = ['attack', 'healpoint', 'armor', 'speed', 'evasion', 'regen']
    listCurrency = ['price', 'income']

    import copy

    if count != 1:
        #? Множественный ролл

        lootEnd = []
        sellIncome = 0

        for _ in range(count):
            
            userBag = await giveUserBag(user=user)

            getPokes = await getLoot(box=box, userBag=userBag)
            loot = copy.deepcopy(getPokes[1])

            loot['price'] = randrange(loot['price'][0], loot['price'][1], 10)
            loot['income'] = randrange(loot['income'][0], loot['income'][1], 5)

            for item in listTrait:
                if loot['trait'][item] is None: del loot['trait'][item]
            for item in listProperty:

                if item in ['armor', 'evasion']:
                    diapozone = loot['params'][item]
                    try: loot['params'][item] = randrange(round(diapozone[0]*100), round(diapozone[1]*100), 1)/100
                    except: loot['params'][item] = 0

                if item == 'speed':
                    diapozone = loot['params'][item]
                    loot['params'][item] = choice(diapozone)

                if item in ['attack', 'healpoint', 'regen']:
                    diapozone = loot['params'][item]
                    loot['params'][item] = randrange(diapozone[0], diapozone[1], 5)

            # Либо продажа, либо сохранение в инвертарь
            if getPokes[3]:
                timesSellIncome = round(loot['price'] * 0.75)
                sellIncome += timesSellIncome

                db.Money(user=user, value=timesSellIncome).add()

            else:
                savePokemon(loot=[(getPokes[0], loot, getPokes[2], getPokes[3], getPokes[4])], uid=user)
            lootEnd.append((getPokes[0], loot, getPokes[2], getPokes[3]))
            del loot


    else:
        userBag = await giveUserBag(user=user)

        getPokes = await getLoot(box=box, userBag=userBag)
        loot = copy.deepcopy(getPokes[1])

        sellIncome = 0

        for item in listTrait:
            if loot['trait'][item] is None: del loot['trait'][item]

        for item in listProperty:

            if item in ['armor', 'evasion']:
                diapozone = loot['params'][item]
                try: loot['params'][item] = randrange(round(diapozone[0]*100), round(diapozone[1]*100), 1)/100
                except: loot['params'][item] = 0

            if item == 'speed':
                diapozone = loot['params'][item]
                loot['params'][item] = choice(diapozone)

            if item in ['attack', 'healpoint', 'regen']:
                diapozone = loot['params'][item]
                loot['params'][item] = randrange(diapozone[0], diapozone[1], 5)
        
        if getPokes[3]:
                timesSellIncome = round(loot['price'] * 0.75)
                sellIncome += timesSellIncome

                db.Money(user=user, value=timesSellIncome).add()

        else:
            savePokemon(loot=[(getPokes[0], loot, getPokes[2], getPokes[3], getPokes[4])], uid=user)

        lootEnd = [(getPokes[0], loot, getPokes[2], getPokes[3])]
    
    
    if count == 1:
        compliment = choice(compliments[f'{lootEnd[0][1]['rank']}'])
    else:
        compliment = choice(compliments['mass'])
    
    user = await userData(uid=user)
    essence = user['money']['ESSENCE']
    buttons = await checkButtonsLotery(essence=essence, priceTiket=priceTiket)
    return {"loot":lootEnd, "compliment":compliment, "buttons":buttons, "sellIncome":sellIncome}
def savePokemon(loot, uid:int) -> None:
    '''Save without trade, for trade use other command «saveAfterTradePoke()»'''
    try:
        with open(f'../PonyashkaDiscord/content/lotery/users_bag/{uid}.json', 'r', encoding='UTF-8') as file:
            progress = json.load(file)
    except:
        progress = {}


    for item in loot:
        ids = item[0]

        # order = {"?":-1,"EX":0, "S":1, "A":2, "B":3, "C":4, "D":5, "E":6, "F":7}

        #rebuild slot perks pokemon
        rg = item[1]['trait']['perk_slot']
        item[1]['trait']['perk_slot'] = [{f"slot{i+1}":None} for i in range(rg)]
        poke = {
            "name":item[1]['name'],
            "rank":item[4],
            "trait":item[1]['trait'],
            "params":item[1]['params'],
            "other_param":{
                "lvl":0,
                "exp":0,
                "essence_drop":0,
                "timestamp_hp":0,
                "healpoint_now":item[1]['params']['healpoint'],
                
                "supports":0,
                "supports_percent_up":0
                },
            "curr":{
                "price":item[1]['price'],
                "income":item[1]['income'],
                "power":1.0
                },
            "owner":uid,
            "holder":[uid]
            }
        try:
            count = 1
            while True: 
                if str(count) in progress[ids]:
                    count += 1
                    continue
                progress[ids][count] = poke
                break
        except:
            try:
                progress[ids] = {"1":poke}
            except:
                progress[ids] = {
                        "1":poke    
                    }
            
        with open(f'../PonyashkaDiscord/content/lotery/users_bag/{uid}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(progress, indent=2, ensure_ascii=False))


async def userHaveTicket(user) -> int:
    return db.Poke(user=user).takeAll()[4]

#? Work pokemon
async def checkValideWorkedFile(user:int):
    try:
        with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file: load = json.load(file)
        return load
    except:
        with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'w', encoding='UTF-8') as file: 
            slots = {"SLOT1":None, "SLOT2":None, "SLOT3":None}
            file.write(json.dumps(slots, indent=2, ensure_ascii=False))
        with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file: load = json.load(file)
        return load

async def checkHavePokemon_WorkFile(rankCOM_poke:str, user):
    '''Give only rankCOM (rank-order-num)'''
    workfile, cashincome = await getWorkPokemon(user=user, sys=False)

    ids, seq = rankCOM_poke.split('-')
    poke = await findMap_PokemonInDB_LikeID(ID=ids)
    
    for item in workfile:
        if workfile[item] is None: continue
        if str(poke['name'].lower()) == str(workfile[item]['name'].lower()): 
            return True, item
    return False, None
async def checkHavePokemon_UserBag(rankCOM_poke:str, user):
    '''Give only rankCOM (rank-order-num)'''
    userBag = await giveUserBag(user=user)
    rank, orde, num = rankCOM_poke.split('-')

    try:
        check = userBag[rank][orde][num]
        return True
    except:
        return False

async def giveUserBag(user) -> map:
    try:
        with open(f'../PonyashkaDiscord/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
            userBag = json.load(file)
    except:
        with open(f'../PonyashkaDiscord/content/lotery/users_bag/{user}.json', 'w', encoding='UTF-8') as file:
            data = {}
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
        with open(f'../PonyashkaDiscord/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
            userBag = json.load(file)
    return userBag

async def checkingPokemonAvialbility(name_or_id:str|int):
    pass

async def findID_PokemonInDB_LikeName(PokemonName:str) -> str:
    # ID == ID 
    with open('../PonyashkaDiscord/content/lotery/lowLotery.json', encoding='UTF-8') as file:
        load = json.load(file)
        pokemons = load['items']
        del load
    
    for item in pokemons:
        if PokemonName.lower() == pokemons[item]['name'].lower(): return item
    return None   
async def findMap_PokemonInUserBag_LikeName(pokemonName:str, user) -> bool:
    # ID == ID 
    '''Give a name or ID pokemon'''
    with open(f'../PonyashkaDiscord/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
        userBag = json.load(file)

    for item in userBag:
        randomSelect = userBag[item][choice(list(userBag[item].keys()))]
        if pokemonName.lower() == randomSelect['name'].lower(): return True

    return False
async def findMap_PokemonInDB_LikeID(ID:str):
    # ID 
    with open('../PonyashkaDiscord/content/lotery/lowLotery.json', encoding='UTF-8') as file:
        load = json.load(file)
        pokemons = load['items']
        del load
    return pokemons[ID]
async def findMap_PokemonInDB_LikeName(name) -> map | bool:
    with open('../PonyashkaDiscord/content/lotery/lowLotery.json', 'r', encoding='UTF-8') as file:
        load = json.load(file)
        pokemons = load['items']
        del load
    
    for ids in pokemons:
        if pokemons[ids]['name'].lower() == name.lower(): return pokemons[ids], ids
    return False

async def findPokemonInUserBag_LikeName(name) -> tuple:
    pass
async def findPokemonInUserBag_LikeID(name) -> tuple:
    pass

async def saveWorkFile(workfile, user):
    with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'w', encoding='UTF-8') as file: 
        file.write(json.dumps(workfile, indent=3, ensure_ascii=False))
    return True
async def saveBagUserFile(userFile, user) -> bool:
    try:
        with open(f'../PonyashkaDiscord/content/lotery/users_bag/{user}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(userFile, indent=3, ensure_ascii=False))
        return True
    except: return False

async def setWorkPokemon(rankCOM:str, user, slot:1|2|3) -> bool:

    ids, seq = rankCOM.split('-')

    workFile = await checkValideWorkedFile(user=user)
    checkHave, workFilePokes = await checkHavePokemon_WorkFile(rankCOM_poke=rankCOM, user=user)
    userPoke = await giveUserBag(user=user)

    poke = userPoke[ids][seq]

    if checkHave:
        if not workFilePokes.endswith(str(slot)): return False
        if workFile[workFilePokes]['cashIncome'] > poke['curr']['income']: return False

    workFile[f'SLOT{slot}'] = {
            "name":poke['name'],
            "time":round(time.time()),
            "cashIncome":poke['curr']['income']
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
    with open(f'../PonyashkaDiscord/content/lotery/users_bag/{user}.json', 'r', encoding='UTF-8') as file:
        userBag = json.load(file)
    with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file:
        userWorPoke = json.load(file)

    pokeCountList = []
    listCorrectSells = []
    async def sell(pokemon):
        checkHavePoke = await findPokemonInUserBag_LikeName(pokemon['name'], user=user)

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

async def getLenUserBag(userBag) -> int:
    count = 0
    for ranks in userBag:
        for numbers in userBag[ranks]:
            if numbers == 'weight': continue
            count += len(userBag[ranks][numbers])
    return count
async def GetTiketPrice(user) -> int:
    userLVL = db.Info(user_id=user).takeFromRPG(table='user_main_info')[1]
    userCountRoll = db.Info(user_id=user).takeFromRPG(table='user_poke')[3]
    userBag = await giveUserBag(user=user)

    if userLVL <= 0: userLVL = 0

    lenBag = await getLenUserBag(userBag=userBag)
    return 10000 + (100 * (userLVL//2)) + (100 * (userCountRoll//100)) + (100 * (lenBag//4))


#? get a property of pokemon, this a start function fight system between pokemon
#? maybe i can use this system to big fight system a RPG module idk
#? but start it's small a piece way
#! warning! i fucked noob for this moment, dude don't fire at pony! plz!

async def saveFightGroup(rankCOM, user:int, slot:int):
    '''Slot take a 1|2|3 and nothing else. Pony sure.'''
    fightPet = await takeFightGroup(user=user)
    fightPet[f'slot{slot}'] = rankCOM
    with open(f'../PonyashkaDiscord/content/lotery/fightPet/{user}.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(fightPet))

async def takeFightGroup(user:int):
    try:
        with open(f'../PonyashkaDiscord/content/lotery/fightPet/{user}.json', 'r', encoding='UTF-8') as file:
            fightPet = json.load(file)
        return fightPet
    except:
        fightPet = {
            'slot1':None,
            'slot2':None,
            'slot3':None
            }
        with open(f'../PonyashkaDiscord/content/lotery/fightPet/{user}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(fightPet))
        return fightPet


async def setDescriptionTextWorkGroup(user):
    workPoke, cashIncome = await getWorkPokemon(user=user, sys=False)
    text = ''
    for index, item in enumerate(workPoke):
        if not workPoke[item]:
            text += f'** `{index+1}`: `Пустой слот`**\n| —\n'
            continue
        income = cashIncome[item]
        text += f' **`{index+1}`**: **`{income['name']}`** **`({workPoke[item]['cashIncome']:,}/h)`**\n| Собрано: `({income['income']})`\n| С последнего сбора: `({time.strftime('%H:%M:%S', time.gmtime(round(time.time())-workPoke[item]['time']))})`\n'
    else:
        text += f'-# _Для сбора используйте команду !work._'
    return text
async def setButtonsWorkGroup(message, rare, user):
    buttons = [
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id=f'selectWorkSlot-1|{rare}|{user}'),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='2', custom_id=f'selectWorkSlot-2|{rare}|{user}'),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='3', custom_id=f'selectWorkSlot-3|{rare}|{user}')
            ]
    await message.edit(components=buttons)
async def setButtonsFightGroup(message, data:tuple):
    buttons = [
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id=f'selectFightSlot-1|{data[0]}|{data[1]}'),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='2', custom_id=f'selectFightSlot-2|{data[0]}|{data[1]}'),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='3', custom_id=f'selectFightSlot-3|{data[0]}|{data[1]}')
            ]
    await message.edit(components=buttons)


def DelicateInjectWorkFile(user, pokemon):
            with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file:
                userWorkPoke = json.load(file)
            for item in userWorkPoke:
                try:
                    if userWorkPoke[item]['name'] == pokemon['name'] and userWorkPoke[item]['cashIncome'] == pokemon['curr']['income']:
                        userWorkPoke[item] = None
                except: pass
async def endSellPokeAfterSelect(pokemon_ids:str, user, message):

    userBag = await giveUserBag(user=user)
    ids, seq = pokemon_ids.split('-')

    pokemon = userBag[ids][seq]
    
    text = f'✔ **Покемон [{pokemon['name']}] был продан за `{round(pokemon['curr']['price']*0.75)}`es** \n'

    embed = disnake.Embed(
            description=text
            ).set_footer(text='Покемон продаётся за 75% от стоимости')
    
    import copy 
    price = copy.copy(userBag[ids][seq]['curr']['price'])
    del userBag[ids][seq]
    if len(userBag[ids]) == 1: del userBag[ids]

    db.Money(user=user, value=round(price*0.75)).add()
    del price

    DelicateInjectWorkFile(user=user, pokemon=pokemon)
    await saveBagUserFile(userBag, user)
    await message.edit(embed=embed)


def addTiket(user, value, price):
    db.Money(user=user, value=value*price).sub()
    db.Poke(user=user).add(value=value, column='TIKET')

def addSoul(user, value, price):
    db.Money(user=user, value=value*price, currency='SHARD').sub()
    db.Money(user=user, value=value, currency='SOUL').add()
    
def addPokeEssence(user, value, price):
    db.Money(user=user, value=value*price).sub()
    db.Poke(user=user).add(value=value, column='POKE_ESSENCE')

# Just locale params and stats
async def AllockatePokemons(name:str) -> str:
    listTrait = {
        'duplicator':'Дубликатор', 'chronojump':'Хронопрыжок', 
        'goldrained':'Злато-дождь', 'deadlyluck':'Смертоудача', 
        'berserk':'Берсерк', 'greenhouse':'Тепличность', 
        'shield':'Щит', 'armored_permove':'Чешуя', 
        'mole':'Кротовик', 'lucky':'Удачливость', 
        'perk_slot':'Слотов навыков'}
    listProperty = {
        'attack':'Урон', 'healpoint':'Здоровье', 
        'armor':'Броня', 'speed':'Скорость', 
        'evasion':'Уклонение', 'regen':'Регенерация'}

    for item in listProperty:
        if name == item: return listProperty[item]
    for item in listTrait:
        if name == item: return listTrait[item]
    return '`[Неизвестное]`'


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





class PokeCom(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
# unstatic load module, it`s just for simplicity
def setup(bot:commands.Bot):
    bot.add_cog(PokeCom(bot))