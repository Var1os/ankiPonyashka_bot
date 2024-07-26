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
    

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))
    print(f'Запуск модуля Admin.system')