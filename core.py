import disnake
from disnake.ext import commands
from tqdm import tqdm

bot = commands.Bot(command_prefix='~', 
                   intents=disnake.Intents.all(), 
                   activity= disnake.Activity(name='fu-fu-fu', type= disnake.ActivityType.playing),
                   reload=True, 
                   help_command=None)
loadRange = ['Economics', 'Message', 'Events', 'Fun', 'Rpg', 'Administrator', 'Until', 'TestingEver', 'module.SystemDialogsRPG', 'module.REQ_database', 'module.SystemCommandRPG', 'module.SystemShop']

index = 0
for _ in tqdm(range(len(loadRange)-1),desc='load module',ncols=75,colour='#666666'):
    bot.load_extension(f'cogs.{loadRange[index]}')
    index+=1

bot.run(open("token.txt", 'r').readline())  