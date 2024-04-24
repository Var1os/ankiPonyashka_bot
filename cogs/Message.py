import disnake
from disnake.ext import commands
from .module import REQ_database as Rdb
import random
import time

db = Rdb.DataBase

class Message(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author.id
        timeMessage = time.strftime('%H:%M', time.gmtime(round(time.time() + 36000)))
        # Проверка на ботовость того, кто отправил сообщение
        if message.author.bot:
            return
        else:
            db.Check(user).user()

        mentioned = message.raw_mentions
        if (mentioned is not None):
            try:
                ment= message.raw_mentions[0]
                user_data = db.Info(user_id=user).user()
                if (user_data[5] < round(time.time())) and ment != user:
                    db.User(user_id=ment, value=1, column='mentions').upParam()
                    db.User(user_id=user, value=30).lockMent()
            except:
                pass
            
        
        # Проверка актуальности уровня
        userExpNow= db.Info(user_id=user).user()[2]
        userLvlNow= db.Info(user_id=user).user()[1]
        userLvl = db.Info().whatIsLvl(exp=userExpNow)
        if userLvl > userLvlNow:
            db.User(column='lvl', user_id=user, value=userLvl).setParam()
            await self.bot.get_channel(1205649033125830706).send(
                f'У {message.author.global_name} Повышен уровень c {userLvlNow} до {userLvl}')

        # Проверка таймера реакций
        if db.Bot(self).checkLock():
            return

        # Выпадения опыта или денег с шансом 10%
        # Шанс выпадения шарда с шансом 0,005%
        valueRandom = random.randint(1, 200)
        valuePupet = random.randint(1,5)
        if valueRandom >= 180:  # Выпадение опыта
            print(f'{timeMessage} | Выпал опыт | {message.author.global_name} ')
            db.Exp(user=user, value=valuePupet).add()
            db.Bot(value=10).lock()
            return
        elif valueRandom <= 40:  # Выпадение денег
            if (random.randint(1, 10000)) <= 5:
                print(f'{timeMessage} | Выпали супер-деньги | {message.author.global_name}')
                db.Money(user=user, currency='shard', value=valuePupet).add()
                return
            print(f'{timeMessage} | Выпали деньги | {message.author.global_name}')
            db.Money(user=user, value=valuePupet).add()
            db.Bot(value=10).lock()
            return

        # Исключение частых символов
        simbol = '/.,&?!()'
        content = message.content
        for item in simbol:
            content = content.replace(item, '')

        # Проверка на разрешенный канал
        if message.guild is None:
            return
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
        num = random.randint(1, 200)
        mass_react = []
        for ent in file:
            mass_react.append(ent.rstrip())
        file.close()

        # Гифки
        file = open('../bots/content/Gif/base.txt', mode='r')
        gifs = []
        for item in file:
            gifs.append(item.rstrip())
        file.close()
        
        # Случайные реакции поняшки
        if num <= 2:
            print(f"{timeMessage} | Случайный_ответ | {message.channel}")
            await message.channel.send(f"_{random.choice(mass_react)}_")
            db.Bot(value=30).lock()
            return
        elif num <= 4:
            print(f"{timeMessage} | Случайный_ответ_2 | {message.channel}")
            emoji = message.guild.emojis
            await message.channel.send(random.choice(emoji))
            db.Bot(value=20).lock()
            return
        elif num <= 6:
            print(f"{timeMessage} | Случайный_ответ_3 | {message.channel}")
            emoji = message.guild.emojis
            await message.add_reaction(random.choice(emoji))
            db.Bot(value=20).lock()
            return
        '''elif num >= 198:
            print(f"{timeMessage} | Случайный_ответ_4 | {message.channel}")
            await message.channel.send(random.choice(gifs))
            db.Bot(value=20).lock()
            return
        '''
        # Слова на которые откликается бот
        react_role = ["пони", "поня", "понь", "поню", "поняш", "поняшь", "pony", "ponyash", "поняшка",
              "понёй", "поняхи", "понем", "понём", "поняшки"]

        # Отклик поняшки на слова, что указаны в [строчке 113]
        for content in content.split(' '):
            for react in react_role:
                if content.lower() == react:
                    choice = random.randint(1, 4)
                    emoji = message.guild.emojis
                    if choice == 1:
                        print(f"{timeMessage} | Ответ | {message.channel}")
                        await message.channel.send(f"_{random.choice(mass_react)}_")
                        db.Bot(value=30).lock()
                        return
                    elif choice == 2:
                        print(f"{timeMessage} | Ответ_2 | {message.channel}")
                        await message.channel.send(random.choice(emoji))
                        db.Bot(value=20).lock()
                        return
                    elif choice == 3:
                        print(f"{timeMessage} | Ответ_3 | {message.channel}")
                        await message.add_reaction(random.choice(emoji))
                        db.Bot(value=20).lock()
                        return
                    '''elif choice == 4:
                        print(f"{timeMessage} | Ответ_4 | {message.channel}")
                        await message.channel.send(random.choice(gifs))
                        db.Bot(value=20).lock()
                        return
                    '''


# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Message(bot))
    print(f'Запуск модуля MESSAGE.system')