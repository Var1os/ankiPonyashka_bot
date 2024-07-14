import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix='~', 
                   intents=disnake.Intents.all(), 
                   activity= disnake.Activity(name='fu-fu-fu', type= disnake.ActivityType.playing),
                   reload=True, 
                   help_command=None)

bot.load_extension('cogs.Message')
bot.load_extension('cogs.Economy')
bot.load_extension('cogs.Events')
bot.load_extension('cogs.Fun')
bot.load_extension('cogs.Rpg')
bot.load_extension('cogs.Administrator')
bot.load_extension('cogs.Until')
bot.load_extension('cogs.EmotionalPony')
bot.load_extension('cogs.TestingEver')

bot.run(open("token.txt", 'r').readline())  