import disnake
from disnake.ext import commands
from .module import REQ_database as Rdb

db = Rdb.DataBase

class Events(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
    
    # Preparation start
    @commands.Cog.listener()
    async def on_ready(self):
        pass
        # await self.bot.get_channel(1205649033125830706).send(f'Запуск номер ``{data[2]}``')
    
    @commands.Cog.listener('on_ready')
    async def on_ready_end(self):
        db.Bot.set(column='dies', value=1).add()
        data = db.Bot().info()
        print(f'| Numbers start >>> {data[2]}')
        print('_'*60)

    '''
    # Обработчик ошибок
    # ! Добавить кастомные варианты ошибок и ответов
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, у вас недостаточно прав для этой команды")
        elif isinstance(error, commands.CommandNotFound):
            print(f"Вызвана неизвестная мне команда: {error}")
        else:
            print(error)'''
    

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(Events(bot))