import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='~', 
                   intents=disnake.Intents.all(), 
                   activity= disnake.Activity(name='версия 2.0!', type= disnake.ActivityType.playing),
                   reload=True, 
                   help_command=None)

# Общие модули поняшки
bot.load_extension('cogs.o_message')

# Загрузка модулей "Зартао"
bot.load_extension('cogs.zr_economy')
bot.load_extension('cogs.zr_events')
bot.load_extension('cogs.zr_fun')
bot.load_extension('cogs.zr_rpg')
bot.load_extension('cogs.zr_administrator')
bot.load_extension('cogs.zr_until')
bot.load_extension('cogs.zr_emotionalPony')

# Загрузка модулй "Тетра"
bot.load_extension('cogs.tr_rpg')

bot.run(open("token.txt", 'r').readline())  