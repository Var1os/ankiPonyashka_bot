import disnake
import os
from disnake.ext import commands

bot = commands.Bot(command_prefix='~', 
                   intents=disnake.Intents.all(), 
                   activity= disnake.Activity(name='версия 2.0!', type= disnake.ActivityType.playing),
                   reload=True, 
                   help_command=None)

# Загрузка модулей "Зартао"
bot.load_extension('cogs.zr_economy')
bot.load_extension('cogs.zr_events')
bot.load_extension('cogs.zr_fun')
bot.load_extension('cogs.zr_rpg')
bot.load_extension('cogs.zr_administrator')
bot.load_extension('cogs.zr_until')
bot.load_extension('cogs.zr_message')
bot.load_extension('cogs.zr_emotionalPony')
# Загрузка модулй "Тетра"

token = os.environ["token"]
bot.run(token)