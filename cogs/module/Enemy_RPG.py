import disnake as dk
from random import *

class Base:
    def __init__(self):

        #? Базовые характиристики
        self.HP # Здоровье
        self.ATK # Атака
        self.DEF # Защита
        self.STR # Ловкость
        self.ULT # Сверх-способность
        self.CRIT # Сила критического удара
        self.CRIT_CHANCE # Шанс крит удара
         
        
        #? Характиристики механик
        self.POW_SOUL # Сила души
        self.LUCK # Удача
        self.FLEX # Гибкость
        self.STEALTH # Скрытность
        self.SENCE # Восприятие
        self.VITALITY # Живучесть
        self.INSIGHT # Проницательность
        self.CONTROL # Контроль (магам)
        self.VAMPIRE # Вампиризм


        #? Спорные или просто не понятные пока
        self.GENUS # Родовитость
        self.COUNTER_ATK # Контратака
        self.EVASION # Уклонение


        #? Стихийные атаки
        # Все в процентност соотношении, где 1 = 100%
        self.ATK_Fire # Огонь
        self.ATK_Aqua # Вода
        self.ATK_Wind # Ветер
        self.ATK_Earth # Земля
        # Необычные типы
        self.ATK_Light # Свет
        self.ATK_Dark # Тьма
        self.ATK_TOXIN # Токсин
        self.ATK_HOLY # Святость


        #? Сопративления к магии
        # Все в процентност соотношении, где 1 = 100%
        # Базовые типы
        self.RES_Fire # Огонь
        self.RES_Aqua # Вода
        self.RES_Wind # Ветер
        self.RES_Earth # Земля
        # Необычные типы
        self.RES_Light # Свет
        self.RES_Dark # Тьма
        self.RES_TOXIN # Токсин
        self.RES_HOLY # Святость


    async def Attack_move(self):
        pass
    async def Defence_move(self):
        pass
    async def Evasion_move(self):
        pass
    async def Resistance(self):
        pass
    
    async def Loader(self, ID:int=0):
        # ID = 0 — тестовое существо со всеми параметрами в 1
        # Загрузчик, должен пройти каждый параметр и занести в БД, только то, чем обладает существо
        # Он должен принимать только название / ID монстра, а дальше только возврат объекта существа
        # Загрузчик упростит присваивание атрибутов существу, при наследовании
        pass