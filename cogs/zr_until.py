from .module import RequestDataBase as Rdb

import disnake
from disnake.ext import commands
import asyncio
import discord
import time

db = Rdb.DataBase
# Основное тело селектора
# тело самой команды, что вызывает данный селектор на 63 строке
class DropDownMenu(disnake.ui.StringSelect):
    def __init__(self, map:map, user:int):
        self.index = 0
        self.map = map
        self.user= user

        options = [
            disnake.SelectOption(label='Опыт', description='Сортировка по свободному опыту'),
            disnake.SelectOption(label='Валюта', description='Сортировка по валюте [1sl = 3200es, 1sh = 400es]'),
            disnake.SelectOption(label='Аркады', description='Сортировка по самому большому винстрику'),
            disnake.SelectOption(label='Характиристикам', description='Топ 1, по каждой характиристике')
            ]
        super().__init__(
            placeholder='Сортировка по...',
            min_values=1,
            max_values=1,
            options=options,
            )
        
        if map is None:
            raise 'Not have map: [components] [embed]'
        
        
    async def callback(self, inter: disnake.MessageInteraction):
        if self.user != inter.author.id:
            await inter.response.send_message('Не вы вызвали таблицу', ephemeral=True)
        if self.values[0] == 'Опыт':
            embed= self.map[0]
        elif self.values[0] == 'Валюта':
            embed= self.map[1]
        elif self.values[0] == 'Аркады':
            embed= self.map[2]
        elif self.values[0] == 'Характиристикам':
            embed= self.map[3]
        else:
            await inter.response.send_message('error?')
        await inter.response.edit_message(embed=embed)
    
# Прослушиватель выбора
class DropDownView(disnake.ui.View):
    def __init__(self, map: map, user:int):
        self.map= map
        self.user= user
        super().__init__(timeout=25.0)
        self.add_item(DropDownMenu(self.map, self.user))

class Until(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
    
    @commands.command(name='leaders', aliases=['lead', 'лидеры', 'топ', 'лид'])
    async def leaders(self, ctx):

        user = ctx.message.author.id
        usersE = db.Info().all('user')
        usersM = db.Info().all('money')
        usersW = db.Info().all('user_wins_max')
        
        # !Создание списка топ 10 участников по опыту-уровню
        # Занесение в список всех заригистрированных участников
        topListE = {}
        for index, item in enumerate(usersE):
            topListE[item[0]] = [item[2], item[1]]
        # Сортировка занесенных в список участников
        sortTopListE = sorted(topListE.items(), key= lambda items: items[1], reverse=True)
        # Поиск места в топе автора вызова лидерборда
        callAuthorE = None
        for index, item in enumerate(sortTopListE):
            if user == int(item[0]):
                callAuthorE = index+1
        # Создание списка для вывода
        EmbedText = ''
        for index, item in enumerate(sortTopListE):
            EmbedText += f'**``{index + 1}``** <@{item[0]}>\n|ㅤ**Уровень: {item[1][1]}**\n|ㅤ**опыт: {item[1][0]}**\n'
            if index == 9:
                break
        # Плашка с итоговой информацией 
        embed_exp = disnake.Embed(
            title='**Топ лидеров по опыту** 🏆', 
            description=EmbedText
            )
        if not ctx.guild is None:
            embed_exp.set_thumbnail(url=ctx.guild.icon)
            embed_exp.set_footer(
                text=f'Вы находитесь на {callAuthorE} месте по опыту', 
                icon_url=ctx.message.author.avatar)
        

        # !Создание списка топ 10 участников по валюте
        topListM = {}
        for index, item in enumerate(usersM):
            summ = item[1] + item[2]*400 + item[3]*3200 + item[4]*6400
            topListM[item[0]] = [summ, item[1], item[2], item[3], item[4]]
        # Сортировка занесенных в список участников
        sortTopListM = sorted(topListM.items(), key= lambda items: items[1], reverse=True)
        # Поиск места в топе автора вызова лидерборда
        callAuthorM = None
        for index, item in enumerate(sortTopListM):
            if user == int(item[0]):
                callAuthorM = index+1
        # Создание списка для вывода
        EmbedText = ''
        for index, item in enumerate(sortTopListM):
            EmbedText += f'**``{index + 1}``** <@{item[0]}>\n|ㅤ**Всего валюты:** **``{item[1][0]}``**\n|ㅤ[{item[1][1]}es] [{item[1][2]}sh] [{item[1][3]}sl] [{item[1][4]}cr]\n'
            if index == 9:
                break
        # Плашка с итоговой информацией 
        embed_money = disnake.Embed(
            title='**Топ лидеров по валюте** 💲', 
            description=EmbedText
            )
        if not ctx.guild is None:
            embed_money.set_thumbnail(url=ctx.guild.icon)
            embed_money.set_footer(
                text=f'Вы находитесь на {callAuthorM} месте по валюте', 
                icon_url=ctx.message.author.avatar)
        

        # !Создание списка топ 10 участников по винстрикам
        # Занесение в список всех заригистрированных участников
        topListW = {}
        for index, item in enumerate(usersW):
            summ = item[1] + item[2] + item[3]
            topListW[item[0]] = [item[1], item[2], item[3], summ]
        # Сортировка занесенных в список участников
        sortTopListW = sorted(topListW.items(), key= lambda items: items[1], reverse=True)
        # Поиск места в топе автора вызова лидерборда
        callAuthorW = None
        for index, item in enumerate(sortTopListW):
            if user == int(item[0]):
                callAuthorW = index+1
        # Создание списка для вывода
        EmbedText = ''
        for index, item in enumerate(sortTopListW):
            EmbedText += f'**``{index + 1}``** <@{item[0]}>\n|ㅤ**Стриков:** **``{item[1][3]}``**\n|ㅤ[{item[1][0]}сn] [{item[1][1]}cs] [{item[1][2]}rr]\n'
            if index == 9:
                break
        # Плашка с итоговой информацией 
        embed_win = disnake.Embed(
            title='**Топ лидеров по винстрикам** 💀', 
            description=EmbedText
            )
        if not ctx.guild is None:
            embed_win.set_thumbnail(url=ctx.guild.icon)
            embed_win.set_footer(
                text=f'Вы находитесь на {callAuthorW} месте по винстрикам', 
                icon_url=ctx.message.author.avatar)
        
        # !Создание списка топ 1, 10 топов по характиристика РПГ
        # 1. Здоровье(ХП) + Стойкость(DR)
        # 2. Атака(ATK) + Защита(DEF)
        # 3. Выносливость(ST)
        # 4. Крит. урон(CrM) + Крит. шанс(CrC)
        # 5. Сила души(SS)
        # 6. Удача(Luck)

        callAuthorRPG = None
        embed_rpg = disnake.Embed(
            title='**Топ по характиристикам** ', 
            description='В разработке~')
        if not ctx.guild is None:
            embed_rpg.set_thumbnail(url=ctx.guild.icon)
            embed_rpg.set_footer(
                text=f'Вы находитесь на {callAuthorRPG} месте по характиристикам', 
                icon_url=ctx.message.author.avatar)
        
        # Список таблиц
        maps = [embed_exp, embed_money, embed_win, embed_rpg]
        view = DropDownView(map=maps, user=user)
        await ctx.send(embed=embed_exp, view=view)


    @commands.command(name='wait')
    async def wait(self, ctx):

        bot = self.bot
        channel = ctx.message.channel
        user = ctx.message.author.id
        await ctx.send('Enter Command! (hello, sex)')
        
        self.text = '?'
        def checker(m):
            if m.content == 'hello' and m.channel == channel and m.author.id == user:
                self.text = 'Boop'
                return True
            elif m.content == 'sex' and m.channel == channel and m.author.id == user:
                self.text = 'Nope.'
                return True
            else:
                return False
            
        msg = await bot.wait_for('message', check=checker, timeout=15.0)
        if msg:
            await channel.send(self.text)
    
    #! Таймер
    class Timer:
        def __init__(self, ctx, times, message, bot):
            self.ctx= ctx
            self.time= times
            self.message= message
            self.bot= bot
        async def start(self):
            while self.time > 0:
                await asyncio.sleep(1)
                self.time-= 1
                embed = disnake.Embed(title=f'{self.time} секунд')
                await self.message.edit(embed=embed)
            else:
                embed= disnake.Embed(title='Таймер закончил счет')
                await self.message.edit(embed=embed)
                await self.bot.get_channel(self.message.channel.id).send(f'<@{self.ctx.message.author.id}>')

    @commands.command()
    async def test(self, ctx):

        timeValue= 30
        try:
            timeValue= int(ctx.message.content.split(' ')[1])
        except:
            embed= disnake.Embed(description='Указано не корректное значение')
            return await ctx.send(embed=embed)
        if timeValue > 180:
            return await ctx.send('Пока не больше 3-х минут')
        embed= disnake.Embed(title=f'{timeValue} секунд')
        self.user= ctx.message.author.id
        message = await ctx.send(embed=embed)

        await self.Timer(ctx= ctx, times=timeValue, message=message, bot= self.bot).start()

    #! голосовалка
    @commands.Cog.listener('on_button_click')
    async def test2_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ['accpt', 'cannel']:
            return
        if inter.author.id in self.say:
            await inter.response.send_message('Вы уже проголосовали', ephemeral=True)
            return
        if inter.author.id not in self.ment:
            await inter.response.send_message('Вы не можете участвовать в данном опросе', ephemeral=True)
            return
        
        if inter.component.custom_id == 'accpt':
            self.index_acpt+= 1
            self.say.append(inter.author.id)
            self.ment.remove(inter.author.id)
            embed= disnake.Embed(title='Голосование', description=f'за: {self.index_acpt}\nпротив: {self.index_cann}')
        elif inter.component.custom_id == 'cannel':
            self.index_cann+= 1
            self.say.append(inter.author.id)
            self.ment.remove(inter.author.id)
            embed= disnake.Embed(title='Голосование', description=f'за: {self.index_acpt}\nпротив: {self.index_cann}')
        if not self.ment:
            embed= disnake.Embed(title='Голосование', description=f'за: {self.index_acpt}\nпротив: {self.index_cann}')
            await inter.response.edit_message(embed=embed, components=None)
        await inter.response.edit_message(embed=embed)

        

    @commands.command()
    async def test2(self, ctx):

        self.ment= ctx.message.raw_mentions
        self.index_acpt= 0
        self.index_cann= 0
        self.say= []

        buttons= [
            disnake.ui.Button(style=disnake.ButtonStyle.green, label='Принять', custom_id='accpt'),
            disnake.ui.Button(style=disnake.ButtonStyle.danger, label='Отклонить', custom_id='cannel')
            ]
        
        embed= disnake.Embed(title='Голосование', description=f'за: {self.index_acpt}\nпротив: {self.index_cann}')
        await ctx.send(embed=embed, components= buttons)

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Until(bot))
    print(f'Запуск модуля Until.system')