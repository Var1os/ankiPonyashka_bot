from disnake.ext import commands
import disnake

# Модуль описывающий команды для ВПИ

class DATABASE:
    def __init__(self) -> None:
        pass


class StepFunc:
    def __init__(self) -> None:
        pass





class PGModule(commands.Cog):
    def __init__(self, bot=commands.Bot):
        self.bot = bot
def setup(bot:commands.Bot):
    bot.add_cog(PGModule(bot))