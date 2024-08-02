from typing import Coroutine
import disnake
from disnake.ext import commands
from random import randint

import asyncio
import json

from .module.SystemCommandRPG import *

class RPG(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    # TODO: need think how do this
    @commands.command(name='fight', aliases=['f'])
    async def fight(self, ctx):
        pass
    

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


    @commands.command(name='stat') #! Aliases add more variation
    async def stat(self, ctx, study=False):
        if ctx.message.author.id != 374061361606688788:
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
        text2 = f'**Главные валюты**\n- Эссенции душ: _`{money['ESSENCE']}`_\n- Осколки душ: _`{money['SHARD']}`_\n- Души: _`{money['SOUL']}`_\n- Кристальные души: _`{money['CRISTAL_SOUL']}`_\n\n**Другие валюты**\n- Монеты «Системы»: _`{money['COU']}`_\n- Монеты «Пустоты»: _`{money['VCOIN']}`_\n- Монеты «Сущности»: _`{money['ACOIN']}`_\n- Монеты «Истины»: _`{money['TCOIN']}`_'


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
        text3 = f'☥ **Духовная сила** - _`{body['SS']}`_ ☥\n```Основная```♥ **Здоровье (+{body['REG']/100}s):** _`{body['HP']}`_\n🐎**Ловкость:** {body['STR']}\n☗ **Защита:** _`{body['DEF']}`_\n♣ **Удача:** _`{body['LUCK']}`_\n\n🩸 **Атака:** _`{body['ATK']}`_\n🧨 **Крит.Удар:** _`{body['CRIT']/100+1}x ({body['CCRIT']}%)`_ {additional}'

 
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
        text7 = f''


        # other information page
        text8 = f''


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
        buttons = [
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='◀', custom_id='back'),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label='▶', custom_id='next'),
            disnake.ui.Button(style=disnake.ButtonStyle.red, label='✖', custom_id='dropStat')
            ]
        terms = int(DataBase.RPG().info(user_id=user, table='user_terms')[3]) == 1
        if terms and not study:
            buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='???', custom_id='talk'))
            
        message = await ctx.send(embed=disnake.Embed.from_dict(embeds[f'{pageStart}']), components=buttons)
        message_id = message.id

        if terms:
            temporal = {
                "phase":1,
                "dialog_text":1,
                "message_id":message_id
                }
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

        # await deleteAfterEmbed(json_name='stat_list.json', message=message, time=60)


    @commands.command(name='test')
    async def test(self, ctx):
        pass

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(RPG(bot))