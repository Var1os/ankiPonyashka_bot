import disnake
from disnake.ext import commands
from .module import REQ_database as Rdb
import random
import time
import json
import sqlite3
import asyncio

db = Rdb.DataBase

def banList(UID:int) -> bool:
    with open('../bots/config/message_banList.json') as file:
        config = json.load(file)
        file.close()
        if UID in config['list']:
            return False
        return True
    
class Message(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_message(self, message):
        
        # Установка главных переменных
        user = message.author.id
        timeMessage = time.strftime('%H:%M', time.gmtime(round(time.time() + 36000)))
        # Проверка на ботовость того, кто отправил сообщение
        if message.author.bot: return
        else: db.Check(user_id=message.author.id).user()


        try:
            con = sqlite3.connect('../bots/_system.db')
            cur = con.cursor()
            cur.execute(f"UPDATE channel_data SET count = count + 1 WHERE ID = {message.channel.id}")
            con.commit()
        except:
            pass

        # Проверка на упоминание пользователя и инкремент при правде
        mentioned = message.raw_mentions
        if (mentioned is not None):
            try:
                ment= message.raw_mentions[0]
                user_data = db.Info(user_id=user).user()
                if (user_data[2] < round(time.time())) and ment != user:
                    db.User(user_id=ment, value=1, column='mentions').upParam()
                    db.User(user_id=user, value=30).lockMent()
            except:
                pass
            
        if message.guild is None:
            print(f'Личные сообщения >>> {message.content}')
            return
        # Проверка актуальности уровня
        userExpNow= db.Info(user_id=user).takeFromRPG(table='user_main_info')[2]
        userLvlNow= db.Info(user_id=user).takeFromRPG(table='user_main_info')[1]
        userLvl = db.Info().positionLVL(exp=userExpNow)
        # Загрузки конфигурацции
        with open(f'../bots/config/levels/{message.guild.id}.json') as f:
            level_config = json.load(f)
            rank = []
            for item in level_config:
                rank.append(item)
            f.close()
        end = True
        s = []
        # Разбиваем ключи на массив связанных чисел, для проверки диапазона
        for item in level_config: s.append(item.split('-'))
        iser = []
        # Проверка диапазона по связанным ключам
        for item in s:
            try: iser.append(int(item[0]) <= userLvl <= int(item[1]))
            except: end = False
        # Выдача ролей
        bl = banList(user)
        if end or bl:
            ti = 0
            for index, item in enumerate(iser):
                if item:
                    ti = index
                    await message.author.add_roles(self.bot.get_guild(message.guild.id).get_role(level_config[rank[index]][0]))
            for index, item in enumerate(iser):
                if index != ti:
                    await message.author.remove_roles(self.bot.get_guild(message.guild.id).get_role(level_config[rank[index]][0]))
            
        if userLvl != userLvlNow:
            embed = disnake.Embed(
            title=f'Изменение силы души у: \n``{message.author.name}`` | ``{message.author.nick}``',
            description=f'Сила души изменилась\n```с {userLvlNow} до {userLvl}```',
            colour=disnake.Color.dark_gold()
            )
            embed.set_thumbnail(url=message.author.avatar)
            db.User(column='lvl', user_id=user, value=userLvl).setParam()
            print(f'Code 1 >>> Обновление уровня у пользователя {message.author.name}')
            await self.bot.get_channel(992673176448417792).send(embed=embed)
            await asyncio.sleep(1)


        # Проверка таймера реакций
        if db.Bot(self).checkLock():
            return

        # Загрузка конфигов
        with open('../bots/config/message_cfg.json') as file:
            config = json.load(file)
        # Проверка на создателя
        if message.author.id != 374061361606688788:
            # Выпадения опыта ~30% и денег с шансом ~10%
            # Шанс выпадения шарда с шансом 0,005%
            valueRandom = random.randint(1, 1000)
            valuePupet = random.randint(1,5)
            if valueRandom <= config['exp']:  # Выпадение опыта ')
                db.Exp(user_id=user, value=valuePupet).add()
                db.Bot(value=10).lock()
                return
            if valueRandom <= config['money']:  # Выпадение денег
                val = random.randint(0, 1000)
                if val <= config['super_money']:
                    db.Money(user=user, currency='SHARD', value=valuePupet).add()
                    return
                db.Money(user=user, value=valuePupet).add()
                db.Bot(value=10).lock()
                return

        # Исключение частых символов
        simbol = '/.,&?!()'
        content = message.content
        for item in simbol:
            content = content.replace(item, '')

        # Проверка на разрешенный канал
        file = open(f"../bots/acesses/{message.guild.id}.txt", mode='a+')
        file.seek(0)
        susc = []
        for item in file:
            susc.append(item.rstrip())
        file.close()

        # Проверка на канал в котором произошел ивент
        if str(message.channel.id) not in susc:
            return
        # простые слова-реакции
        file = open('../bots/React_text/Base_react_pony.txt', mode='r', encoding='utf-8')
        num = random.randint(1, 1000)
        mass_react = []
        for ent in file:
            mass_react.append(ent.rstrip())
        file.close()
        
        # Случайные реакции поняшки
        if num <= config['text_react_chance']:
            await message.channel.send(f"_{random.choice(mass_react)}_")
            db.Bot(value=config['text_react_timer']).lock()
            return
        # if num <= config['emoji_react_chance']:
        #     emoji = message.guild.emojis
        #     await message.channel.send(random.choice(emoji))
        #     db.Bot(value=config['emoji_react_timer']).lock()
        #     return
        # if num <= config['reaction_react_chance']:
        #     emoji = message.guild.emojis
        #     await message.add_reaction(random.choice(emoji))
        #     db.Bot(value=config['reaction_react_timer']).lock()
            return
        # Слова на которые откликается бот
        react_role = config['reaction_word']
        if message.author.id == 374061361606688788:
            return
        # Отклик поняшки на слова, что указаны в config.json["reaction_word"]
        for content in content.split(' '):
            for react in react_role:
                if content.lower() == react:
                    choice = random.randint(1, 4)
                    emoji = message.guild.emojis
                    if choice == 1:
                        await message.channel.send(f"_{random.choice(mass_react)}_")
                        db.Bot(value=30).lock()
                        return
                    # elif choice == 2:
                    #     await message.channel.send(random.choice(emoji))
                    #     db.Bot(value=20).lock()
                    #     return
                    # elif choice == 3:
                    #     await message.add_reaction(random.choice(emoji))
                    #     db.Bot(value=20).lock()
                    #     return


# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Message(bot))