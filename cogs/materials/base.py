from random import randint

class Base:
    const = 0
    def __init__(self):
        Base.const += 1
        self.id = randint(0, 255)

        #? Базовые характиристики
        self.HP = 10 # Здоровье
        self.ATK = 5 # Атака
        self.DEF = 1 # Защита
        self.STR = 1 # Ловкость
        self.REGEN = 0.5 # Регенерация
        self.CRIT = 0 # (%)Сила критического удара
        self.CRIT_CHANCE = 0 # (%)Шанс крит удара
         
        #? Характиристики механик
        self.LUCK = 0 # Удача (Множит проценты и шанс хорошего события)
        self.UNLUCK = 0 # Неудача (Шанс плохого события, в каждом ходу)
        self.POW_SOUL = 1 # Сила души
        self.FLEX = 0 # Гибкость
        self.STEALTH = 0 # Скрытность
        self.SENCE = 0 # Восприятие
        self.VITALITY = 1 # Живучесть
        self.INSIGHT = 0 # Проницательность
        self.CONTROL = 0 # (%)Контроль (магам)
        self.VAMPIRE = 0 # (%)Вампиризм

        self.CHANCE_STUN = 0 # Шанс оглушение
        self.RES_STUN = 0 # (%)Защиты от оглушения
        self.CHANCE_UPDROP = 0 # (%)Шансы на более качественный дроп и на количество
        self.DOUBLE_CHANCE = 0 # (%)Шансы на удвоение дропа с моба
        self.EXPBOOST = 0 # (%)Повышение количества опыта
        self.MINENEMY = 1 # Минимальное количество противников
        self.MAXENEMY = 5 # Максимальное количество противников, но не >10
        self.DURATION = 1 # (Ход)Продолжительность статусных эффектов
        self.POWER_EFFECT = 1 # (%)Сила статусных эффектов

        #? Спорные или просто не понятные пока
        self.GENUS = 0 # Родовитость
        self.COUNTER_ATK = 0.05 # (%)Контратака шанс
        self.EVASION = 0.05 # (%)Уклонение


        #? Стихийные атаки
        # Все в процентност соотношении, где 1 = 100%
        self.ATK_FIRE = 0 # Огонь
        self.ATK_AQUA = 0 # Вода
        self.ATK_WIND = 0 # Ветер
        self.ATK_EARTH = 0 # Земля
        # Необычные типы
        self.ATK_LIGHT = 0 # Свет
        self.ATK_DARK = 0 # Тьма
        self.ATK_TOXIN = 0 # Токсин
        self.ATK_HOLY = 0 # Святость

        #? Сопративления к магии
        # Все в процентност соотношении, где 1 = 100%
        # Базовые типы
        self.RES_FIRE = 0 # Огонь
        self.RES_AQUA = 0 # Вода
        self.RES_WIND = 0 # Ветер
        self.RES_EARTH = 0 # Земля
        # Необычные типы
        self.RES_LIGHT = 0 # Свет
        self.RES_DARK = 0 # Тьма
        self.RES_TOXIN = 0 # Токсин
        self.RES_HOLY = 0 # Святость

    def __str__(self) -> str:
        return f'Объект класса, id={self.id}, const={Base.const}'
    # def __getstate__(self) -> dict:
    #     param = {
    #         "HP" : self.HP,
    #         "ATK" : self.ATK,
    #         "DEF" : self.DEF,
    #         "STR" : self.STR,
    #         "REGEN" : self.REGEN,
    #         "CRIT" : self.CRIT,
    #         "CRIT_CHANCE" : self.CRIT_CHANCE,
    #         "LUCK" : self.LUCK,
    #         "UNLUCK" : self.UNLUCK,
    #         "POW_SOUL" : self.POW_SOUL,
    #         "FLEX" : self.FLEX,
    #         "STEALTH" : self.STEALTH,
    #         "SENCE" : self.SENCE,
    #         "VITALITY" : self.VITALITY,
    #         "INSIGHT" : self.INSIGHT,
    #         "CONTROL" : self.CONTROL,
    #         "VAMPIRE" : self.VAMPIRE,
    #         "CHANCE_STUN" : self.CHANCE_STUN,
    #         "RES_STUN" : self.RES_STUN,
    #         "CHANCE_UPDROP" : self.CHANCE_UPDROP,
    #         "DOUBLE_CHANCE" : self.DOUBLE_CHANCE,
    #         "EXPBOOST" : self.EXPBOOST,
    #         "MINENEMY" : self.MINENEMY,
    #         "MAXENEMY" : self.MAXENEMY,
    #         "DURATION" : self.DURATION,
    #         "POWER_EFFECT" : self.POWER_EFFECT, 
    #         "GENUS" : self.GENUS,
    #         "COUNTER_ATK" : self.COUNTER_ATK,
    #         "EVASION" : self.EVASION,
    #         "ATK_FIRE" : self.ATK_FIRE,
    #         "ATK_AQUA" : self.ATK_AQUA,
    #         "ATK_WIND" : self.ATK_WIND,
    #         "ATK_EARTH" : self.ATK_EARTH,
    #         "ATK_LIGHT" : self.ATK_LIGHT,
    #         "ATK_DARK" : self.ATK_DARK,
    #         "ATK_TOXIN" : self.ATK_TOXIN,
    #         "ATK_HOLY" : self.ATK_HOLY,
    #         "RES_FIRE" : self.RES_FIRE,
    #         "RES_AQUA" : self.RES_AQUA,
    #         "RES_WIND" : self.RES_WIND,
    #         "RES_EARTH" : self.RES_EARTH,
    #         "RES_LIGHT" : self.RES_LIGHT,
    #         "RES_DARK" : self.RES_DARK,
    #         "RES_TOXIN" : self.RES_TOXIN,
    #         "RES_HOLY" : self.RES_HOLY
    #     }
    #     return param
    def __del__(self):
        Base.const -= 1
        del self


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

    async def sub(self, param, value):
        pass
    async def add(self, param, value):
        pass
    async def update(self, param, value):
        pass