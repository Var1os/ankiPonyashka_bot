from .module import RequestDataBaseZarato as Rdb
from .module.Slicer import PagReact as pag

import random
import time

import disnake
from disnake.ext import commands

db = Rdb.DataBase

class Economycs(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
    
    @commands.command(name='work')
    async def work(self, ctx):
        if not ctx.guild is None:
            serverT= [1199488197885968515, 958063150144577558] # Дом поняшки, сервер зарато
            if ctx.guild.id not in serverT:
                return

        user = ctx.message.author.id
        db.Check(user_id= user).user()
        
        if db.Money(user= user).checkTimeLock():

            count = random.randint(5, 40)
            
            # Аудит заработка в консоль
            times = time.strftime('%H:%M', time.gmtime(round(time.time() + 36000)))
            print(f'{ctx.message.author.name} заработал {count} эссенций в {times}')

            # Взаимодействие с валютой
            db.Money(user= user, currency='essence', value=count).add
            db.Money(user= user).lock(valueLock=3600, lockLvl='low')

            emb = disnake.Embed(title=f"Заработано - {count} MaCoin(ов)", colour=disnake.Color.dark_gold())
        else:
            times = time.strftime('%H:%M:%S', time.gmtime(db.Money(user= user).lockTake() - time.time()))
            emb = disnake.Embed(description=f'Остудись, ещё не время работать.\nОсталось подождать: {times}', colour=disnake.Color.red())
            
        await ctx.send(embed=emb)

    #! Прослушка
    @commands.Cog.listener('on_button_click')
    async def stat_list(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ['next', 'back', 'dropStat']:
            return
        if self.user != inter.author.id:
            await inter.response.send_message('Данное сообщение вызвали не вы', ephemeral=True)
            return
            #! Расписать ответ для других пользователей

        if self.timeout < round(time.time()):
            embed = disnake.Embed(title='Паспорт',description='_Окно было закрыто..._\n_Вышло время_').set_thumbnail(url=inter.author.avatar)
            await inter.response.edit_message(embed=embed, components=None)
            return
        
        if inter.component.custom_id == 'next':
            if self.index+1 > len(self.embeds)-1:
                await inter.response.edit_message(embed=self.embeds[self.index])
                return
            self.index+= 1
            await inter.response.edit_message(embed=self.embeds[self.index])
        elif inter.component.custom_id == 'back':
            if self.index-1 < 0:
                await inter.response.edit_message(embed=self.embeds[self.index])
                return
            self.index-= 1
            await inter.response.edit_message(embed=self.embeds[self.index])
        elif inter.component.custom_id == 'dropStat':
            embed = disnake.Embed(title='Паспорт',description='_Окно было закрыто..._').set_thumbnail(url=inter.author.avatar)
            await inter.response.edit_message(embed=embed, components=None)


    @commands.command(name='stat', aliases=['statistic', 'стат', 'статус', 'профиль'])
    async def stat(self, ctx):
        if not ctx.guild is None:
            serverT= [1199488197885968515, 958063150144577558] # Дом поняшки, сервер зарато
            if ctx.guild.id not in serverT:
                return

        self.user = ctx.message.author.id
        db.Check(user_id= self.user).user()
        db.Fun(user=self.user).maxis()

        baseStat = db.Info(user_id= self.user).user()
        moneyStat = db.Info(user_id= self.user).money()
        rpgStat = db.Info(user_id= self.user).system()
        wins_str = db.Info(user_id=self.user).any_table(table='user_wins_max')

        # Эмбиенд основного табла
        emb_main = disnake.Embed(title=f"Пользователь - {ctx.message.author.name}",
                            colour=disnake.Color.dark_gold(),
                            description=
                                '''**Уровень:** {n1}\n**Опыт:** {n2:,d}\n**Любовь поняшки:** {n3}\n
                                '''.format(n1= baseStat[1], n2= baseStat[2], n3= baseStat[3] - 500))
        emb_main.set_thumbnail(url=ctx.message.author.avatar)
        emb_main.set_footer(text='страница [1/3]')

        # Табло с количеством денег пользователя
        emb_money = disnake.Embed(title=f'Пользователь - {ctx.message.author.name}',
            colour=disnake.Color.dark_gold(),
            description=
                '''**Эссенции:** {n1:,d}\n**Осколки:** {n2:,d}\n**Души:** {n3:,d}\n\n**Кристалльная душа:** {n4:,d}
                '''.format(n1= moneyStat[1], n2= moneyStat[2], n3= moneyStat[3], n4= moneyStat[4]))
        emb_money.set_thumbnail(url=ctx.message.author.avatar)
        emb_money.set_footer(text='страница [2/3]')

        # Табло с винстриками пользователей
        emb_wins_str = disnake.Embed(title=f'Пользователь - {ctx.message.author.name}',
            colour=disnake.Color.dark_gold(),
            description=
                f'''**Винстрики в аркадах:**\nРусская рулетка ``(Max)``: ``{wins_str[3]}``\nМонеточка ``(Max)``: ``{wins_str[1]}``\nКазино ``(Max)``: ``{wins_str[2]}``
                ''')
        emb_wins_str.set_thumbnail(url=ctx.message.author.avatar)
        emb_wins_str.set_footer(text='страница [3/3]')

        self.embeds = [emb_main, emb_money, emb_wins_str]
        self.timeout = round(time.time()) + 45
        self.index= 0

        buttons= [
            disnake.ui.Button(style= disnake.ButtonStyle.green, disabled=False, label='Назад', custom_id='back'),
            disnake.ui.Button(style= disnake.ButtonStyle.green, disabled=False, label='Дальше', custom_id='next'),
            disnake.ui.Button(style= disnake.ButtonStyle.danger, disabled=False, label='Закрыть', custom_id='dropStat')
            ]

        await ctx.send(embed=emb_main, components=buttons)

        # message = await ctx.send(embed=self.embeds[self.index])
        # page = pag(self.bot, message, only=ctx.author, use_more=False, embeds=self.embeds, timeout=25)
        # await page.start()

    #! Прослушка
    @commands.Cog.listener("on_button_click")
    async def tran_select(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["essence_soul", "shard_soul", "soul", "cristall_soul", "cannel"] or inter.author.id != self.user:
            return
        # Проверка на наличие указанной суммы 
        trust = True
        if inter.component.custom_id != "cannel":
            have = db.Money(user=self.user, currency=str(inter.component.custom_id)).have()
            if self.value > have:
                emb = disnake.Embed(title='У вас недостаточно данной валюты')
                trust = False
        # essence
        if inter.component.custom_id == "essence_soul" and trust:
            db.Money(user=self.user, currency='essence', value=self.value).sub()
            db.Money(user=self.mentioned, currency='essence', value=self.value).add()
            emb = disnake.Embed(title=f'Вы перевели {self.value} эссенций')
        # shard
        elif inter.component.custom_id == "shard_soul" and trust:
            db.Money(user=self.user, currency='shard', value=self.value).sub()
            db.Money(user=self.mentioned, currency='shard', value=self.value).add()
            emb = disnake.Embed(title=f'Вы перевели {self.value} осколков')
            
        # soul
        elif inter.component.custom_id == "soul" and trust:
            db.Money(user=self.user, currency='soul', value=self.value).sub()
            db.Money(user=self.mentioned, currency='soul', value=self.value).add()
            emb = disnake.Embed(title=f'Вы перевели {self.value} душ')
        # cristall
        elif inter.component.custom_id == "cristall_soul" and trust:
            db.Money(user=self.user, currency='cristall', value=self.value).sub()
            db.Money(user=self.mentioned, currency='cristall', value=self.value).add()
            emb = disnake.Embed(title=f'Вы перевели {self.value} кристаллов')
        
        elif inter.component.custom_id == "cannel":
            emb = disnake.Embed(description='Вы забрали деньги обратно')
        await inter.response.edit_message(embed=emb, components=None)
        
    @commands.command(name='tran', aliases=['перевод', 'перед'])
    async def tran(self, ctx):
        if not ctx.guild is None:
            serverT= [1199488197885968515, 958063150144577558] # Дом поняшки, сервер зарато
            if ctx.guild.id not in serverT:
                return

        self.user = ctx.message.author.id
        db.Check(user_id=self.user).user()
        
        # Проверка на наличие количества передаваемой валюты
        try:
            self.value = abs(int(ctx.message.content.split(' ')[1]))
        except:
            embed = disnake.Embed(
                description='**Не указано количество**\n~tran ``(value)`` [mentioned]\nㅤㅤㅤ^^^^^^')
            return await ctx.send(embed=embed)
        
        # Проверка на наличие упомянутого человека
        try:
            self.mentioned = int(ctx.message.raw_mentions[0])
        except:
            embed = disnake.Embed(
                description='**Не указан пользователь**\n~tran (value) ``[mentioned]``\nㅤㅤㅤㅤㅤㅤ^^^^^^^^^^')
            return await ctx.send(embed=embed)

        # Ботов нельзя трогать
        if disnake.Guild.get_member(ctx.guild, self.mentioned).bot:
            await ctx.send('Не трожте ботов...')
            return
        # Нельзя отправлять самому себе валюту
        if self.user == self.mentioned:
            embed = disnake.Embed(
                description='Вы не можете отправить валюту сами себе')
            return await ctx.send(embed=embed)
        
        btn = disnake.ui
        emb = disnake.Embed(title= 'Какую валюту желаете перевести?').set_thumbnail(url=disnake.Guild.get_member(ctx.guild, self.mentioned).avatar)
        button_es = btn.Button(style=disnake.ButtonStyle.success, disabled=False, label='Эссенцию', custom_id="essence_soul")
        button_ch = btn.Button(style=disnake.ButtonStyle.success, disabled=False, label='Осколки', custom_id="shard_soul")
        button_soul = btn.Button(style=disnake.ButtonStyle.success, disabled=False, label='Души', custom_id="soul")
        button_cristal = btn.Button(style=disnake.ButtonStyle.success, disabled=False, label='Кристалы', custom_id="cristall_soul")
        cannel = btn.Button(style=disnake.ButtonStyle.danger, disabled=False, label='Отмена', custom_id="cannel")
        self.buttons = [button_es, button_ch, button_soul, button_cristal, cannel]

        db.Check(user_id=self.mentioned).user()

        await ctx.send(embed=emb, components=self.buttons)

    #! Функция пустая, следует доделать позже
    @commands.command(name='shop', aliases=['магаз', 'sh'])
    async def shop(self, ctx):

        # ! Закидон на будующую модернизацию магазина
        # for item in range(len(items)/10):
        embed_1 = disnake.Embed(title='Лист магазина №{item}')

    #! Прослушка
    @commands.Cog.listener("on_button_click")
    async def craft_conf(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ['essence_soul_cf', 'shard_soul_cf']:
            return

        # Крафт осколков душ
        # Коэффициент 400 к 1
        if inter.component.custom_id == 'essence_soul_cf':
            # Проверка наличие указаных средств у пользователя
            check = db.Info(user_id=self.user).money()
            if self.value > check[1]:
                embed = disnake.Embed(description='**Недостаточно средств**', color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            shardValue = self.value//400
            # Шанс дропа шардов
            chanceDrop = float('{:.3f}'.format(self.value / (self.value+100)))
            # Не больше 80%
            if chanceDrop > 0.8: chanceDrop = 0.800

            # Создание диапазона выпадающих шардов
            minDrop = int(shardValue * 0.7)
            if minDrop <= 0: minDrop = 1
            maxDrop = int(round(shardValue * 1.3))
            if maxDrop <= 1: maxDrop = 2
            lossEssence = int(self.value*0.8)
            # Сколько будет потеряно в случае неудачи
            if lossEssence <= 10: lossEssence = self.value
            # Рандоминг чисел. Шанса и числа шардов
            randomNum= float('{:.3f}'.format(random.random()))
            ShardDrop = random.randint(minDrop, maxDrop)

            if chanceDrop > randomNum:
                # Позитивный исход
                db.Money(user=self.user, currency='essence', value=self.value).sub()
                db.Money(user=self.user, currency='shard', value=ShardDrop).add()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ [{:.1%}]\n**Вы получили:**ㅤㅤㅤ[{ShardDrop}] осколок(-ов)'.format(chanceDrop, ShardDrop= ShardDrop),
                    color= disnake.Colour.green())
                return await inter.response.edit_message(embed=embed, components=None)
            else:
                # Негативный исход
                db.Money(user=self.user, currency='essence', value=lossEssence).sub()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ [{:.1%}]\n**Вы потеряли (80%):**ㅤ[{lossEssence}] эссенций'.format(chanceDrop, lossEssence= lossEssence),
                    color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
        # Крафт душ
        # Коэффициент 1200 к 1
        elif inter.component.custom_id == 'shard_soul_cf':
            # Проверка наличие указаных средств у пользователя
            check = db.Info(user_id=self.user).money()
            if self.value > check[2]:
                embed = disnake.Embed(description='**Недостаточно средств**', colour= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)
            # Основные преобразования по формуле
            # Число выпадающих шардов
            soulValue = self.value//1200
            # Шанс дропа шардов
            chanceDrop = float('{:.3f}'.format(self.value / (self.value+300)))
            # Не больше 80%
            if chanceDrop > 0.6: chanceDrop = 0.600

            # Создание диапазона выпадающих шардов
            minDrop = int(soulValue * 0.5)
            if minDrop <= 0: minDrop = 1
            maxDrop = int(round(soulValue * 1.8))
            if maxDrop <= 1: maxDrop = 2
            lossShard = int(self.value*0.5)
            # Сколько будет потеряно в случае неудачи
            if lossShard <= 10: lossShard = self.value
            # Рандоминг чисел. Шанса и числа шардов
            randomNum= float('{:.3f}'.format(random.random()))
            soulValue = random.randint(minDrop, maxDrop)

            if chanceDrop > randomNum:
                # Позитивный исход
                db.Money(user=self.user, currency='shard', value=self.value).sub()
                db.Money(user=self.user, currency='soul', value=soulValue).add()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ [{:.1%}]\n**Вы получили:**ㅤㅤㅤㅤ[{soulValue}] душ'.format(chanceDrop, soulValue= soulValue),
                    color= disnake.Colour.green())
                return await inter.response.edit_message(embed=embed, components=None)
            else:
                # Негативный исход
                db.Money(user=self.user, currency='shard', value=lossShard).sub()
                embed = disnake.Embed(
                    description='**Шанс выпадения : **ㅤ [{:.1%}]\n**Вы потеряли (50%):**ㅤ[{lossShard}] осколков'.format(chanceDrop, lossShard= lossShard),
                    color= disnake.Colour.red())
                return await inter.response.edit_message(embed=embed, components=None)

    # formyla = n // (n + 100)
    @commands.command(name='craft', aliases=['crt', 'крафт'])
    async def craft(self, ctx):
        if not ctx.guild is None:
            serverT= [1199488197885968515, 958063150144577558] # Дом поняшки, сервер зарато
            if ctx.guild.id not in serverT:
                return

        self.user = ctx.message.author.id
        db.Check(user_id=self.user).user()

        # Проверка на наличия числового значения
        try:
            self.value = abs(int(ctx.message.content.lower().split(' ')[1]))
        except:
            embed = disnake.Embed(description='**Не указано количество**', color= disnake.Colour.red())
            return await ctx.send(embed=embed)
        
        components = [
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='Осколки', custom_id='essence_soul_cf'),
            disnake.ui.Button(style=disnake.ButtonStyle.secondary, disabled=False, label='Души', custom_id='shard_soul_cf')
            ]
        embed = disnake.Embed(title='Что желаете скрафтить?')

        await ctx.send(embed=embed, components=components)

    @commands.command()
    async def lofi(self):
        pass

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Economycs(bot))
    print(f'Запуск модуля Economy.system')