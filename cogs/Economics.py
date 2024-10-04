import disnake
from disnake.ext import commands
from .module import REQ_database as Rdb

import json
import time
from random import choice, choices, randint, random, randrange
from .module.SystemCommandRPG import *

db = Rdb.DataBase

class Economics(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    #? Добавить стриковую градацию <10/1 <25/2,5 <50/5 <75/7.5 <100/10 endless/15
    @commands.command(name='work', aliases=['работа', 'раб'])
    async def work(self, ctx):

        if db.Lock(user_id=ctx.author.id, slot=1).ready() or ctx.author.id == 374061361606688788:
            db.Check(user_id=ctx.author.id, user_name=ctx.author.name).user()
            cashIncome = await calculateValueWorkPokemon(user=ctx.author.id, sys=True)

            info = db.Poke(user=ctx.author.id).takeAll()
            strikeMulti = await checkStrikeWork(info[1])
            timestamp = (round(time.time()) - info[2])//3600
            strikeup = 24 > timestamp >= 0
            dropstrike = (timestamp//24) > 5

            text = ''
            pokemonIncome = 0
            for item in cashIncome:
                if cashIncome[item] is None:
                    continue
                if cashIncome[item]['pastTense'] > 0:
                    pokemonIncome += int(cashIncome[item]['income'])
                    text += f'[{cashIncome[item]['name']}] принес(-ла): **`{cashIncome[item]['income']}`**\n'

            cash = round(randint(15, 120) * strikeMulti)
            embed = disnake.Embed(description=f'### Вы заработали: `{cash}es`\n\n{text}\n`Приходите позже!`', colour=disnake.Colour.dark_green())
            embed.set_footer(text=f'Вызвал: {ctx.author.name}.   Текущий стрик: {info[1]+1} = {strikeMulti}x')
            cash += pokemonIncome
            if db.Money(user=ctx.author.id, value=cash).add():
                if strikeup and not dropstrike: 
                    db.Poke(user=ctx.author.id).update(value=round(time.time()))
                    db.Poke(user=ctx.author.id).add(value=1)
                elif dropstrike:
                    db.Poke(user=ctx.author.id).update(value=round(time.time()))
                    db.Poke(user=ctx.author.id).update(value=0, time=False)
                db.Lock(user_id=ctx.author.id, slot=1, value=14400).lock()
                await ctx.send(embed=embed)
            else: await ctx.send('Сообщите поню, я опять сломана')
        else:
            to_formated_time = db.Lock(user_id=ctx.author.id, slot=1).info()[0] - round(time.time())
            end_time = time.strftime('%H:%M:%S', time.gmtime(to_formated_time))
            embed = disnake.Embed(description=f'### Не торопитесь так сильно\n`приходите через: {end_time}`', colour=disnake.Colour.dark_red())
            embed.set_footer(text=f'Вызвал: {ctx.author.name}')
            await ctx.send(embed=embed)

    @commands.Cog.listener('on_button_click')
    async def loteryListener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ['lotery_1', 'lotery_5', 'lotery_10']:
            return

        if inter.component.custom_id == 'lotery_1':
            priceTiket = await GetTiketPrice(inter.author.id)
            data = await RollLotery(user=inter.author.id, priceTiket=priceTiket)
            loots = data['loot'][0]
            embed = disnake.Embed(
                description=f"# ```Ты выиграл в лотери...```\n## → {loots[1]['name']} `(Rank: {loots[0]})`\n## `{data['compliment']}`\n",
                colour=loots[2]           
                )
            embed.set_footer(text=f'Крутил барабан: <{inter.author.name}> | Цена за тикет = <{priceTiket}>')
            await savePokemon(loot=data['loot'], uid=inter.author.id)
            await inter.response.edit_message(embed=embed, components=data['buttons'])
        elif inter.component.custom_id == 'lotery_5':
            priceTiket = await GetTiketPrice(inter.author.id)
            data = await RollLotery(user=inter.author.id, count=5, priceTiket=priceTiket)
            text = ''
            for index, item in enumerate(data['loot']):
                text += f'## ({index+1})→ {item[1]['name']} `(Rank: {item[0]})`\n'
            embed = disnake.Embed(
                description=f"# ```Ты выиграл в лотери...```\n{text}\n## `{data['compliment']}`\n",
                colour=disnake.Colour.dark_gold()           
                )
            embed.set_footer(text=f'Крутил барабан: <{inter.author.name}> | Цена за тикет = <{priceTiket}>')
            await savePokemon(loot=data['loot'], uid=inter.author.id)
            await inter.response.edit_message(embed=embed, components=data['buttons'])
        elif inter.component.custom_id == 'lotery_10':
            priceTiket = await GetTiketPrice(inter.author.id)
            data = await RollLotery(user=inter.author.id, count=10, priceTiket=priceTiket)
            text = ''
            for index, item in enumerate(data['loot']):
                text += f'## ({index+1})→ {item[1]['name']} `(Rank: {item[0]})`\n'
            embed = disnake.Embed(
                description=f"# ```Ты выиграл в лотери...```\n{text}\n## `{data['compliment']}`\n",
                colour=disnake.Colour.dark_gold()           
                )
            embed.set_footer(text=f'Крутил барабан: <{inter.author.name}> | Цена за тикет = <{priceTiket}>')
            await savePokemon(loot=data['loot'], uid=inter.author.id)
            await inter.response.edit_message(embed=embed, components=data['buttons'])
        
    @commands.command(name='lotery', aliases=['лотерея', 'гача'])
    async def lotery(self, ctx):
        
        user = await userData(ctx.author.id)
        essence = user['money']['ESSENCE']
        priceTiket = await GetTiketPrice(ctx.author.id)
        if priceTiket*5 > essence >= priceTiket:
            data = await RollLotery(user=ctx.author.id, priceTiket=priceTiket)
            loots = data['loot'][0]
            embed = disnake.Embed(
                description=f"# ```Ты выиграл в лотери...```\n# {loots[1]['name']} `(Rank: {loots[0]})`\n## `{data['compliment']}`\n",
                colour=loots[2]         
                )
            embed.set_footer(text=f'Крутил барабан: <{ctx.author.name}> | Цена за тикет = <{priceTiket}>')
            await savePokemon(loot=data['loot'], uid=ctx.author.id)
            await ctx.send(embed=embed, components=data['buttons'])
        elif essence > priceTiket*5:
            user = await userData(ctx.author.id)
            essence = user['money']['ESSENCE']
            buttons = await checkButtonsLotery(essence=essence, priceTiket=priceTiket)
            embed = disnake.Embed(
                description="### Сколько желаете открыть?",
                colour=disnake.Colour.dark_orange()
                )
            embed.set_footer(text=f'Вызвал окно: {ctx.author.name}')
            await ctx.send(embed=embed, components=buttons)
        else:
            embed = disnake.Embed(
                description=f'```Похоже у вас не хватает средств\nСтоимость 1 крутки для вас равна {priceTiket} шекелям.```',
                colour=disnake.Colour.dark_red()
                )
            embed.set_footer(text=f'Вызвал окно: <{ctx.author.name}?')
            await ctx.send(embed=embed)

    @commands.command(name='pokemon', aliases=['петы', 'покемоны', 'poke'])
    async def pokemon(self, ctx):


        try:
            with open(f'../bots/content/lotery/users_bag/{ctx.author.id}.json', 'r', encoding='UTF-8') as file:
                userBag = json.load(file)
            with open(f'../bots/content/lotery/lowLotery.json', 'r', encoding='utf-8') as file:
                load = json.load(file)
                loteryItem = load['items']
        except:
            embed = disnake.Embed(description='Пусто')
            await ctx.send(embed=embed)
            return

        text = ''
        order = ["?", "EX", "S", "A", "B", "C", "D", "E", "F"]
        sortedBag = sorted(userBag, key=lambda k: userBag[k]['rank'][1])
        sortedListRank = {}
        
        for item in order:
            for item_ in sortedBag:
                rank = userBag[item_]['rank'][0].split('-')[0]
                if rank == item and rank not in sortedListRank:
                    sortedListRank[item] = [item_]
                elif rank == item and rank in sortedListRank:
                    sortedListRank[item].append(item_)



        for item in order:
            if not item in sortedListRank:
                continue

            text += f'```{item} - rank ({len(sortedListRank[item])}/{len(loteryItem[item])})```'
            for index, sortitem in enumerate(sortedListRank[item]):
                pet = userBag[sortitem]
                if len(sortedListRank[item]) != index+1: 
                    text += f'**`({pet['count']})-{sortitem}`,** '
                else: 
                    text += f'**`({pet['count']})-{sortitem}`**'

        embed = disnake.Embed(
            description=f"{text}"
            )
        embed.set_footer(text=f'Вызвал: {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.Cog.listener("on_button_click")
    async def craftListener(self, inter: disnake.MessageInteraction):
        check = ['essence_soul_cf', 'shard_soul_cf']
        for item in check:
            if inter.component.custom_id.startswith(item):break
        else: return
        component = inter.component.custom_id.split('|')[0]
        user = int(inter.component.custom_id.split('|')[1])
        value = int(inter.component.custom_id.split('|')[2])
        if user != inter.author.id:
            await inter.response.send_message('Данное взаимодействие не принадлежит вам.', ephemeral=True)
            return

        # Крафт осколков душ
        # Коэффициент 400 к 1
        if component == 'essence_soul_cf':
            # Проверка наличие указаных средств у пользователя
            check = db.Money(user=user).have()
            if value > check:
                embed = disnake.Embed(description='**Недостаточно средств**', color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            shardValue = value//400
            # Шанс дропа шардов
            chanceDrop = float('{:.3f}'.format(value / (value+100)))
            # Не больше 80%
            if chanceDrop > 0.8: chanceDrop = 0.800

            # Создание диапазона выпадающих шардов
            minDrop = int(shardValue * 0.7)
            if minDrop <= 0: minDrop = 1
            maxDrop = int(round(shardValue * 1.3))
            if maxDrop <= 1: maxDrop = 2
            lossEssence = int(value*0.8)
            # Сколько будет потеряно в случае неудачи
            if lossEssence <= 10: lossEssence = value
            # Рандоминг чисел. Шанса и числа шардов
            randomNum= float('{:.3f}'.format(random()))
            ShardDrop = randint(minDrop, maxDrop)

            if chanceDrop > randomNum:
                # Позитивный исход
                db.Money(user=user, currency='ESSENCE', value=value).sub()
                db.Money(user=user, currency='SHARD', value=ShardDrop).add()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ `[{:.1%}]`\n**Вы получили:**ㅤㅤㅤ`[{ShardDrop}]` осколок(-ов)'.format(chanceDrop, ShardDrop= ShardDrop),
                    color= disnake.Colour.green())
                return await inter.response.edit_message(embed=embed, components=None)
            else:
                # Негативный исход
                db.Money(user=user, currency='ESSENCE', value=lossEssence).sub()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ `[{:.1%}]`\n**Вы потеряли (80%):**ㅤ`[{lossEssence}]` эссенций'.format(chanceDrop, lossEssence= lossEssence),
                    color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
        # Крафт душ
        # Коэффициент 1200 к 1
        elif component == 'shard_soul_cf':
            # Проверка наличие указаных средств у пользователя
            check = db.Money(user=user, currency='SHARD').have()
            if value > check:
                embed = disnake.Embed(description='**Недостаточно средств**', colour= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            soulValue = value//1200
            # Шанс дропа шардов
            chanceDrop = float('{:.3f}'.format(value / (value+300)))
            # Не больше 80%
            if chanceDrop > 0.6: chanceDrop = 0.600

            # Создание диапазона выпадающих шардов
            minDrop = int(soulValue * 0.5)
            if minDrop <= 0: minDrop = 1
            maxDrop = int(round(soulValue * 1.8))
            if maxDrop <= 1: maxDrop = 2
            lossShard = int(value*0.5)
            # Сколько будет потеряно в случае неудачи
            if lossShard <= 10: lossShard = value
            # Рандоминг чисел. Шанса и числа шардов
            randomNum= float('{:.3f}'.format(random()))
            soulValue = randint(minDrop, maxDrop)

            if chanceDrop > randomNum:
                # Позитивный исход
                db.Money(user=user, currency='SHARD', value=value).sub()
                db.Money(user=user, currency='SOUL', value=soulValue).add()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ `[{:.1%}]`\n**Вы получили:**ㅤㅤㅤㅤ`[{soulValue}]` душ'.format(chanceDrop, soulValue= soulValue),
                    color= disnake.Colour.green())
                return await inter.response.edit_message(embed=embed, components=None)
            else:
                # Негативный исход
                db.Money(user=user, currency='SHARD', value=lossShard).sub()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ `[{:.1%}]`\n**Вы потеряли (50%):**ㅤ`[{lossShard}]` осколков'.format(chanceDrop, lossShard= lossShard),
                    color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)

    @commands.command(name='craft', aliases=['cfs', 'крафтдуш', 'создать'])
    async def craft(self, ctx):

        user = ctx.message.author.id
        db.Check(user_id=user, user_name=ctx.message.author.name).user()

        # Проверка на наличия числового значения
        try:
            value = abs(int(ctx.message.content.lower().split(' ')[1]))
        except:
            embed = disnake.Embed(description='**Не корректно указано количество, или вовсе не указано**', color= disnake.Colour.red())
            return await ctx.send(embed=embed)
        
        components = [
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='SH', custom_id=f'essence_soul_cf|{user}|{value}'),
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='SL', custom_id=f'shard_soul_cf|{user}|{value}')
            ]
        embed = disnake.Embed(title='Что желаете скрафтить?', description='\nSH = Осколки\nSL = Души')

        message = await ctx.send(embed=embed, components=components)
        await deleteAfter(message=message, time=120)

    @commands.Cog.listener('on_button_click')
    async def uncraftListener(self, inter: disnake.MessageInteraction):
        check = ['shard_break_uncf', 'soul_break_uncf', 'cristall_break_uncf', 'item_break_uncf']
        for item in check:
            if inter.component.custom_id.startswith(item):break
        else: return
        component = inter.component.custom_id.split('|')[0]
        user = int(inter.component.custom_id.split('|')[1])
        value = int(inter.component.custom_id.split('|')[2])
        if user != inter.author.id:
            await inter.response.send_message('Данное взаимодействие не принадлежит вам.', ephemeral=True)
            return

        def randomBreak() -> bool:
            randNum = randint(1, 100)
            if randNum >= 80: return False
            else: return True

        # Поломка валют
        # Коэффициент 400 к 1
        if component == 'shard_break_uncf':
            # Проверка наличие указаных средств у пользователя
            check = db.Money(user=user, currency='SHARD').have()
            if value > check:
                embed = disnake.Embed(description='**Недостаточно [SH] в кошельке**', color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            dropEssence = 0
            breakCount = 0
            for _ in range(value):
                if randomBreak(): 
                    dropEssence += randrange(10, 300, 10)
                else: breakCount += 1

            db.Money(user=user, currency='SHARD', value=value).sub()
            db.Money(user=user, currency='ESSENCE', value=dropEssence).add()
            embed = disnake.Embed(
                description=f'**Разрушение `{value}` [SH] принесло: `{dropEssence}es`**\n**Пустых осколков: `{breakCount}`**',
                color= disnake.Colour.green())
            embed.set_footer(text='Шанс неудачи стабилен: 20% на ед.')
            return await inter.response.edit_message(embed=embed, components=None)
        
        # Крафт душ
        # Коэффициент 1200 к 1
        elif component == 'soul_break_uncf':
            # Проверка наличие указаных средств у пользователя
            check = db.Money(user=user, currency='SOUL').have()
            if value > check:
                embed = disnake.Embed(description='**Недостаточно [SL] в кошельке**', color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            dropEssence = 0
            breakCount = 0
            for _ in range(value):
                if randomBreak(): 
                    dropEssence += randrange(10, 200, 5)
                    breakCount += 1

            db.Money(user=user, currency='SOUL', value=value).sub()
            db.Money(user=user, currency='SHARD', value=dropEssence).add()
            embed = disnake.Embed(
                description=f'**Разрушение `{value}` [SL] принесло: {dropEssence}sh**\n**Пустых душ: `{breakCount}`**',
                color= disnake.Colour.green())
            embed.set_footer(text='Шанс неудачи стабилен: 20% на ед.')
            return await inter.response.edit_message(embed=embed, components=None)
            
        elif component == 'cristall_break_uncf':
            # Проверка наличие указаных средств у пользователя
            check = db.Money(user=user, currency='CRISTALL_SOUL').have()[4]
            if value > check:
                embed = disnake.Embed(description='**Недостаточно [CSL] в кошельке**', color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            dropEssence = 0
            breakCount = 0
            for _ in range(value):
                if randomBreak(): 
                    dropEssence += randrange(10, 100, 1)
                    breakCount += 1

            db.Money(user=user, currency='CRISTALL_SOUL', value=value).sub()
            db.Money(user=user, currency='SOUL', value=dropEssence).add()
            embed = disnake.Embed(
                description=f'**Разрушение `{value}` [CSL] принесло: `{dropEssence}sl`**\n**Пустых кристальных душ: `{breakCount}`**',
                color= disnake.Colour.green())
            embed.set_footer(text='Шанс неудачи стабилен: 20% на ед.')
            return await inter.response.edit_message(embed=embed, components=None)
        
        elif component == 'item_break_uncf':
           pass

    @commands.command(name='uncraft', aliases=['unc', 'сломать', 'разломать', 'разбор', 'переработать'])
    async def uncraft(self, ctx):
        user = ctx.message.author.id
        db.Check(user_id=user, user_name=ctx.message.author.name).user()

        # Проверка на наличия числового значения
        try:
            value = abs(int(ctx.message.content.lower().split(' ')[1]))
        except:
            embed = disnake.Embed(description='**Не корректно указано количество, или вовсе не указано**', color= disnake.Colour.red())
            return await ctx.send(embed=embed)
        
        components = [
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='SH', custom_id=f'shard_break_uncf|{user}|{value}'),
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='SL', custom_id=f'soul_break_uncf|{user}|{value}'),
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='CSL', custom_id=f'cristall_break_uncf|{user}|{value}')
            ]
        embed = disnake.Embed(title='Что желаете разрушить?', description='\nSH = Осколки\nSL = Души\nCSL = Кристальные души')

        message = await ctx.send(embed=embed, components=components)
        await deleteAfter(message=message, time=120)

    @commands.command(name='sellpoke', aliases=['продать', 'slp'])
    async def sellpoke(self, ctx):

        name = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
        ranksToSell = ['?', 'EX', 'S', 'A', 'B', 'C', 'D', 'E', 'F']
        foundPoke = []

        try:
            if name.upper() in ranksToSell:
                with open(f'../bots/content/lotery/users_bag/{ctx.author.id}.json', 'r', encoding='UTF-8') as file:
                    userBag = json.load(file)

                sortedBag = sorted(userBag, key=lambda k: userBag[k]['rank'][1])
                sortedListRank = {}

                for item in ranksToSell:
                    for item_ in sortedBag:
                        rank = userBag[item_]['rank'][0].split('-')[0]
                        if rank == item and rank not in sortedListRank:
                            sortedListRank[item] = [item_]
                        elif rank == item and rank in sortedListRank:
                            sortedListRank[item].append(item_)
                
                namePoke = sortedListRank[name[0]]
            else:
                namePoke = name.split(', ')

            try: 
                for item in namePoke:
                    backTake, _ = await findPokemonInDatabaseLikeName(name=item)
                    foundPoke.append(backTake)
            except: 
                for item in namePoke:
                    backTake, _ = await findPokemonInDatabaseLikeName(name=item)
                    foundPoke.append(backTake)
        except:
            embed = disnake.Embed(description='Укажите покемона(-ов) или ранг, который вы хотите полностью продать')
            await ctx.send(embed=embed)
            return

        commandToSell, sellCountList = await sellPokemon(pokemon=foundPoke, user=ctx.author.id)

        text = ''
        endSummGain = 0
        for index, item in enumerate(foundPoke):
            
            if commandToSell[index]:
                endSummGain += round(item['price']*0.75)*sellCountList[index]
                if sellCountList[index] > 1: endWords = ['и', 'ы']
                else: endWords = ['', '']
                text += f'✔ **Покемон{endWords[1]} [{foundPoke[index]['name']}] был{endWords[0]} продан{endWords[1]} за `{round(item['price']*0.75)*sellCountList[index]}`es** ({sellCountList[index]} шт)\n'
            else:
                text += f'❌ **Вы не обладаете [{foundPoke[index]['name']}].**\n'
        if endSummGain > 0:
            text += f'\n_Общая выгода продажи: **`{endSummGain}`**es_'
        embed = disnake.Embed(
            description=text
            ).set_footer(text='Покемон продаётся за 75% от стоимости')
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener('on_button_click')
    async def setpokeListener(self, inter: disnake.MessageInteraction):
        check = ['slot_1', 'slot_2', 'slot_3']
        for item in check:
            if inter.component.custom_id.startswith(item):break
        else: return
        slot, rare, user = inter.component.custom_id.split('|')
        if int(user) != inter.author.id: 
            await inter.response.send_message('Вызовите свою команду', ephemeral=True)
            return
        slotID = slot.split('_')[1]
        embed = disnake.Embed(description=f'### Вы установили покемона на работу в {slotID} слот')
        check = await setWorkPokemon(pokemon_id=rare, user=int(user), slot=int(slotID))
        if not check: await inter.response.send_message(ephemeral=True, content='Нельзя ставить одного и того же покемона на разные позиции. Только уникальные покемоны.')
        else: await inter.response.edit_message(embed=embed, components=None)

    @commands.command(name='setpokework', aliases=['датьроботу', 'упрячь', 'поставить', 'spw'])
    async def setpokework(self, ctx):
        try:
            name = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
            try: foundPoke, rare = await findPokemonInDatabaseLikeName(name=name)
            except: 
                foundPoke = await findPokemonInDatebase(ID=name)
                rare = name.split('-')
            workPoke, cashIncome = await getWorkPokemon(user=ctx.author.id, sys=False)

            havePokemon = await findPokemonInUserBag(foundPoke['name'], user=ctx.author.id)
            if not havePokemon:
                await ctx.send(embed=disnake.Embed(description='### У тебя не такого в наличии'))
                return
            
            

            text = ''
            for index, item in enumerate(workPoke):
                income = cashIncome[item]
                if not workPoke[item]:
                    text += f'### `{index+1}`: `Пустой слот`\n'
                    continue
                try: text += f'### `{index+1}`: `{workPoke[item]['name']}` `({workPoke[item]['cashIncome']:,}/h)`\n'
                except: text += f'### `{index+1}`: `{workPoke[item]['name']}` `({income['income']})`\n'
            else:
                text += f'\n\n-# Нажмите на кнопку, для завершения'

            embed = disnake.Embed(
                title='На какое место желаете посадить покемона?',
                description=text,
                colour=disnake.Colour.fuchsia()
                )
            embed.set_footer(text=f'Вызвал: {ctx.author.name}. ')

            pokeID = f'{rare[0]}-{rare[1]}'
            if pokeID.startswith('?'):
                await ctx.send('Покемонов ранга [?] нельзя использовать для работы.')
                return

            buttons = [
                disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id=f'slot_1|{pokeID}|{ctx.author.id}'),
                disnake.ui.Button(style=disnake.ButtonStyle.gray, label='2', custom_id=f'slot_2|{pokeID}|{ctx.author.id}'),
                disnake.ui.Button(style=disnake.ButtonStyle.gray, label='3', custom_id=f'slot_3|{pokeID}|{ctx.author.id}')
                ]
        except:
            embed = disnake.Embed(
                description='Укажите имя или ID покемона, которого желаете отправить работать.'
                )
            buttons = None
        await ctx.send(embed=embed, components=buttons)

    @commands.command(name='lookdivpoke', aliases=['pokediv', 'осмотрпокемонов', 'осмотрработы', 'ld', 'покеработа'])
    async def lookDivPoke(self, ctx):
        
        workPoke, cashIncome = await getWorkPokemon(user=ctx.author.id, sys=False)
        text = ''
        for index, item in enumerate(workPoke):
            if not workPoke[item]:
                text += f'** `{index+1}`: `Пустой слот`**\n| —\n'
                continue
            income = cashIncome[item]
            text += f' **`{index+1}`**: **`{income['name']}`** **`({workPoke[item]['cashIncome']:,}/h)`**\n| Собрано: `({income['income']})`\n| С последнего сбора: `({time.strftime('%H:%M:%S', time.gmtime(round(time.time())-workPoke[item]['time']))})`\n'
        else:
            text += f'-# _Для сбора используйте команду ~work._'

        embed = disnake.Embed(
            description=text,
            colour=disnake.Colour.fuchsia()
            )
        embed.set_footer(text=f'Вызвал: {ctx.author.name}. ')
        await ctx.send(embed=embed)

    @commands.command(name='look', aliases=['l', 'осмотр'])
    async def look(self, ctx):
        try:
            name = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
            try: foundPoke, rare = await findPokemonInDatabaseLikeName(name=name)
            except: 
                await ctx.send('Offнуто')
                return
                # foundPoke = await findPokemonInDatebase(ID=name)
                # rare = name.split('-')

            try: crafteble = 'Да' if foundPoke['crafteble'] else 'Нет'
            except: crafteble = 'Неизвестно'

            try: desc = foundPoke['description']
            except: desc = '-Отсутсвует-'

            try: gif = foundPoke['gif']
            except: gif = None

            embed = disnake.Embed(
                title=f'Покемон [{foundPoke['name']}]',
                description=f'`Описание:`\n{desc}\n\n',
                )
            embed.add_field(name='Цена', value=f'{foundPoke['price']}')
            embed.add_field(name='Доход', value=f'{foundPoke['income']}')
            embed.add_field(name='Редкость', value=f'{rare[0]}-{rare[1]}')
            embed.set_thumbnail(url=gif)
            embed.set_footer(text=f'Возможность крафта: {crafteble}')
        except:
            embed = disnake.Embed(description='### Либо такого предмета - `нет`, либо вы неправильно написали его `название`.')
        await ctx.send(embed=embed)

    
    #? pokemon fight between player
    @commands.Cog.listener('on_button_click')
    async def fightPokeListener(self, inter: disnake.MessageInteraction):
        pass

    @commands.command(name='fightpoke', aliases=['fp', 'сражение', 'бой'])
    async def fightPoke(self, ctx):
        pass


    @commands.command(name='tradepoke', aliases=['trp', 'передать'])
    async def tradepoke(self, ctx):
        pass

    @commands.command(name='bidding', aliases=['bidg', 'аукцион', 'аук', 'торги'])
    async def bidding(self, ctx):
        pass

    @commands.command(name='evolve', aliases=['эвол', 'эволюция', 'ev'])
    async def evolve(self, ctx):
        pass

    @commands.command(name='fusion', aliases=['слияние', 'fp'])
    async def fusionPokemon(self, ctx): # Слияние мелких в большого
        pass

    @commands.command(name='upgradepoke', aliases=['up', 'улучшение'])
    async def upPoke(self, ctx):
        pass

    @commands.command(name='remelting', aliases=['плавка', 'переплавка', 'rm'])
    async def remelting(self, ctx):
        pass

    @commands.command(name='pokedex', aliases=['пхелп', 'покедекс', 'опокемонах', 'ph', 'phelp'])
    async def pokedex(self, ctx):

        embed = disnake.Embed(
            description='''
            ## система на коленки, но команды такие:
            ```В круглых скобках обязательное, в квадратных иная форма команды```
            `~pokedex [пхелп, покедекс, опокемонах, ph, phelp]` — То, что вы сейчас смотрите.

            `~work [работа, раб]` — основное место где зарабатывается валюта для игры.

            `~lotery [лотерея, гача]` — команда для кручения гачи, в которой можно выбить покемончика.

            `~pokemon [poke, петы, покемоны, poke]` — команда для просмотра питомцев, что у вас есть.

            `~setpokework [spw, датьработу, упрячь, поставить] (имя покемона)` — команда для того что бы назначить покемона на работу, в одну из 3-х ячеек. Можно ставить только не повторяющихся покемонов.

            `~lookdivpoke [pokediv, осмотрпокемонов, осмотрработы, ld, покеработа]` — Вы можете посмотреть сколько покемоны собрали эссенций, а так же какие покемоны где стоят в слотах.

            `~look [l, осмотр] (имя покемона)` — команда для осмотра самого покемона.

            `~sellpoke [slp, продать]` — Возможность продать покемона, получив 75% от стоимости.

            `~craft [cfs, крафтдуш, создать]` — Преобразование валюты вверх. [Эссенции → Осколки → Души]

            `~uncraft [unc, сломать, разломать, разбор, переработать]` — Преобразование валюты вниз. [Кристальные души → Души → Осколки → Эссенции]
            '''
            )
        await ctx.send(embed=embed)

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Economics(bot))