import disnake
from disnake.ext import commands
from .PokemonModule import setButtonsFightGroup, setButtonsWorkGroup, setDescriptionTextWorkGroup, endSellPokeAfterSelect, giveUserBag, takeFightGroup

# Заглушка для динамической подгрузки
class Cock(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


# Слушающий класс для выбора покемонов из категории боевых групп.
class SelectMassPokemonsViewfightGroup(disnake.ui.View):
    def __init__(self, options:list, user:int):
        super().__init__(timeout=None)
        self.add_item(SelectMassPokemonsMenuFightGroup(options, user))
class SelectMassPokemonsMenuFightGroup(disnake.ui.StringSelect):
    def __init__(self, options:list, user:int):
        self.index = 0
        self.user = user

        super().__init__(
            placeholder=f'Выбрать из {len(options)}',
            min_values=1,
            max_values=1,
            options=options
            )
        
    async def callback(self, inter: disnake.MessageInteraction):
        if self.user != inter.author.id: return

        _, index, hp_atk, rankCOM = inter.data.values[0].split('|')
        ids, seq = rankCOM.split('-')


        userBag = (await giveUserBag(self.user))[ids][seq]
        params = userBag['params']
        pokes = f'### `>>` `{userBag['name']}` `({userBag['other_param']['lvl']}) lvl`\n| Здоровье: `[{params['healpoint']:,}]` `[{params['regen']}/15m]`\n| Атака: `[{params['attack']:,}]`\n| Процент защиты: `[{params['armor']:.0%}]`\n| Шанс уклонения: `[{params['evasion']:.0%}]`\n| Скорость: `[{(1/params['speed']):.0%}]`\n'

        slots = await takeFightGroup(user=self.user)
        text = ''
        for index, item in enumerate(slots):
            if slots[item] is None:
                text += f'### **`{index+1}:` `Пустой слот.`**\n| <None>\n'
            else:
                localRank, localOrde, localNums = slots[item].split('-')
                localUserBag = (await giveUserBag(self.user))[localRank][localOrde][localNums]
                localParams = localUserBag['params']

                text += f'### **`{index+1}:` `{localUserBag['name']}` `({localUserBag['other_param']['lvl']}) lvl`**\n| Здоровье: `[{localParams['healpoint']:,}]` `[{localParams['regen']}/15m]`\n| Атака: `[{localParams['attack']:,}]`\n| Процент защиты: `[{localParams['armor']:.0%}]`\n| Шанс уклонения: `[{localParams['evasion']:.0%}]`\n| Скорость: `[{(1/localParams['speed']):.0%}]`\n'

        embed = disnake.Embed(description=f'```Выбранный покемон:``` {pokes}\n```Слоты```\n{text}')

        await inter.response.edit_message(embed=embed, view=None)
        await setButtonsFightGroup(message=inter.message, data=(rankCOM, self.user))

# Слушатель для команды работы покемонов 
class SelectMassPokemonsViewWorkGroup(disnake.ui.View):
    def __init__(self, options:list, user:int):
        super().__init__(timeout=None)
        self.add_item(SelectMassPokemonsMenuWorkGroup(options, user))
class SelectMassPokemonsMenuWorkGroup(disnake.ui.StringSelect):
    def __init__(self, options:list, user:int):
        self.index = 0
        self.user = user

        super().__init__(
            placeholder=f'Выбрать из {len(options)}',
            min_values=1,
            max_values=1,
            options=options
            )
        
    async def callback(self, inter: disnake.MessageInteraction):
        if self.user != inter.author.id: return

        _, index, hp_atk, rankCOM = inter.data.values[0].split('|')
        text = await setDescriptionTextWorkGroup(user=inter.author.id)

        embed = disnake.Embed(
            title='На какой из 3-х слотов вы желаете его поставить?',
            description=text,
            colour=disnake.Colour.fuchsia()
            )

        await inter.response.edit_message(embed=embed, view=None)
        await setButtonsWorkGroup(message=inter.message, rare=rankCOM, user=inter.author.id)
        
# Слушатель для продажи одного покемона
class SelectMassPokemonsViewCorrectSell(disnake.ui.View):
    def __init__(self, options:list, user:int):
        super().__init__(timeout=None)
        self.add_item(SelectMassPokemonsMenuCorrectSell(options, user))
class SelectMassPokemonsMenuCorrectSell(disnake.ui.StringSelect):
    def __init__(self, options:list, user:int):
        self.index = 0
        self.user = user

        super().__init__(
            placeholder=f'Выбрать из {len(options)-1}',
            min_values=1,
            max_values=1,
            options=options
            )
        
    async def callback(self, inter: disnake.MessageInteraction):
        if self.user != inter.author.id: return

        command, index, rankCOM, price = inter.data.values[0].split('|')

        if command == 'cannelSell':
            embed = disnake.Embed(description='**Процесс продажи был отменен.**')
            await inter.response.edit_message(embed=embed, view=None)
            return
        else:
            
            await inter.response.edit_message(view=None)
            await endSellPokeAfterSelect(pokemon_ids=rankCOM, user=self.user, message=inter.message)

# Слушатель для трейдов между игроками
class SelectMassPokemonsViewSelectPoke(disnake.ui.View):
    def __init__(self, options:list, user:int):
        super().__init__(timeout=None)
        self.add_item(SelectMassPokemonsMenuSelectPoke(options, user))
class SelectMassPokemonsMenuSelectPoke(disnake.ui.StringSelect):
    def __init__(self, options:list, user:int):
        self.index = 0
        self.user = user

        super().__init__(
            placeholder=f'Выбрать из {len(options)-1}',
            min_values=1,
            max_values=1,
            options=options
            )
        
    async def callback(self, inter: disnake.MessageInteraction):
        if self.user != inter.author.id: return

        command, index, rankCOM, price = inter.data.values[0].split('|')

        if command == 'cannelSell':
            embed = disnake.Embed(description='**Процесс продажи был отменен.**')
            await inter.response.edit_message(embed=embed, view=None)
            return
        else:
            
            await inter.response.edit_message(view=None)
            await endSellPokeAfterSelect(pokemon_ids=rankCOM, user=self.user, message=inter.message)
 







# unstatic load module, it`s just for simplicity
def setup(bot:commands.Bot):
    bot.add_cog(Cock(bot))