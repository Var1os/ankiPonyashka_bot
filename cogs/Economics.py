import disnake
from disnake.ext import commands
from .module import REQ_database as Rdb

import json
import yaml
import pickle

import time
import random

# Импортирование для исправления бага связанного с пиклом
from .module.PokemonModule import addTiket, addSoul, addPokeEssence

from .module.PokemonModule import *
from .module.SystemCommandRPG import *
from .module.SystemViews import *

db = Rdb.DataBase

class Economics(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.command(name='bag', aliases=['мешок', 'хабар'])
    async def bag(self, ctx):

        user = ctx.message.author.id
        stat = await userData(uid=user)
        poke = db.Poke(user=ctx.author.id).takeAll()
        
        money = stat['money']
        text = f'## Шэкэли, что ты насобирал \n```Эссенции: {money['ESSENCE']:,}\nОсколки: {money['SHARD']:,}\nДуши: {money['SOUL']:,}``````Кристальные души: {money['CRISTALL_SOUL']:,}``````Монеты «Коширского»: {money['COU']:,}\nМонеты «Сущности»: {money['ACOIN']:,}\nМонеты «Пустоты»: {money['VCOIN']:,}\nМонеты «Истины»: {money['TCOIN']:,}``` ```Билеты: {poke[4]}\nЭссенции монстра: {poke[5]}```'

        embed = disnake.Embed(
            description=text
            ).set_thumbnail(url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed)

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
            dropstrike = (strikeup//24) > 5

            text = ''
            pokemonIncome = 0
            for item in cashIncome:
                if cashIncome[item] is None:
                    continue
                if cashIncome[item]['pastTense'] > 0:
                    pokemonIncome += int(cashIncome[item]['income'])
                    text += f'[{cashIncome[item]['name']}] принес(-ла): **`{cashIncome[item]['income']}`**\n'

            cashUser = round(random.randint(15, 120) * strikeMulti)
            cash = pokemonIncome + cashUser
            embed = disnake.Embed(description=f'### Вы заработали: `{cashUser}es`\n\n{text}\nОбщая прибыль: `+{cash}es`\n`Приходите позже!`', colour=disnake.Colour.dark_green())
            embed.set_footer(text=f'Вызвал: {ctx.author.name}.   Текущий стрик: {info[1]+1} = {strikeMulti}x')
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
        if inter.component.custom_id not in ['lotery_1', 'lotery_5', 'lotery_10', 'lotery_50']:
            return

        def weightRank(rank):
            order = {"?":-1,"EX":0, "S":1, "A":2, "B":3, "C":4, "D":5, "E":6, "F":7}
            return order[rank]
        async def bestRoll(count, best:bool):
            priceTiket = await GetTiketPrice(inter.author.id)
            data = await RollLotery(user=inter.author.id, count=count, priceTiket=priceTiket)

            text = ''
            SortedData = sorted(data['loot'], key=lambda x: weightRank(x[1]['rank']))
            DeleteDuplicate = {
                'add':{},
                'sell':{}
                }

            for item in SortedData:
                if item[3]:
                    if item[0] in DeleteDuplicate['sell']:
                        DeleteDuplicate['sell'][item[0]]['count'] += 1
                    else:
                        DeleteDuplicate['sell'][item[0]] = {
                            'poke':item[1],
                            'count':1
                            }
                else:
                    if item[0] in DeleteDuplicate['add']:
                        DeleteDuplicate['add'][item[0]]['count'] += 1
                    else:
                        DeleteDuplicate['add'][item[0]] = {
                            'poke':item[1],
                            'count':1
                            }

            text += f'```Добавлено в инвертарь```'

            for index, item in enumerate(DeleteDuplicate['add']):

                if index+1 == len(DeleteDuplicate['add']):
                    text += f'`({DeleteDuplicate['add'][item]['poke']['rank']}:{DeleteDuplicate['add'][item]['count']}x)|{DeleteDuplicate['add'][item]['poke']['name']}`\n'
                    continue

                text += f'`({DeleteDuplicate['add'][item]['poke']['rank']}:{DeleteDuplicate['add'][item]['count']}x) {DeleteDuplicate['add'][item]['poke']['name']}`, '
                
            if len(DeleteDuplicate['sell']) != 0:
                text += f'```Продано из-за ограничение: ```'

            for index, item in enumerate(DeleteDuplicate['sell']):

                if index+1 == len(DeleteDuplicate['sell']):
                    text += f'`({DeleteDuplicate['sell'][item]['poke']['rank']}:{DeleteDuplicate['sell'][item]['count']}x)|{DeleteDuplicate['sell'][item]['poke']['name']}`'
                    continue

                text += f'`({DeleteDuplicate['sell'][item]['poke']['rank']}:{DeleteDuplicate['sell'][item]['count']}x) {DeleteDuplicate['sell'][item]['poke']['name']}`, '
                
            else:
                if len(DeleteDuplicate['sell']) != 0:
                    text += f'\n\n**Возвращено по ставке 75%:** `+{data['sellIncome']}(es)`'

            embed = disnake.Embed(
                description=f"# ```Ты выиграл в лотереи...```\n{text}\n`{data['compliment']}`\n",
                colour=disnake.Colour.dark_gold()           
                )
            embed.set_footer(text=f'Вызвал: <{inter.author.name}> | Цена за тикет = <{priceTiket}>')

            await inter.response.edit_message(embed=embed, components=data['buttons'])

        if inter.component.custom_id == 'lotery_1':
            priceTiket = await GetTiketPrice(inter.author.id)
            data = await RollLotery(user=inter.author.id, priceTiket=priceTiket)
            loots = data['loot'][0]

            text = f"# ```Ты выиграл в лотереи...```\n## → {loots[1]['name']} `({loots[0]})`\n"
            if loots[3]: text += f'>20, Продан по ставке 75%: +`{data['sellIncome']}(es)`'
            text += f'`\n{data['compliment']}`'
            embed = disnake.Embed(
                description=text,
                colour=loots[2]           
                )
            embed.set_footer(text=f'Вызвал: <{inter.author.name}> | Цена за тикет = <{priceTiket}>')

            await inter.response.edit_message(embed=embed, components=data['buttons'])
        elif inter.component.custom_id == 'lotery_5':
            await bestRoll(count=5, best=False)
        elif inter.component.custom_id == 'lotery_10':
            await bestRoll(count=10, best=False)
        elif inter.component.custom_id == 'lotery_50':
            await bestRoll(count=50, best=True)
        
    @commands.command(name='lotery', aliases=['лотерея', 'гача'])
    async def lotery(self, ctx):
        
        user = await userData(ctx.author.id)
        essence = user['money']['ESSENCE']
        priceTiket = await GetTiketPrice(ctx.author.id)
        if priceTiket*5 > essence >= priceTiket:
            data = await RollLotery(user=ctx.author.id, priceTiket=priceTiket)
            loots = data['loot'][0]

            embed = disnake.Embed(
                description=f"# ```Ты выиграл в лотереи...```\n# {loots[1]['name']} `(Rank: {loots[0]})`\n## `{data['compliment']}`\n",
                colour=loots[2]         
                )
            embed.set_footer(text=f'Крутил барабан: <{ctx.author.name}> | Цена за тикет = <{priceTiket}>')

            savePokemon(loot=data['loot'], uid=ctx.author.id)

            await ctx.send(embed=embed, components=data['buttons'])
        elif essence > priceTiket*5:
            user = await userData(ctx.author.id)
            essence = user['money']['ESSENCE']
            buttons = await checkButtonsLotery(essence=essence, priceTiket=priceTiket)

            embed = disnake.Embed(
                description=f"### Сколько желаете открыть?\nПри себе у вас ({await userHaveTicket(user=ctx.author.id)}) билетов, они используются первыми, а далее деньги.\n\n**1 билет:** `{priceTiket:,}`\n**5 билетов:** `{priceTiket*5:,}`\n**10 билетов:** `{priceTiket*10:,}`\n**50 билетов:** `{priceTiket*50:,}`",
                colour=disnake.Colour.dark_orange()
                )
            embed.set_footer(text=f'Вызвал: {ctx.author.name}')

            await ctx.send(embed=embed, components=buttons)
        else:
            embed = disnake.Embed(
                description=f'```Похоже у вас не хватает средств\nСтоимость 1 крутки для вас равна {priceTiket} шекелям.```',
                colour=disnake.Colour.dark_red()
                )
            embed.set_footer(text=f'Вызвал: <{ctx.author.name}?')
            await ctx.send(embed=embed)

    @commands.command(name='pokemon', aliases=['петы', 'покемоны', 'poke'])
    async def pokemon(self, ctx):


        try:
            with open(f'../PonyashkaDiscord/content/lotery/users_bag/{ctx.author.id}.json', 'r', encoding='UTF-8') as file:
                userBag = json.load(file)

            with open(f'../PonyashkaDiscord/content/lotery/lowLotery.json', 'r', encoding='utf-8') as file:
                load = json.load(file)
                loteryItem = load['items']
        except:
            embed = disnake.Embed(description='```Похоже вы не обладаете ни одним покемонов. Возможно вы даже ещё не играли в гачу-рулетку. Попробуйте.```')
            await ctx.send(embed=embed)
            return

        text = ''
        order = ["?", "EX", "S", "A", "B", "C", "D", "E", "F"]
        mapingPokemons = {}

        # text += f'`({countPet}) {randomPet['name']}` '
        # text += f'```{itemORD} - rank ```'

        for itemORD in order:
            for item in userBag:
                try: randomPet = userBag[item][choice(list(userBag[item].keys()))]
                except: continue
                countPet = len(userBag[item])

                if randomPet['rank'] != itemORD: continue

                if randomPet['rank'] in mapingPokemons:
                    card = {"name":randomPet['name'], "count":countPet}
                    mapingPokemons[randomPet['rank']].append(card)
                else:
                    mapingPokemons[randomPet['rank']] = [{"name":randomPet['name'], "count":countPet}]
                
        for rank in order:
            if rank not in mapingPokemons: continue

            text += f'```{rank} - rank ```'
            for poke in mapingPokemons[rank]:
                text += f'`({poke['count']}) {poke['name']}` '


        if text == '': text = '**У вас тут пусто. Даже перекати поля нет.**'
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
            chanceDrop = float('{:.3f}'.format(value / (value+200)))
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
            randomNum= float('{:.3f}'.format(random.random()))
            ShardDrop = random.randint(minDrop, maxDrop)

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
            randomNum= float('{:.3f}'.format(random.random()))
            soulValue = random.randint(minDrop, maxDrop)

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
        embed.set_footer(text=f'Вызвал: {ctx.author.name}')

        message = await ctx.send(embed=embed, components=components)

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
            randNum = random.randint(1, 100)
            if randNum >= 70: return False
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
                    dropEssence += random.randrange(10, 200, 10)
                else: breakCount += 1

            db.Money(user=user, currency='SHARD', value=value).sub()
            db.Money(user=user, currency='ESSENCE', value=dropEssence).add()
            embed = disnake.Embed(
                description=f'**Разрушение `{value}` [SH] принесло: `{dropEssence}es`**\n**Пустых осколков: `{breakCount}`**',
                color= disnake.Colour.green())
            embed.set_footer(text='Шанс неудачи стабилен: 30% на ед.')
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
                    dropEssence += random.randrange(10, 100, 5)
                    breakCount += 1

            db.Money(user=user, currency='SOUL', value=value).sub()
            db.Money(user=user, currency='SHARD', value=dropEssence).add()
            embed = disnake.Embed(
                description=f'**Разрушение `{value}` [SL] принесло: {dropEssence}sh**\n**Пустых душ: `{breakCount}`**',
                color= disnake.Colour.green())
            embed.set_footer(text='Шанс неудачи стабилен: 30% на ед.')
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
                    dropEssence += random.randrange(10, 50, 1)
                    breakCount += 1

            db.Money(user=user, currency='CRISTALL_SOUL', value=value).sub()
            db.Money(user=user, currency='SOUL', value=dropEssence).add()
            embed = disnake.Embed(
                description=f'**Разрушение `{value}` [CSL] принесло: `{dropEssence}sl`**\n**Пустых кристальных душ: `{breakCount}`**',
                color= disnake.Colour.green())
            embed.set_footer(text='Шанс неудачи стабилен: 30% на ед.')
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


    @commands.command(name='sellpoke', aliases=['продать', 'slp'])
    async def sellpoke(self, ctx):
        # Одиночная продажа имеет флаги: all, по стандарту one
        # Без подтверждения действия о продажи всех покемонов

        # Продажа по рангам, переделать, да и просто починить, дабы можно было продать несколько рангов
        # Выскакивает подтверждение на действие с описанием, что будут проданы все покемоны, а те, что работают из этого ранга, будут сняты

        name = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
        ranksToSell = ['?', 'EX', 'S', 'A', 'B', 'C', 'D', 'E', 'F']
        pokemonsList = name.split(', ')

        userBag = await giveUserBag(user=ctx.author.id)

        # Функция для удаления работающего покемона из списка работающих
        # Первая грубая, смотрящая только на название покемона, вторая деликатная, смотрящая ещё и на зарабаоток
        def injectWorkFile(user, pokemon):
            with open(f'../PonyashkaDiscord/content/lotery/user_pet_in_work/{user}.json', 'r', encoding='UTF-8') as file:
                userWorkPoke = json.load(file)
            for item in userWorkPoke:
                try:
                    if userWorkPoke[item]['name'] == pokemon['name']:
                        userWorkPoke[item] = None
                except: pass

        errorsInput = []
        endSelled = []
        # endSelled = (commandToSell, sellValueList, pokeHowSell)

        async def mainSellFunc(mass:bool, pokemonName):
            if type(pokemonName) == list:
                pokemon = pokemonName[0]
            else: pokemon = pokemonName

            if '-all' in pokemon or mass: flag = 'all'
            else: flag = 'one'
            pokemon = pokemon.split(' -')[0]

            rankSell = True
            if pokemon.upper() in ranksToSell: 
                rankSell = False

            else:
                pokemonID = await findID_PokemonInDB_LikeName(PokemonName=pokemon)
                if pokemonID is None:
                    if not mass:
                        errorsInput.append(pokemon)
                        return False
                    else:
                        errorsInput.append(pokemon)
                        return False

            
            if rankSell:
                # Когда указывается название покемона
                if flag == 'all':
                    # Флаг на продажу всех типов этого покемона
                    # Поиск реальности существования данного покемона
                    pokemonID = await findID_PokemonInDB_LikeName(PokemonName=pokemon)
                    
                    try: 
                        # Получение пользовательского инветаря
                        userBagPoke = userBag[pokemonID]
                        # Количество тамошних покемонов и временная переменная для продажи
                        count = len(userBagPoke)
                        timesSelled = 0
                        associate = []
                        for item in userBagPoke:
                            associate.append(item)
                        # Прочесывание стоимости
                        for item in userBagPoke:
                            timesSelled += userBagPoke[item]['curr']['price'] * 0.75
                            injectWorkFile(user=ctx.author.id, pokemon=userBagPoke[item])
                        else:
                            pokeHowSell = userBagPoke[random.choice(associate)]['name']
                        
                        commandToSell = True
                        sellValueList = (timesSelled, count)

                        del userBag[pokemonID]
                        endSelled.append((commandToSell, sellValueList, pokeHowSell, (False, None), (False, None)))
                    except:
                        pokesWhatWannaSell = await findMap_PokemonInDB_LikeID(ID=pokemonID)
                        endSelled.append((False, (0, 0), pokesWhatWannaSell['name'], (False, None), (False, None)))
                    await saveBagUserFile(userBag, ctx.author.id)
                if flag == 'one':
                    # Флаг на продажу одного покемона из этого типа.
                    # 1. Через view пользователь выбирает покемона.
                    # 2. Через флаг слеш указывается ids. <name>/<count>
                    # Поиск реальности существования данного покемона
                    # input -> rank
                    pokemonID = await findID_PokemonInDB_LikeName(PokemonName=pokemon)
                    rank = (await findMap_PokemonInDB_LikeID(ID=pokemonID))['rank']

                    options = []
                    userBagPoke = userBag[pokemonID]

                    for index, item in enumerate(userBagPoke):
                        options.append(
                            disnake.SelectOption(
                                label=f'({index+1}) {userBagPoke[item]['name']} ({userBagPoke[item]['curr']['price']} es)',
                                value=f'poke|{index+1}|{pokemonID}-{item}|{userBagPoke[item]['curr']['price']}'
                                )
                            )
                    else:
                        options.append(
                            disnake.SelectOption(
                                label=f'Отменить продажу',
                                value=f'cannelSell|null|null|999999999999999999'
                                )
                            )
                    options.sort(key=lambda x: int(x.value.split('|')[3]), reverse=True)
                    
                    view = SelectMassPokemonsViewCorrectSell(options=options, user=ctx.author.id)
                    embed = disnake.Embed(description='**Выберите из списка ваших покемонов, того что желаете продать.**').set_footer(text='Для продажи всех, одного типа, используйте флаг [-all]')
                    await ctx.send(embed=embed, view=view)
                    return True
                return False
            else:
                # Когда указывается ранг который надо продать
                pokemonRank = pokemon.upper()
                
                userBagPokes = []
                ids = []
                for item in userBag:
                    if userBag[item][choice(list(userBag[item].keys()))]['rank'] == pokemonRank: 
                        userBagPokes.append(userBag[item])
                        ids.append(item)


                if not userBagPokes:
                    endSelled.append((False, 0, None, (True, pokemon), (False, None)))
                    return False

                commandToSell = True

                timesSelled = 0
                for item in userBagPokes:
                    for pokes in item:
                        pricePokes = item[pokes]['curr']['price']

                        injectWorkFile(user=ctx.author.id, pokemon=item[pokes])
                        try:
                            timesSelled += round(pricePokes * 0.75)
                        except:
                            print(pricePokes, item[pokes]['name'])

                else:
                    sellValueList = (timesSelled, len(userBagPokes)-1)
                    commandToSell = True
                    endSelled.append((commandToSell, sellValueList, None, (False, None), (True,pokemon)))
                    for item in ids:
                        del userBag[item]
                    await saveBagUserFile(userBag, ctx.author.id)
        # В целом, скорей всего есть более элегантное решение, но мне так похуй. Лень искать, да и время жмёт.
        # Удачи будущему мне эту хуйню пытаться улучшать, для чего-то кардинально нового
        if len(pokemonsList) == 1:
            viewStart = await mainSellFunc(mass=False, pokemonName=name)
            if viewStart: return

        else:
            # Когда через запятую перечисляют ранги или покемонов
            # Проверок на продажу нет, кроме вопроса о подтверждении действия
            # Попытаться реализовать, что с рангом можно указать и название, а это будет работать
            # Мысль: Через реализацию функций из блока if == 1   
            for item in pokemonsList:
                await mainSellFunc(mass=True, pokemonName=item)

        # endSelled = (commandToSell, sellValueList, pokeHowSell, rankSelledUser, UnknowEnter, rankedSelect)
        text = ''
        endSummGain = 0
        count = 0

        for nums in endSelled:
            if nums[0]:
                endSummGain += nums[1][0]
                count += nums[1][1]
        if endSummGain != 0:
            db.Money(user=ctx.author.id, value=round(endSummGain)).add()

        for index, item in enumerate(endSelled):
            
            if item[0] and not item[4][0]:

                if item[1][1] > 1: endWords = ['и', 'ы']
                else: endWords = ['', '']

                text += f'✔ **Покемон{endWords[1]} [{item[2]}] был{endWords[0]} продан{endWords[1]} за `{round(item[1][0]):,}`es** ({item[1][1]} шт)\n'

            elif item[0] and item[4][0]:
                text += f'✔ **Покемоны ранга [{item[4][1].upper()}] проданы за `{round(item[1][0]):,}`es** ({item[1][1]} вид(-ов))\n'

            elif not item[0] and item[3][0]:
                text += f'❌ **У вас нет покемонов из ранга [{item[3][1]}].**\n'

            else:
                text += f'❌ **Вы не обладаете [{item[2]}].**\n' 

        else:
            if len(errorsInput) != 0: text += '\n'
            for item in errorsInput:
                text += f'❓ **Ошибочный или неверный ввод:** [{item}]\n'
        if endSummGain > 0:
            text += f'\n💰 _Общая выгода продажи: **`{endSummGain:.0f}`**es_'

        embed = disnake.Embed(
            description=text
            ).set_footer(text='Покемоны продаются за 75% от стоимости')
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener('on_button_click')
    async def setpokeListener(self, inter: disnake.MessageInteraction):
        check = ['selectWorkSlot-1', 'selectWorkSlot-2', 'selectWorkSlot-3']
        for item in check:
            if inter.component.custom_id.startswith(item):break
        else: return
        
        slot, rareCOM, user = inter.component.custom_id.split('|')

        if int(user) != inter.author.id: 
            await inter.response.send_message('Вызовите свою команду', ephemeral=True)
            return  
        
        slotID = slot.split('-')[1]
        embed = disnake.Embed(description=f'### Вы установили покемона на работу в {slotID} слот')
        check = await setWorkPokemon(rankCOM=rareCOM, user=int(user), slot=int(slotID))

        if not check: await inter.response.send_message(ephemeral=True, content='Только уникальные виды покемонов.\nЛибо вы можете переназначить уже работающего, на более продуктивного.')
        else: await inter.response.edit_message(embed=embed, components=None)

    @commands.command(name='setpokework', aliases=['датьроботу', 'упрячь', 'поставить', 'spw'])
    async def setpokework(self, ctx):
        # Проверка значения
        try: 
            # Введенные данные от пользователя
            enterMessage = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
            # попытка поиска, через введенное имя покемона
            foundPoke, ids = await findMap_PokemonInDB_LikeName(name=enterMessage)
            # Получение данных о боевой группе пользователя
            fightPoke = await takeFightGroup(ctx.author.id)
        except:
            print(enterMessage)
            # Исключение извещающее о отсутствии покемона или ошибке 
            embed = disnake.Embed(description='**Не указано имя покемона или его ID**') 
            await ctx.send(embed=embed)
            return
        
        # Наличие покемна у человека
        userBag = await giveUserBag(user=ctx.author.id)
        try:
            poke = userBag[ids]
        except:
            embed = disnake.Embed(description='**Вы не обладаете данным покемоном**') 
            await ctx.send(embed=embed)
            return
        
        # Получение рабочего стака покемонов у человека
        workPoke, cashIncome = await getWorkPokemon(user=ctx.author.id, sys=False)

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

        if foundPoke['rank'] == '?':
            embed = disnake.Embed(description='Покемонов ранга [?] нельзя использовать для работы.')
            await ctx.send(embed=embed)
            return
        
        # buttons = [
        #     disnake.ui.Button(style=disnake.ButtonStyle.gray, label='1', custom_id=f'slot_1|{pokeID}|{ctx.author.id}'),
        #     disnake.ui.Button(style=disnake.ButtonStyle.gray, label='2', custom_id=f'slot_2|{pokeID}|{ctx.author.id}'),
        #     disnake.ui.Button(style=disnake.ButtonStyle.gray, label='3', custom_id=f'slot_3|{pokeID}|{ctx.author.id}')
        #     ]

        text = 'Учтите, что пока покемон работает, его нельзя отправить сражаться.'
        embed = disnake.Embed(
            title='Кого вы бы хотели отправить работать?',
            description=text
            )

        options = []
        for index, item in enumerate(poke):
            options.append(
                disnake.SelectOption(
                    label=f'({index+1}) {poke[item]['name']} ({poke[item]['curr']['income']}/h)',
                    value=f'poke|{index+1}|{poke[item]['curr']['income']}|{ids}-{item}'
                    )
                )
        options.sort(key=lambda x: int(x.value.split('|')[2]), reverse=True)
        view = SelectMassPokemonsViewWorkGroup(options=options, user=ctx.author.id)

        await ctx.send(embed=embed, view=view)

    @commands.command(name='lookdivpoke', aliases=['pokediv', 'осмотрпокемонов', 'осмотрработы', 'ld', 'покеработа'])
    async def lookDivPoke(self, ctx):
        
        workPoke, cashIncome = await getWorkPokemon(user=ctx.author.id, sys=False)
        text = ''
        for index, item in enumerate(workPoke):
            if not workPoke[item]:
                text += f'### ** `{index+1}`: `Пустой слот`**\n| —\n'
                continue
            income = cashIncome[item]
            text += f'### **`{index+1}`**: **`{income['name']}`** **`({workPoke[item]['cashIncome']:,}/h)`**\n| Собрано: `({income['income']})`\n| С последнего сбора: `({time.strftime('%H:%M:%S', time.gmtime(round(time.time())-workPoke[item]['time']))})`\n'
        else:
            text += f'-# _Для сбора используйте команду !work._'

        embed = disnake.Embed(
            description=text,
            colour=disnake.Colour.fuchsia()
            )
        embed.set_footer(text=f'Вызвал: {ctx.author.name}. ')
        await ctx.send(embed=embed)

    @commands.command(name='look', aliases=['l', 'осмотр'])
    async def look(self, ctx):
        # TODO: Сделать дополнительную возможность на просмотр навыков, характеристик и эффектов
        try:
            name = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
            try: 
                foundPoke, rare = await findMap_PokemonInDB_LikeName(name=name)

            except: 
                embed = disnake.Embed(description='')
                await ctx.send('`Ты где-то ошибся в названиия`')
                return

            try: crafteble = 'Да' if foundPoke['crafteble'] else 'Нет'
            except: crafteble = 'Неизвестно'

            try: desc = random.choice(foundPoke['description'])
            except: desc = '-Отсутсвует-'

            try: gif = foundPoke['gif']
            except: gif = None

            def sizeStat(stat):
                return (foundPoke['params'][stat][0]+foundPoke['params'][stat][1])/2

            priceText = f'**`Ценообразование:`**\n- Цена от _`{foundPoke['price'][0]:,}(es)`_ до _`{foundPoke['price'][1]:,}(es)`_\n- Доход от _`{foundPoke['income'][0]:,}(es/h)`_ до _`{foundPoke['income'][1]:,}(es/h)`_'
            pokeStats = f'**`Характиристики (среднее):`**\n- Здоровье: {sizeStat('healpoint'):.0f} ({sizeStat('regen'):.0f}/15m)\n- Атака: {sizeStat('attack'):.0f}\n- Броня: {sizeStat('armor'):.0%}\n- Уклонение: ({sizeStat('evasion'):.0%})\n- Скорость: {1/foundPoke['params']['speed'][1]:.1f}x-{1/foundPoke['params']['speed'][0]:.1f}x'

            embed = disnake.Embed(
                title=f'[{foundPoke['name']}]|[ID:{rare}]|[Rare:{foundPoke['rank']}]',
                description=f'**`Описание:`**\n{desc}\n\n{priceText}\n\n{pokeStats}',
                )
            embed.set_thumbnail(url=gif)
            embed.set_footer(text=f'Возможность крафта: {crafteble}')
            
        except:
            embed = disnake.Embed(description='### Либо такого предмета - `нет`, либо вы неправильно написали его `название`.')
        await ctx.send(embed=embed)




    #? pokemon fight-2 between player
    @commands.Cog.listener('on_button_click')
    async def fightPokeListener2(self, inter: disnake.MessageInteraction):
        pass
    
    #? pokemon fight between player
    @commands.Cog.listener('on_button_click')
    async def fightPokeAcceptSystem(self, inter: disnake.MessageInteraction):
        acc = ['fip1', 'fip2']
        for item in acc:
            if inter.component.custom_id.startswith(item): break
        else:
            return

    @commands.command(name='fightpoke', aliases=['fip', 'сражение', 'боп'])
    async def fightPoke(self, ctx: disnake.ext.commands.Context):
        try:
            opponentID = ctx.message.mentions[0].id
            opponent = ctx.message.mentions[0]
        except:
            embed = disnake.Embed(description='Не выбран соперник, упомяните его после команды.')
            await ctx.send(embed=embed)
            return

        try:
            with open(f"../PonyashkaDiscord/content/lotery/fightPet/{ctx.author.id}.json", 'r', encoding='utf-8') as file:
                loadPokeUser = json.load(file)
        except:
            await ctx.send('прикол с боевыми конями')
            return

        #! Потом удалить
        userBag = await giveUserBag(user=ctx.author.id)

        randomPoke = []

        for index in range(3):
            associate = []
            associateOrde = []
            associateNums = []

            for item in userBag:
                associate.append(item)
            else: 
                rank = random.choice(associate)

            for item in userBag[rank]:
                associateOrde.append(item)
            else: 
                associateOrde.pop(0)
                orde = random.choice(associateOrde)

            for item in userBag[rank][orde]:
                associateNums.append(item)
            else: 
                nums = random.choice(associateNums)

            randomPoke.append(f'{rank}-{orde}-{nums}')
            
        fightMap = {
            "Player1":{
                "IDP":int(ctx.author.id),
                "Ready":False,

                "pokemons":{
                    'slot1':loadPokeUser['slot1'],
                    'slot2':loadPokeUser['slot2'],
                    'slot3':loadPokeUser['slot3']
                    }
                },
            "Player2":{
                "IDP":int(opponent.id),
                "Ready":False,

                "pokemons":{
                    'slot1':randomPoke[0],
                    'slot2':randomPoke[1],
                    'slot3':randomPoke[2]
                    }
                }            
            }

        # PreStart call to accept fight
        embed = disnake.Embed(description=f'## Готовы ли игроки к бою?\nPlayer 1 ({ctx.author.name[0].upper()}) — `{ctx.author.name}`\nPlayer 2 ({opponent.name[0].upper()}) — `{opponent.name}`')
        # F1 - Who command call
        # F2 - Whos called
        buttonsPlayer = [
            disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f'({ctx.author.name[0].upper()})-yes', custom_id=f'fip1|{ctx.author.id}'),

            disnake.ui.Button(style=disnake.ButtonStyle.red, label=f'({opponent.name[0].upper()})-yes', custom_id=f'fip2|{opponent.id}')
            ]
        
        with open(f'../PonyashkaDiscord/content/lotery/fight/{ctx.author.id}-{opponent.id}.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(fightMap, indent=3, ensure_ascii=False))
        await ctx.send(embed=embed, components=buttonsPlayer)




    @commands.Cog.listener('on_button_click')
    async def setFightGroupLictener(self, inter: disnake.MessageInteraction):
        trustList = ['selectFightSlot-1', 'selectFightSlot-2', 'selectFightSlot-3']
        for item in trustList:
            if inter.component.custom_id.startswith(item): break
        else: return

        comm, rankCOM, user = inter.component.custom_id.split('|')
        _, slot = comm.split('-')
        ids, seq = rankCOM.split('-')
        userBag = (await giveUserBag(int(user)))[ids][seq]

        if int(user) != inter.author.id: 
            await inter.response.defer()
            return
        
        await saveFightGroup(user=user, rankCOM=rankCOM, slot=slot)
        embed = disnake.Embed(description=f'**[{userBag['name']}] был установлен в {slot} слот**')

        await inter.response.edit_message(embed=embed, components=None)

    @commands.command(name='setFightGroup', aliases=['sfg', 'угу', 'установкабоеваягруппа'])
    async def setFightGroup(self, ctx):
        
        # Проверка значения
        try: 
            # Введенные данные от пользователя
            enterMessage = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')

            try: 
                # первая попытка поиска, через введенное имя покемона
                foundPoke, rare = await findMap_PokemonInDB_LikeName(name=enterMessage)

            except: 
                # Вторая попытка нахождения покемона через индитификатор покемона Rank-num
                foundPoke = await findMap_PokemonInDB_LikeID(ID=enterMessage)
                rare = enterMessage.split('-')

            # Получение данных о боевой группе пользователя
            fightPoke = await takeFightGroup(ctx.author.id)
        except:
            # Исключение извещающее о отсутствии покемона или ошибке 
            embed = disnake.Embed(description='**Не указано имя покемона или его ID**') 
            await ctx.send(embed=embed)
            return

        # TODO: Реализовать пересмотр поиска покемона, так как при повышении у него ранга изменяется его положение в инвентаре.
        # Однако оставить поиск по ID и имени, так как потребуется проверять реальность наличия такового покемона в базе данных, хотя можно откинуть это в отдельную функцию.

        # Наличие покемона у человека
        userBag = await giveUserBag(user=ctx.author.id)
        try:
            poke = userBag[rare]
        except:
            embed = disnake.Embed(description='**Вы не обладаете данным покемоном**') 
            await ctx.send(embed=embed)
            return
        
        text = '**Выберите покемона из списка, которого бы вы хотели установить в боевую группу**'
        embed = disnake.Embed(description=text)

        options = []
        for index, item in enumerate(poke):
            options.append(
                disnake.SelectOption(
                    label=f'({index+1}) {poke[item]['name']} ({poke[item]['params']['healpoint']}hp) ({poke[item]['params']['attack']}atk)',
                    value=f'poke|{index}|{poke[item]['params']['healpoint']}-{poke[item]['params']['attack']}|{rare}-{item}'
                    )
                )
        options.sort(key=lambda x: round((int(x.value.split('|')[2].split('-')[0]) + int(x.value.split('|')[2].split('-')[1]))/2), reverse=True)
        view = SelectMassPokemonsViewfightGroup(options=options, user=ctx.author.id)

        await ctx.send(embed=embed, view=view)

    @commands.command(name='lookFightGroup', aliases=['lfg', 'бгу', 'боеваягруппа'])
    async def lookFightGroup(self, ctx):
        slots = await takeFightGroup(user=ctx.author.id)
        text = ''
        for index, item in enumerate(slots):
            if slots[item] is None:
                text += f'### **`{index+1}:` `Пустой слот.`**\n| <None>\n'
            else:
                ids, seq = slots[item].split('-')
                localUserBag = (await giveUserBag(ctx.author.id))[ids][seq]
                localParams = localUserBag['params']
                text += f'### **`{index+1}:` `{localUserBag['name']}` `({localUserBag['other_param']['lvl']}) lvl`**\n| Здоровье: `[{localParams['healpoint']:,}]` `[{localParams['regen']}/15m]`\n| Атака: `[{localParams['attack']:,}]`\n| Процент защиты: `[{localParams['armor']:.0%}]`\n| Шанс уклонения: `[{localParams['evasion']:.0%}]`\n| Скорость: `[{(1/localParams['speed']):.0%}]`\n'

        embed = disnake.Embed(description=text, colour=disnake.Colour.dark_red())
        await ctx.send(embed=embed)



    @commands.Cog.listener('on_button_click')
    async def tradePokeListener(self, inter: disnake.MessageInteraction):
        pass

    @commands.command(name='tradepoke', aliases=['trp', 'передать'])
    async def tradepoke(self, ctx):
        
        try:
            # Получение упоминания пользователя которому добавляется покемон
            mentionedUser = ctx.message.mentions[0]
        except:
            ErrorEmbed = disnake.Embed(description='**Форма команды: !trp <пользователь> <покемон>**')
            await ctx.send(embed=ErrorEmbed)
            return

        try:
            # Получение названия или ID покемона
            sennedPokemon = ctx.message.content.split()[2]
        except:
            ErrorEmbed = disnake.Embed(description='**Форма команды: !trp <пользователь> <покемон>**')
            await ctx.send(embed=ErrorEmbed)
            return
        
        try:
            try: 
                    # первая попытка поиска, через введенное имя покемона
                    foundPoke, rare = await findMap_PokemonInDB_LikeName(name=sennedPokemon)
            except: 
                # Вторая попытка нахождения покемона через индитификатор покемона Rank-num
                foundPoke = await findMap_PokemonInDB_LikeID(ID=sennedPokemon)
                rare = sennedPokemon.split('-')
        except:
            ErrorEmbed = disnake.Embed(description='**Возможно вы неверно указали либо ID покемона, либо название.**')
            await ctx.send(embed=ErrorEmbed)
            return

        try:
            userPokemons = await giveUserBag(user=ctx.author.id)
            SelectedPokes = userPokemons[rare]
        except:
            userPokemons = await giveUserBag(user=ctx.author.id)
            SelectedPokes = userPokemons[rare]
            print(rare)
            return

        # Формат [trade|rankCOM|user-ment]
        options = []
        for index, item in enumerate(SelectedPokes):
            options.append(
                disnake.SelectOption(
                    label=f'({index+1}) {SelectedPokes[item]['name']} ({SelectedPokes[item]['curr']['income']}/h)',
                    value=f'trade|{index+1}|{rare[0]}-{rare[1]}|{ctx.author.id}-{mentionedUser.id}'
                    )
                )

        view = SelectMassPokemonsViewSelectPoke(options=options, user=ctx.author.id)
        await ctx.send(f"{mentionedUser.id} - {sennedPokemon}", view=view)

    @commands.command(name='bidding', aliases=['bid', 'аукцион', 'аук', 'торги'])
    async def bidding(self, ctx):
        pass

    @commands.command(name='support', aliases=['пдж', 'поддержка', 'sup'])
    async def support(self, ctx):
        pass

    @commands.command(name='upgradepoke', aliases=['upp', 'улучшение'])
    async def upPoke(self, ctx):
        pass

    @commands.command(name='remelting', aliases=['плавка', 'переплавка', 'rem'])
    async def remelting(self, ctx):
        pass

    @commands.command(name='lookbag', aliases=['рюкзак', 'lb', 'рюк'])
    async def lookBag(self, ctx):
        pass



    @commands.command(name='marketpoke', aliases=['mp', 'магаз', 'магазин'])
    async def marketPoke(self, ctx):
        
        try:
            with open('../PonyashkaDiscord/content/lotery/market.yaml', 'r', encoding='utf-8') as file:
                market = yaml.safe_load(file)
        except:
            market = {
                "config":{
                    "timestamp":0
                    },
                "items":{}
                }
            with open('../PonyashkaDiscord/content/lotery/market.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(market, file)


        try:
            comm = ctx.message.content.split()
            comm.pop(0)

            listComm = []
            for item in comm:
                if '-' in item:
                    listComm.append((item.split('-')[0], item.split('-')[1]))
        except:
            comm = None

        buying = False

        listBuy = []

        if comm is not None:
            for command in listComm:
                keys = market['items'].keys()

                for item in keys:
                    noItem = False
                    # Проверка на релевантность покупки, если там есть указанные товары
                    if market['items'][item]['name'].lower() == command[0].lower():
                        
                        if command[1].isdigit():
                            if int(command[1]) > 0: value = int(command[1])
                            else: value = 1
                        else: value = 1

                        count = market['items'][item]['count']
                        if count - value < 0: value = int(count)
                        if value == 0: 
                            buy = False
                            noItem = True

                        price = market['items'][item]['price']
                        userCurr = db.Money(user=ctx.author.id, currency=market['items'][item]['curr']).have()
                        if value * price > userCurr or noItem: 
                            buy = False 
                        else: 
                            buy = True
                        
                        if buy:
                            # Загрузка функции
                            func = pickle.loads(market['items'][item]['added'])
                            func(user=ctx.author.id, value=value, price=market['items'][item]['price'])
                            market['items'][item]['count'] -= value

                            with open('../PonyashkaDiscord/content/lotery/market.yaml', 'w', encoding='utf-8') as file:
                                yaml.dump(market, file)
                        

                        buying = True
                        listBuy.append((market['items'][item]['name'], value, market['items'][item]['price'], (buy, userCurr, market['items'][item]['curr_r'], noItem)))

        if buying:
            text = ''
            for index, item in enumerate(listBuy):
                if item[3][0]:
                    text += f'**({index+1}) Куплен предмет: `[{item[0]}]` \n| `[{item[1]}/шт]` по цене `({item[2]:,}/штука)`**\n\n'
                elif item[3][3]:
                    text += f'**({index+1}) Предмета [{item[0]}] — Ожидайте завоз.**\n'
                else:
                    text += f'**({index+1}) Недостаточно денег для [{item[0]}], требуется `[{(item[1]*item[2]):,} {item[3][2]}]`, у вас `[{item[3][1]:,} {item[3][2]}]`**'
            embed = disnake.Embed(description=text)
            await ctx.send(embed=embed)
            return

        timestamp = market['config']['timestamp'] - round(time.time())

        if timestamp < 0: 
            updateStamp = True
        else: 
            updateStamp = False
            timeStruct = time.gmtime(timestamp)
            times = time.strftime(f'{timeStruct[2]-1}:%H:%M:%S', timeStruct)

        
        mainText = ''
        if updateStamp:
            associateItems = {
                    "1":{
                        "name":"Билет",
                        "desc":"Простой билет для гачи. Чаще всего он стоит в разы дешевле, но количество ограничено.",
                        "rank":"GRAY",

                        "added":pickle.dumps(addTiket),

                        "count":random.randrange(50, 200, 5),
                        "price":random.randrange(3500, 17500, 500),
                        "curr":"ESSENCE", "curr_r":"es"
                        },
                    "2":{
                        "name":"Душа",
                        "desc":"Душа сильного существа. Откуда поставщик Лид добывает их, неизвестно, но поставки регулярные.",
                        "rank":"GREEN",

                        "added":pickle.dumps(addSoul),

                        "count":random.randrange(200, 700, 10),
                        "price":random.randrange(50, 300, 10),
                        "curr":"SHARD", "curr_r":"sh"
                        },
                    "3":{
                        "name":"Эссенция монстра",
                        "desc":"Эссенция монстра для развития покемонов.",
                        "rank":"GREEN",

                        "added":pickle.dumps(addPokeEssence),

                        "count":random.randrange(200, 700, 10),
                        "price":random.randrange(50, 750, 10),
                        "curr":"SHARD", "curr_r":"sh"
                        }
                }

            for index, item in enumerate(associateItems):
                if index == 5: break

                tere = associateItems[item]

                mainText += f'### {index+1}. {tere['name']} ({tere['count']}/{tere['count']})\n| `Описание:` {tere['desc']}\n| `Стоимость:` **{tere['price']}**{tere['curr_r']} / one\n'

                market['items'][item] = {
                    "name":tere['name'],
                    "desc":tere['desc'],
                    "added":tere['added'],

                    "max_count":tere['count'],
                    "count":tere['count'],

                    "price":tere['price'],
                    "curr":tere['curr'], 
                    "curr_r":tere['curr_r']
                    }
            else:
                market['config']['timestamp'] = round(time.time()) + 259200


                with open('../PonyashkaDiscord/content/lotery/market.yaml', 'w', encoding='utf-8') as file:
                    yaml.dump(market, file)

        else:
            with open('../PonyashkaDiscord/content/lotery/market.yaml', 'r', encoding='utf-8') as file:
                loadMarket = yaml.safe_load(file)
            
            for index, item in enumerate(loadMarket['items']):
                if index == 5: break

                tere = loadMarket['items'][item]

                mainText += f'### {index+1}. {tere['name']} ({tere['count']}/{tere['max_count']})\n| `Описание:` {tere['desc']}\n| `Стоимость:` **{tere['price']}**{tere['curr_r']} / one\n'


        embed = disnake.Embed(
            title='Шайтан магазин дряхлого {Санди}',
            description=mainText
            )
        
        if updateStamp:
            embed.set_footer(text='При вас торговец раставил новые товары.\nДля покупки: !mp <товар>-<количество>')
        else:
            embed.set_footer(text=f'До завоза нового товара: [{times}]\nДля покупки: !mp <товар>-<количество>')


        await ctx.send(embed=embed)
        



    @commands.command(name='pokedex', aliases=['пхелп', 'покедекс', 'опокемонах', 'ph', 'phelp'])
    async def pokedex(self, ctx):

        embed = disnake.Embed(
            description='''
            ## Когда доделает понь обнову, появится и тут информация.
            '''
            )
        await ctx.send(embed=embed)

    # TODO: Не забыть добавить эту наглядную команду для награждения
    @commands.command(name='buggift', aliases=['b'])
    async def buggift(self, ctx):
        ment = ctx.message.mentions[0]

        await ctx.send(ment.id)

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Economics(bot))