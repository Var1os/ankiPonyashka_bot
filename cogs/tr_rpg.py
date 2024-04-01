import disnake
from disnake.ext import commands

from .module import RequestDataBaseTetra as Rdb

# Основное тело ядра
class RPG_system(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.command(name='tstat')
    async def tstat(self, ctx):
        # Обязательная структура для разделения систем поняшки и тетры
        if not ctx.guild is None:
            serverT= [1199488197885968515, 1155195910402351254] # Дом поняшки, сервер тетра
            if ctx.guild.id not in serverT:
                return

        head= ['slot1', 'slot2', 'slot3']
        body= ['slot1', 'slot2', 'slot3']
        belt= ['slot1', 'slot2', 'slot3']
        bag= ['slot1', 'slot2', 'slot3']


        embed = disnake.Embed(title='Профиль', description=f'Голова: {head}\nТело: {body}\nПояс: {belt}\nРюкзак: {bag}')
        embed.set_thumbnail(ctx.message.author.avatar)

        await ctx.send(embed=embed)

# Загрузка модуля в ядро
def setup(bot:commands.Bot):
    bot.add_cog(RPG_system(bot))
    print('Модуль TETRA.RPG_system загружен')