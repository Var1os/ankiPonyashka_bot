import disnake
from disnake.ext import commands
from random import randint

class RPG(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_button_click')
    async def fight_endMove(self, inter: disnake.MessageInteraction):
        try:
            if inter.component.custom_id not in ['atk', 'def', 'item', 'leave'] or inter.author.id != self.user:
                await inter.response.defer()
                return


            if inter.component.custom_id == 'atk' and not self.win:
                damage_p = randint(3, 7)
                damage_e = randint(self.atk_gob[0], self.atk_gob[1])
                gob_hp = self.hp_gob - damage_p
                player_hp = self.hp_player - damage_e
                if gob_hp <= 0:
                    embed = disnake.Embed(title='Победа!', description='''# Вы оказались сильнее этого гоблина!\n```Получено: 25 эссенций, 2 зуба гоблина```''')
                    self.win = True
                elif player_hp <= 0:
                    embed = disnake.Embed(title='Поражение...', description='''# Гоблин оказался сильнее вашей воли...\n```Штраф: Смерть и ваша анальная девственность```''')
                else:
                    embed = disnake.Embed(title='Перед вами гоблин', description=
f'''# Сражение.

```Вы атаковали гоблина на ({damage_p})```
```Гоблин совершил ататку по вам и нанёс: ({damage_e})```

**Здоровье гоблина:** {self.hp_gob} >>> {gob_hp}
**Атака гоблина:** {self.atk_gob[0]}-{self.atk_gob[1]}

''')
                self.hp_player = player_hp
                self.hp_gob = gob_hp
                embed.set_footer(text=f'💗 Ваше здоровье: {self.hp_player}')
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1206487729995517962/1244870023017664614/gqwaSu0_wRo.jpg?ex=6656af0e&is=66555d8e&hm=29ee0310d6ccb71bc7313b8b528bf14ba67d4b988662afd8187f303a094371b3&')
            
            if inter.component.custom_id == 'leave':
                chance = randint(0, 100)
                if chance >= 85:
                    embed = disnake.Embed(title='')
            await inter.response.edit_message(embed=embed)
        except:
            embed = disnake.Embed(description='Гоблин победил... По техническим причинам!!!')

    @commands.command(name='fight')
    async def fight(self, ctx):
        
        self.user = ctx.message.author.id

        self.hp_gob = randint(50, 100)
        self.atk_gob = [randint(2, 4), randint(4, 7)]
        self.hp_player = randint(80, 120)
        self.win = False


        embed = disnake.Embed(title='Перед вами гоблин', 
            description=
f'''
# Вас атаковал гоблин! 

```Сниф-сниф, блять!```
**Здоровье гоблина:** {self.hp_gob}-HP
**Атака гоблина:** {self.atk_gob[0]}-{self.atk_gob[1]}

'''
).set_thumbnail(
url='https://cdn.discordapp.com/attachments/1206487729995517962/1244870023017664614/gqwaSu0_wRo.jpg?ex=6656af0e&is=66555d8e&hm=29ee0310d6ccb71bc7313b8b528bf14ba67d4b988662afd8187f303a094371b3&'
                )
        embed.set_footer(text=f'💗 Ваше здоровье: {self.hp_player}')


        style = disnake.ButtonStyle
        self.buttons = [
            disnake.ui.Button(style=style.red, label='🗡 Атака', custom_id='atk'),
            disnake.ui.Button(style=style.blurple, label='🚬 Фокусы', custom_id='def'),
            disnake.ui.Button(style=style.green, label='🎒 Предметы', custom_id='item'),
            disnake.ui.Button(style=style.gray, label='🏃‍♀️ Сбежать', custom_id='leave')
            ]

        await ctx.send(embed=embed, components=self.buttons)

# Загрузка кога в основное ядро по команде
def setup(bot:commands.Bot):
    bot.add_cog(RPG(bot))
    print(f'Запуск модуля RPG.system')