import disnake as dk
from random import *

class Base:
    def __init__(self):

        # Базовые характиристики
        self.HP
        self.ATK
        self.DEF
        self.STR
        self.ULT

        # Типы сопративлений к элементам магии
        self.RES_Fire
        self.RES_Aqua
        self.RES_Wind
        self.RES_Earth


    async def Attack(self):
        pass
    async def Defence(self):
        pass
    async def Evasion(self):
        pass
    async def Resistance(self):
        pass
    