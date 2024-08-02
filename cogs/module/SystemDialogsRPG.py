import disnake
from disnake.ext import commands
from random import randint
import asyncio
import json

from .SystemCommandRPG import *


# ID = 1-1-00001
# open all function for RPG module

class Dialogs(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_button_click')
    async def first_talk_with_player(self, inter:disnake.MessageInteraction, input=0):
        if inter.component.custom_id not in ['talk', 'start_prologe1', 'start_prologe2', 'start_prologe3']:
            return
        if inter.component.custom_id in ['start_prologe1', 'start_prologe2', 'start_prologe3']:
            await inter.response.defer()

        # load dialog for this interact
        with open('../bots/content/dialogs/first_dialog_with_ponyashka.json', encoding='UTF-8') as file:
            scene = json.load(file)
            file.close()
        # Information data about user
        with open(f'../bots/content/dialogs/temporal_dialog/{inter.author.id}.json', encoding='UTF-8') as file:
            temporal_dia = json.load(file)
            file.close()
        


        
        if len(scene) < temporal_dia['phase']:
            await endDialogScene(message=inter.message)
            return
        else: 
            phase, temp = temporal_dia['phase'], temporal_dia['dialog_text']
            phase_text = scene[f'phase{phase}']
            buttons = []
            for index, item in enumerate(phase_text[f'select_{temp}']):
                buttons.append(disnake.ui.Button(style=disnake.ButtonStyle.gray, label=item, custom_id=f'start_prologe{index+1}'))
        await dialogWithoutSelect(tempo=phase_text['tempo'], text=phase_text[f'text_{temp}'], message=inter.message, end_button=buttons)
        
        # check level dialogs for exit
        temporal_dia['dialog_text'] += 1
        if temporal_dia['dialog_text'] > int((len(phase_text)-1)/3):
            temporal_dia['dialog_text'] = 1
            temporal_dia['phase'] += 1
            #! here add close noobe dialog
            
        
        with open(f'../bots/content/dialogs/temporal_dialog/{inter.author.id}.json', 'w', encoding='UTF-8') as file:
            file.write(json.dumps(temporal_dia, indent=3, ensure_ascii=False))
            file.close()


    @commands.Cog.listener()
    async def dialog1_1_00001(message:int, /):
        pass


def setup(bot:commands.Bot):
    loadCog = Dialogs(bot)
    bot.add_cog(loadCog)