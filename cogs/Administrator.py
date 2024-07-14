import disnake
from disnake.ext import commands

from .module import REQ_database as Rdb
import os

db = Rdb.DataBase

class Admin(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
    
    # ? Позже добавить права на эту команду
    @commands.has_permissions(administrator=True) 
    @commands.command(name='addChannel', aliases=['ответы', 'addch'])
    async def addChannel(self, ctx):

        # Открытие файла
        file = open(f'../bots/acesses/{ctx.guild.id}.txt', mode="a+")
        file.seek(0)

        channel = ctx.message.raw_channel_mentions

        n = 0
        if channel:
            for item in channel:
                list_channel = []
                for ent in file:
                    list_channel.append(ent.rstrip())
                sus = True
                if os.stat(f'../bots/acesses/{ctx.guild.id}.txt').st_size == 0:
                    file.writelines(f"{item}\n")
                    continue

                for ent in list_channel:
                    if item == int(ent):
                        sus = False
                if sus:
                    file.writelines(f"{item}\n")
                else:
                    n += 1
            else:
                if n > 0:
                   await ctx.message.channel.send(f"({n}) Некоторые каналы есть в списке. Они были пропущены.")
                else:
                    await ctx.send("Каналы добавлены в список")
        else:
            await ctx.send('Укажите каналы, для добавления')
        file.close()
    
    @commands.command(name='RChannel', aliases=['нуль', 'rc'])
    # ? Позже добавить права на эту команду
    @commands.has_permissions(administrator=True) 
    async def RChannel(self, ctx):

        # Считка параметров файла
        file = open(f'../bots/acesses/{ctx.guild.id}.txt', mode="a+")
        file.seek(0)

        channelList = ''
        for index, item in enumerate(file):
            channelList += f"``<{index+1}>`` <#{item.rstrip()}> \n"

        # Простая проверка на наличие значения
        if channelList == '':
            channelList = '<None>'
        file.close()

        # Реализация Embed панели
        emb = disnake.Embed(title="Доступные для реакций каналы сервера",
                            colour=disnake.Color.green(), description=channelList)
        emb.set_footer(text=f'Вы находитесь в канале {ctx.message.channel}')

        await ctx.message.channel.send(embed=emb)
    
    @commands.command(name='exp')
    @commands.has_permissions(administrator=True)
    async def exp(self, ctx):   

        user = ctx.message.author.id
        content = ctx.message.content
        mentioned = ctx.message.raw_mentions
        simbol = ',.!?'
        # Удаление лишних символов
        for item in simbol:
            content.replace(item, '')
        else:
            content = content.split(' ')
        # проверка на правильность числа для применения
        try:
            count = str(content[1])
            operation = None
            if count.startswith('+'):
                operation = 'plus'
            elif count.startswith('-'):
                operation = 'minus'
            else:
                operation = 'update'
            count = abs(int(content[1]))
        except:
            embed = disnake.Embed(title='Неверное значение', description='~exp ``(value)`` [mentioned]\nㅤㅤㅤㅤㅤ^^^^^^^^')
            embed.set_footer(text='Для установки значения, просто укажите число, для прибавления или убавления добавьте к числу + или -')
            return await ctx.send(embed=embed)

        # Проверка на наличие пингов пользователей
        if not mentioned:
            embed = disnake.Embed(title='Не указан(ы) пользователь(и)',description='~exp (value) ``[mentioned]``\nㅤㅤㅤㅤㅤㅤㅤㅤ^^^^^^^^^^^^')
            return await ctx.send(embed=embed)
        else:
            mentioned = int(mentioned[0])
            if disnake.Guild.get_member(ctx.guild, mentioned).bot:
                return await ctx.send('Не трожте ботов...')
            db.Check(user_id=ctx.message.author.id, user_name=ctx.message.author.name).user

        # Основное тело команды
        if operation == 'plus':
            db.Exp(user=mentioned, value=count).add()
            embed = disnake.Embed(description=f'Количество опыта ``{disnake.Guild.get_member(ctx.guild, user).global_name}`` увеличено на ``+{count}``')
            await ctx.send(embed=embed)
        elif operation == 'minus':
            db.Exp(user=mentioned, value=count).sub()
            embed = disnake.Embed(description=f'Количество опыта ``{disnake.Guild.get_member(ctx.guild, user).global_name}`` уменьшено на ``-{count}``')
            await ctx.send(embed=embed)
        elif operation == 'update':
            db.Exp(user=mentioned, value=count).update()
            embed = disnake.Embed(description=f'Количество опыта ``{disnake.Guild.get_member(ctx.guild, user).global_name}`` установлено на ``{count}``')
            await ctx.send(embed=embed)

    #! Написать команду для изменения денег
    @commands.command(name='m')
    @commands.has_permissions(administrator=True)
    async def money(self, ctx):
        pass
    
    @commands.command(name='mute')
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx):
        pass

    @commands.command(name='unmute')
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx):
        pass

    @commands.command(name='warn')
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx):
        pass

    @commands.command(name='kick')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx):
        pass


# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))
    print(f'Запуск модуля Admin.system')