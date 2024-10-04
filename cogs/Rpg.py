import disnake
from disnake.ext import commands

import json
import time
from time import time, strftime, gmtime
from random import randint, choices

from .module.SystemCommandRPG import *
from .module.REQ_database import DataBase
from .materials.enemy_base.lowEnemy import Goblin

db = DataBase

class RPG(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.command(name='bag', aliases=['мешок', 'хабар'])
    async def bag(self, ctx):

        user = ctx.message.author.id
        stat = await userData(uid=user)
        
        money = stat['money']
        text = f'## Шэкэли, что ты насобирал \n```Эссенции = {money['ESSENCE']}\nОсколки = {money['SHARD']}\nДуши = {money['SOUL']}``````Кристальные души = {money['CRISTALL_SOUL']}``````Монеты «Коширского» = {money['COU']}\nМонеты «Сущности» = {money['ACOIN']}\nМонеты «Пустоты» = {money['VCOIN']}\nМонеты «Истины» = {money['TCOIN']}```'

        embed = disnake.Embed(
            description=text
            ).set_thumbnail(url=ctx.message.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='daily', aliases=['подарок', 'сбор', 'gift'])
    async def daily(self, ctx):
        
        user = ctx.message.author.id
        times = db.Lock(user_id=user, slot=5).info()[0]
        gift = ["ESSENCE", "SHARD", "SOUL", "CRISTALL_SOUL", "COU", "VCOIN", "ACOIN", "TCOIN"]
        gift_chance = [.559, .30, .10, .001, .01, .01, .01, .01]
        with open('../bots/content/system/association.json', encoding='UTF-8') as file:
            associat = json.load(file, )

        if db.Lock(user_id=user, slot=5).ready():
            drop = choices(gift, weights=gift_chance)[0]
            color = disnake.Colour.from_rgb(255, 244, 33)

            db.Money(user=user, currency=drop, value=1).add()
            db.Lock(user_id=user, slot=5, value=43_200).lock()
            embed = disnake.Embed(
                title='Подарочная коробка 🎉', 
                description=f'```Ого! Ты получил из коробки: \n>> [{associat['money'][drop]['name']}] (+1 {associat['money'][drop]['tag']}). \nПриходи завтра ещё!```',
                colour=color)
            await ctx.send(embed=embed)
            return
        good_format_time = strftime('%H:%M:%S', gmtime(times-time.time()))
        color = disnake.Colour.from_rgb(89, 85, 8)

        embed = disnake.Embed(
            title='Подарочная коробка', 
            description=f'```Увы, ты уже забирал коробочку, \nприходи чуть позже, \nскажем... \nЧерез {good_format_time}, хорошо?```',
            colour=color)
        await ctx.send(embed=embed)

    # TODO: need think how do this
    @commands.command(name='fight', aliases=['f'])
    async def fight(self, ctx):
        
        #? Основное определение визуальной части системы боя
        embed = disnake.Embed()
        embed.title = ''

        enemyForm = ''
        base = []
        for i in range(randint(1, 5)):
            base.append(Goblin())
        else: base
        for index, item in enumerate(base): enemyForm += f'{index+1}. {item.name} ({item.HP}hp)\n'
        
        playerForm = ''
        for i in range(3): playerForm += f'{i+1}. Игрок/соратник\n'
        

        embed.description = f'## Testing fight system\n`{enemyForm}`\n```\t/ - / - / - /```\n`{playerForm}`'
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/1206487729995517962/1244870023017664614/gqwaSu0_wRo.jpg?ex=66ea570e&is=66e9058e&hm=c83116a688a7d724ec03c9e342c577018e5763f4bf0b4b095ab7fe692d5a6048&=&format=webp&width=577&height=676')

        #? Определение кнопочек боя
        buttons = await getButtonsFight()
        
        #? Определение важных элементов контейнера
        players = []

        #? Контейнер с информацией о бое и доп информация
        container = {
            "message":ctx.message.id,
            "players":players
            }
        
        await ctx.send(embed=embed, components=buttons)
    
    #! listener for switching pages
    @commands.Cog.listener('on_button_click')
    async def stat_list(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ['next', 'back', 'dropStat']:
            return
        
        try:
            with open('../bots/config/stat_list.json', encoding='UTF-8') as file:
                stat_list = json.load(file)
                file.close()

            message = stat_list[f'{inter.message.id}']

            if message['author'] != inter.author.id:
                await inter.response.send_message('`Отказано в доступе. Вы не являетесь автором вызова.`', ephemeral=True)
                return
            
            if inter.component.custom_id == 'next':
                if message['index']+1 > len(message['embeds']):
                    await inter.response.defer()
                    return
                message['index']+= 1
                await inter.response.edit_message(embed=disnake.Embed.from_dict(message['embeds'][f'{message['index']}']))
            elif inter.component.custom_id == 'back':
                if message['index']-1 <= 0:
                    await inter.response.defer()
                    return
                message['index']-= 1
                await inter.response.edit_message(embed=disnake.Embed.from_dict(message['embeds'][f'{message['index']}']))
            elif inter.component.custom_id == 'dropStat':
                embed = disnake.Embed(title='Информация',description='```Окно закрыто пользователем.```')
                await inter.response.edit_message(embed=embed, components=None)
                return
            
            with open('../bots/config/stat_list.json', mode='w', encoding='UTF-8', ) as file:
                file.write(json.dumps(stat_list, indent=3, ensure_ascii=False))
                file.close()
        except:
            embed = disnake.Embed(title='Информация',description='```Активно иное окно.```')
            await inter.response.edit_message(embed=embed, components=None)


    @commands.command(name='stat', alises=["стат", "статус"]) #! Aliases add more variation
    async def stat(self, ctx, study=False):
        if ctx.message.author.id not in [374061361606688788,777612548152229888, 351617185170325515]:
            await ctx.send('В переработке~')
            return

        user = ctx.message.author.id
        try: pageStart = int(ctx.message.content.split()[1])
        except: pageStart = 1
        if not 1 <= pageStart <= 8: pageStart = 1

        # main information of user. Here describe all need info.
        userDatal = await userData(uid=user)

        # main page
        # TODO: finalize this page, in particular achivm, title and rank
        achivm = 'Отсутсвуют'
        for index, item in enumerate(userDatal['main']['ACHIVM']): 
            if index != len(userDatal['main']['ACHIVM'])-1: achivm+=f'{item}, '
            else: achivm+=f'{item}'
        if achivm == '': achivm = 'Отсутсвуют'
        text1 = f'Уровень: `{userDatal['main']['LVL']} ({userDatal['main']['EXP']})`\nРепутация: {userDatal['main']['REP']}\n\nДостижения:```{achivm}```'
        
        
        # money page
        money = userDatal['money']
        text2 = f'**Главные валюты**\n- Эссенции душ: _`{money['ESSENCE']}`_\n- Осколки душ: _`{money['SHARD']}`_\n- Души: _`{money['SOUL']}`_\n- Кристальные души: _`{money['CRISTALL_SOUL']}`_\n\n**Другие валюты**\n- Монеты «Системы»: _`{money['COU']}`_\n- Монеты «Пустоты»: _`{money['VCOIN']}`_\n- Монеты «Сущности»: _`{money['ACOIN']}`_\n- Монеты «Истины»: _`{money['TCOIN']}`_'


        # body score page
        body = userDatal['parametr']
        additional = 'p'
        param = {
            "FLX":'🐍 **Гибкость:** ',
            "ST":'🦴 **Стойкость:** ',
            "STL":'👥 **Скрытность:** ',
            "SEN":'👀 **Восприятие:** ',
            "INS":'🧠 **Проницательность:** ',
            "CTR":'✊ **Контроль:** ',
            "GEN":'🧬 **Генетика:** ',
            "FR":'🔥 **Огонь:** ',
            "ER":'⛰ **Земля:** ',
            "AQ":'💧 **Вода:** ',
            "WD":'💨 **Воздух:** ',
            "HL":'✝ **Святость:** ',
            "WG":'☀ **Свет:** ',
            "LG":'💀 **Токсин:** ',
            "DR":'⚫ **Тьма:** ',
            }
        for item in param:
            if body[item] != 0:
                additional += f'{param[item]}_`{body[item]}`_\n'
        if additional == 'p': additional = ''
        else: additional = additional.replace('p', '\n\n```Дополнительная```')
        text3 = f'☥ **Духовная сила** - _`{body['SS']}`_ ☥\n```Основная```♥ **Здоровье (+{body['REG']/100}ц):** _`{body['HP']}`_\n🐎**Ловкость:** {body['STR']}\n☗ **Защита:** _`{body['DEF']}`_\n♣ **Удача:** _`{body['LUCK']}`_\n\n🩸 **Атака:** _`{body['ATK']}`_\n🧨 **Крит.Удар:** _`{body['CRIT']/100+1}x ({body['CCRIT']}%)`_ {additional}'

 
        # equipment page
        equip = userDatal['equipment']
        main_text4 = '```Снаряжение```'
        emp = 'p'
        emp_param = {
            "EMP_HEAD":'**Голова:** ',
            "EMP_CHEST":'**Грудь:** ',
            "EMP_BELLY":'**Живот:** ',
            "EMP_RHAND":'**Правая рука:** ',
            "EMP_LHAND":'**Левая рука:** '
            }
        equip_param = {
            "HEAD":'**Голова:** ',
            "NEAK":'**Шея:** ',
            "FINGER_1":'**Безымянный (правый):** ',
            "FINGER_2":'**Безымянный (левый):** ',
            "HAND_L":'**Левая рука:** ',
            "HAND_R":'**Правая рука:** ',
            "BODY":'**Тело:** ',
            "LEGS":'**Ноги:** '
            }
        for index, item in enumerate(equip_param):
            if equip[item] != 0:
                main_text4 += f'{equip_param[item]}`{equip[item]}`\n'
            else:
                main_text4 += f'{equip_param[item]}`<None>`\n'
            if index in [1, 3, 5]:
                main_text4+='\n'
        for item in emp_param:
            if equip[item] != 0:
                emp += f'{emp_param[item]}_`{equip[item]}`_\n'
        if emp == 'p': emp = ''
        else: emp = emp.replace('p', '```Импланты```')
        text4 = f'{main_text4}{emp}'


        # items page
        item = userDatal['inventory']
        main_text5 = '```Предметы в карманах```'
        item_param = {
            "SLOT1":'**Слот 1:** ',
            "SLOT2":'**Слот 2:** ',
            "SLOT3":'**Слот 3:** ',
            "SLOT4":'**Слот 4:** ',
            "SLOT5":'**Слот 5:** '
            }
        for index, it in enumerate(item_param):
            if item[it] != 0:
                main_text5 += f'{item_param[it]}`{item[it]}`\n'
            else:
                main_text5 += f'{item_param[it]}`<None>`\n'
        # TODO: once perk get more slot for inventory, but relize this a little later.
        text5 = f'{main_text5}'


        # perk page
        perk = userDatal['perk']
        active = ''
        passive = ''
        special = ''
        text6 = f'```Позже доработать```'


        # diplomaty page
        text7 = f'```Да, когда-то надо```'


        # other information page
        text8 = f'```Возможно в этом веку```'


        embeds = {
            '1': {
                'title':'Главная страница',
                'description':text1,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 1/8'}
                },
            '2': {
                'title':'Финансы гражданина',
                'description':text2,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 2/8'}
                },
            '3': {
                'title':'Оценка тела',
                'description':text3,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 3/8'}
                },
            '4': {
                'title':'Обмундирование',
                'description':text4,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 4/8'}
                },
            '5': {
                'title':'Предметы при себе',
                'description':text5,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 5/8'}
                },
            '6': {
                'title':'Навыки',
                'description':text6,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 6/8'}
                },
            '7': {
                'title':'Отношения',
                'description':text7,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 7/8'}
                },
            '8': {
                'title':'Остальное',
                'description':text8,
                "thumbnail": {"url": ctx.message.author.avatar.url},
                'footer':{'text':'Страница 8/8'}
                }
            }
        if not study:
            buttons = [
                disnake.ui.Button(style=disnake.ButtonStyle.gray, label='◀', custom_id='back'),
                disnake.ui.Button(style=disnake.ButtonStyle.gray, label='▶', custom_id='next'),
                disnake.ui.Button(style=disnake.ButtonStyle.red, label='✖', custom_id='dropStat')
                ]
        terms = int(DataBase.RPG().info(user_id=user, table='user_terms')[3]) == 1
        if terms and not study:
            buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='???', custom_id='first_talk_with_player'))
            
        if not study: message = await ctx.send(embed=disnake.Embed.from_dict(embeds[f'{pageStart}']), components=buttons)
        else: message = await ctx.send(embed=disnake.Embed.from_dict(embeds[f'{pageStart}']))
        message_id = message.id

        if terms and not study:
            temporal = await createMetadata(message_id=message_id)
            with open(f'../bots/content/dialogs/temporal_dialog/{user}.json', mode='w', encoding='UTF-8') as file:
                file.write(json.dumps(temporal, indent=3, ensure_ascii=False))
                file.close()

        try: 
            with open('../bots/config/stat_list.json') as file:
                stat_list = json.load(file)
                file.close()
        except: pass
        try:
            stat_list[message_id] = {
                'author':user,
                'index':pageStart,
                'embeds':embeds
                }
        except:
            stat_list = {
                message_id:{
                    'author':user,
                    'index':pageStart,
                    'embeds':embeds
                    }
                }
        with open('../bots/config/stat_list.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(stat_list, indent=3, ensure_ascii=False))
            file.close()

        await deleteAfterEmbed(json_name='stat_list.json', message=message, time=60)


    @commands.command(name='location', aliases=['локация', 'лока'])
    async def location(self, ctx):
        if ctx.message.guild.id not in [374061361606688788,777612548152229888]:
            await ctx.send('`В разработке.`')
            return
        check_terms_noob = db.Info(user_id=ctx.message.author.id).takeFromRPG(table='user_terms')
        if check_terms_noob[3] == True: 
            await ctx.send('`Сначала изучите главное в ~stat`')
            return
        try: 
            user_pararmetr = ctx.message.content.split()[1]
            user_pararmetr_command = ctx.message.content.split()[2]
        except: pass

    @commands.command(name='carddrop', aliases=['card'])
    async def card(self, ctx):
        mast = ['пики ♠', 'буби ♦', 'червы ♥', 'трефы ♣']
        value = [2, 3, 4, 5, 6, 7, 8, 9, 'Валет', 'Дама', 'Король', 'Туз']

        text = f'{choice(value)} {choice(mast)}'
        if randint(1, 100) > 90:
            text = f'О нет! {choice('Красный', 'Черный')} джокер!'
        
        embed = disnake.Embed(title=text)
        await ctx.send(embed=embed)

    @commands.Cog.listener('on_button_click')
    async def test_listener(self, inter:disnake.MessageInteraction):
        if inter.component.custom_id not in ['test']:
            return

        # print(inter.response.type())
        try:
            print('done=', inter.response.is_done())
            print('defer=',await inter.response.defer())
            print('done=', inter.response.is_done())
            print('type=', inter.component.type())
        except:
            print('error')


    @commands.command(name='testdialog')
    async def testdialog(self, ctx):

        button = disnake.ui.Button(style=disnake.ButtonStyle.green, label='Начать', custom_id='testDialog')
        message = await ctx.send('Тестовый диалог с персонажем.', components=button)
        temporal = await createMetadata(message.id)
        with open(f'../bots/content/dialogs/temporal_dialog/{ctx.author.id}.json', mode='w', encoding='UTF-8') as file:
            file.write(json.dumps(temporal, indent=3, ensure_ascii=False))
            file.close()

    @commands.command(name='test')
    async def test(self, ctx):
        name = ctx.message.content.replace(f'{ctx.message.content.split(' ')[0]} ', '')
        try: foundPoke, rare = await findPokemonInDatabaseLikeName(name=name)
        except: 
            foundPoke = await findPokemonInDatebase(ID=name)
            rare = name.split('-')
        try: crafteble = 'Да' if foundPoke['crafteble'] else 'Нет'
        except: crafteble = 'Неизвестно'
        try: desc = foundPoke['description']
        except: desc = '-Отсутсвует-'
        try: gif = foundPoke['gif']
        except: gif=None
        embed = disnake.Embed(
            title=f'Покемон [{foundPoke['name']}]',
            description=f'`Описание:`\n{desc}\n\n',
            )
        embed.add_field(name='Цена', value=f'{foundPoke['price']}')
        embed.add_field(name='Доход', value=f'{foundPoke['income']}')
        embed.add_field(name='Редкость', value=f'{rare[0]}-{rare[1]}')
        embed.set_thumbnail(url=gif)
        embed.set_footer(text=f'Возможность крафта: {crafteble}')
        await ctx.send(embed=embed)

    @commands.command(name='test2')
    async def test2(self, ctx):
        data = await RollLotery(user=ctx.author.id, count=10, sys=True)
        text = ''
        for index, item in enumerate(data['loot']):
            text += f'## ({index+1})→ {item[1]['name']} `(Rank: {item[0]})`\n'
        embed = disnake.Embed(
            description=f"# ```Ты выиграл в лотери...```\n{text}\n## `{data['compliment']}`\n",
            colour=disnake.Colour.dark_gold()           
            )
        embed.set_footer(text=f'Крутил барабан: {ctx.author.name}')
        await savePokemon(loot=data['loot'], uid=ctx.author.id)
        await ctx.send(embed=embed)

    #? save history channel
    @commands.command(name='test3')
    async def test3(self, ctx):
        messages = []
        user = ctx.message.author.id
        async for ctx.message in ctx.channel.history(limit=50):
            messages.append(f'{ctx.message.author.name} >>> {ctx.message.content}\n')

        # for item in messages:
        #     print(item)

        with open('../bots/content/system/text.txt', 'w') as file:
            for item in messages:
                file.writelines(item)
        with open('../bots/content/system/text.txt', 'rb') as file:
            await ctx.send(f'len_load={len(messages)}', file=disnake.File(file, 'text.txt'))

    #? calculate summ all message in channel and give time writing
    @commands.command(name='test4')
    async def test4(self, ctx):

        timer = round(time())
        count = 0

        async for ctx.message in ctx.channel.history(limit=None):
            count += 1
        
        await ctx.send(f'times need for read= {strftime('%H:%M:%S', gmtime(round(time()-timer)))}\nCount message={count}')

    @commands.command(name='test5')
    async def clearConsole(self, ctx):
        import os
        os.system('cls')


# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(RPG(bot))