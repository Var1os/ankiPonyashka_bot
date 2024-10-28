from disnake.ext import commands
import disnake

from .module.PGModule import *

# Модуль описывающий команды для ВПИ

class PG(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot


    @commands.command(name='country', aliases=['страна'])
    async def country(self, ctx):
        '''
        Отображение основной информации о государстве в формате фотографии эксель.
        Установить запрет на отображение вне ЛС поняшки, но его можно снять в дополнительных настройках 
        '''

    @commands.command(name='info', aliases=['Инфо'])
    async def info(self, ctx):
        '''
        Команда для осмотра механик, статусов, игровых элементов и так далее. 
        В основе своей просто читает JSON с информацие по частям БПП.
        '''


def setup(bot:commands.Bot):
    bot.add_cog(PG(bot))