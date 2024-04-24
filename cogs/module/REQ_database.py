import sqlite3
import time

con = sqlite3.connect('../bots/database.db')
cur = con.cursor()

# DataBase.Check(user_id=9000).user()

class DataBase:
    class Check:
        # Передать id пользователя
        def __init__(self, user_id = None):
            self.user_id= user_id
        def user(self):
            num= 0
            # Основная таблица юзера
            cur.execute(f'SELECT * FROM user WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)", (self.user_id, 0, 0, 500, 0, 0))
            # Таблица денег
            cur.execute(f'SELECT uid FROM money WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO money VALUES (?, ?, ?, ?, ?)", (self.user_id, 0, 0, 0, 0))
            # РПГ статы
            cur.execute(f'SELECT uid FROM rpg_stat WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO rpg_stat VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.user_id, 10, 1, 1, 1, 0, 50, 5, 1, 1, ''))
            # Динамические победы юзера
            cur.execute(f'SELECT uid FROM user_wins WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO user_wins VALUES (?, ?, ?, ?)", (self.user_id, 0, 0, 0))
            # Блокировки
            cur.execute(f'SELECT uid FROM lock WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO lock VALUES (?, ?, ?, ?)", (self.user_id, 0, 0, 0))
            # Максимальные стрики выигрышей
            cur.execute(f'SELECT uid FROM user_wins_max WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO user_wins_max VALUES (?, ?, ?, ?)", (self.user_id, 0, 0, 0))

            con.commit()
            if num!= 0:
                print(f'Create new record {self.user_id}')
                return False
            return True
        def bot(self):
            checkValue = cur.execute('SELECT * FROM bot')
            if checkValue is None:
                cur.execute("INSERT INTO bot VALUES (?, ?, ?, ?)", (0, 0, 0, 0))
                con.commit()
                return True
            else:
                return False
        def level(self):
            pass
        #! проверка актуальности уровня чувачка  
    class Money:
        # Передать id пользователя по которому и будут совершаться дальнейшие операции
        def __init__(self, *, user: int, currency= 'essence', value= 0):
            self.user= user
            self.currency= currency
            self.value= value

        # essence, shard, soul, cristall
        def add(self):
            if self.currency == 'essence':
                cur.execute(f'UPDATE money SET essence_soul = essence_soul + {self.value} WHERE uid = {self.user}')
            elif self.currency == 'shard':
                cur.execute(f'UPDATE money SET shard_soul = shard_soul + {self.value} WHERE uid = {self.user}')
            elif self.currency == 'soul':
                cur.execute(f'UPDATE money SET soul = soul + {self.value} WHERE uid = {self.user}')
            elif self.currency == 'cristall':
                cur.execute(f'UPDATE money SET cristal_soul = cristal_soul + {self.value} WHERE uid = {self.user}')
            else:
                return False
            con.commit()

        def sub(self):
            if self.currency == 'essence':
                cur.execute(f'SELECT essence_soul FROM money WHERE uid = {self.user}')
                data = cur.fetchone()[0]
                if 0 <= data - self.value:
                    cur.execute(f'UPDATE money SET essence_soul = essence_soul - {self.value} WHERE uid = {self.user}')
                else:
                    return False
            elif self.currency == 'shard':
                cur.execute(f'SELECT shard_soul FROM money WHERE uid = {self.user}')
                data = cur.fetchone()[0]
                if 0 <= data - self.value:
                    cur.execute(f'UPDATE money SET shard_soul = shard_soul - {self.value} WHERE uid = {self.user}')
                else:
                    return False
            elif self.currency == 'soul':
                cur.execute(f'SELECT soul FROM money WHERE uid = {self.user}')
                data = cur.fetchone()[0]
                if 0 <= data - self.value:
                    cur.execute(f'UPDATE money SET soul = soul - {self.value} WHERE uid = {self.user}')
                else:
                    return False
            elif self.currency == 'cristall':
                cur.execute(f'SELECT cristal_soul FROM money WHERE uid = {self.user}')
                data = cur.fetchone()[0]
                if 0 <= data - self.value:
                    cur.execute(f'UPDATE money SET cristal_soul = cristal_soul - {self.value} WHERE uid = {self.user}')
                else:
                    return False
            else:
                return False
            con.commit()
            return True
        
        def update(self):
            if self.currency == 'essence':
                cur.execute(f'UPDATE money SET essence_soul = {self.value} WHERE uid = {self.user_id}')
            elif self.currency == 'shard':
                cur.execute(f'UPDATE money SET shard_soul = {self.value} WHERE uid = {self.user_id}')
            elif self.currency == 'soul':
                cur.execute(f'UPDATE money SET soul = {self.value} WHERE uid = {self.user_id}')
            elif self.currency == 'cristall':
                cur.execute(f'UPDATE money SET cristal_soul = {self.value} WHERE uid = {self.user_id}')
            else:
                return False
            con.commit()
            return True
        
        def have(self):
            cur.execute(f'SELECT {self.currency} FROM money WHERE uid = {self.user}')
            return cur.fetchone()[0]

        def lock(self, *, valueLock= 0, lockLvl= None):
            data = round(time.time() + valueLock)
            if lockLvl == 'low':
                cur.execute(f'UPDATE lock SET soul_tmlock_lvl1 = {data} WHERE uid = {self.user}')
            elif lockLvl == 'half':
                cur.execute(f'UPDATE lock SET soul_tmlock_lvl2 = {data} WHERE uid = {self.user}')
            elif lockLvl == 'high':
                cur.execute(f'UPDATE lock SET soul_tmlock_lvl3 = {data} WHERE uid = {self.user}')
            con.commit()
            return True
        
        def checkTimeLock(self, lockLvl= 'low'):
            if lockLvl == 'low':
                cur.execute(f'SELECT soul_tmlock_lvl1 FROM lock WHERE uid = {self.user}')
                timeLock = cur.fetchone()[0]
                if timeLock < round(time.time()):
                    return True
                elif timeLock is None:
                    return False
                else:
                    return False
            elif lockLvl == 'half':
                cur.execute(f'SELECT soul_tmlock_lvl2 FROM lock WHERE uid = {self.user}')
                timeLock = cur.fetchone()[0]
                if timeLock < round(time.time()):
                    return True
                elif timeLock is None:
                    return False
                else:
                    return False
            elif lockLvl == 'high':
                cur.execute(f'SELECT soul_tmlock_lvl3 FROM lock WHERE uid = {self.user}')
                timeLock = cur.fetchone()[0]
                if timeLock < round(time.time()):
                    return True
                elif timeLock is None:
                    return False
                else:
                    return False
            return False

        def lockTake(self, lockLvl= 'low'):
            if lockLvl == 'low':
                cur.execute(f'SELECT soul_tmlock_lvl1 FROM lock WHERE uid = {self.user}')
                return cur.fetchone()[0]
            elif lockLvl == 'half':
                cur.execute(f'SELECT soul_tmlock_lvl2 FROM lock WHERE uid = {self.user}')
                return cur.fetchone()[0]
            elif lockLvl == 'high':
                cur.execute(f'SELECT soul_tmlock_lvl3 FROM lock WHERE uid = {self.user}')
                return cur.fetchone()[0]
            return False
    class Exp:
        def __init__(self, user: int, value= 0):
            self.user= user
            self.value= value

        def add(self):
            cur.execute(f'UPDATE user SET exp = exp + {self.value} WHERE uid = {self.user}')
            con.commit()
            return True

        def sub(self):
            cur.execute(f'SELECT exp FROM user WHERE uid = {self.user}')
            data = cur.fetchone()[0]
            if 0 <= data - self.value:
                cur.execute(f'UPDATE user SET exp = exp - {self.value} WHERE uid = {self.user}')
            else:
                return False
            con.commit()
            return True
        
        def update(self):
            cur.execute(f'UPDATE user SET exp = {self.value} WHERE uid = {self.user}')
            con.commit()
            return True
    class Info:
        def __init__(self, user_id= None):
            self.user_id= user_id
        
        def user(self):
            cur.execute(f'SELECT * FROM user WHERE uid = {self.user_id}')
            return cur.fetchone()
        
        def system(self):
            cur.execute(f'SELECT * FROM rpg_stat WHERE uid = {self.user_id}')
            return cur.fetchone()
        
        def money(self):
            cur.execute(f'SELECT * FROM money WHERE uid = {self.user_id}')
            return cur.fetchone()
        
        def any_table(self, table: str):
            cur.execute(f'SELECT * FROM {table} WHERE uid = {self.user_id}')
            return cur.fetchone()

        def all(self, table: str):
            cur.execute(f'SELECT * FROM {table}')
            return cur.fetchall()

        def whatIsLvl(self, exp=0):
            cur.execute(f"SELECT max(lvl) FROM levels WHERE expTotal - {exp} <= 0")
            res = cur.fetchone()
            if res[0] is None: 
                return 0
            return res[0]
    class Bot:
        def __init__(self, value=0):
            self.value = value
        
        def lock(self):
            data = round(time.time() + self.value)
            cur.execute(f'UPDATE bot SET lock_tmreact = {data}')
            con.commit()
            return True

        def checkLock(self):
            data = round(time.time())
            cur.execute(f'SELECT lock_tmreact FROM bot')
            if data > cur.fetchone()[0]:
                return False
            else:
                return True
        
        def info(self):
            cur.execute('SELECT * FROM bot')
            return cur.fetchone()
        
        class set:
            def __init__(self, column=None, value=0):
                self.column = column
                self.value = value
            def add(self):
                cur.execute(f'UPDATE bot SET {self.column} = {self.column} + {self.value}')
                con.commit()
                return True
            def sub(self):
                cur.execute(f'UPDATE bot SET {self.column} = {self.column} - {self.value}')
                con.commit()
                return True
            def set(self):
                cur.execute(f'UPDATE bot SET {self.column} = {self.value}')
                con.commit()
                return True
    class User:
        def __init__(self, column=None, user_id=None, value=0):
            self.user_id = user_id
            self.value = value
            self.column = column

        def setParam(self):
            cur.execute(f'UPDATE user SET {self.column} = {self.value} WHERE uid = {self.user_id}')
            con.commit()
            return True
        
        def upParam(self):
            cur.execute(f'UPDATE user SET {self.column} = {self.column} + {self.value} WHERE uid = {self.user_id}')
            con.commit()
            return True
        
        def downParam(self):
            cur.execute(f'UPDATE user SET {self.column} = {self.column} - {self.value} WHERE uid = {self.user_id}')
            con.commit()
            return True
        
        def lockMent(self):
            times = round(time.time()) + self.value
            cur.execute(f'UPDATE user SET MentTimer = {times} WHERE uid = {self.user_id}')
            con.commit()
            return True

    class BotMood:
        def __init__(self, user: int= None):
            self.user = user
        
        # Получение актуальной информации о настроении
        def infoLove(self):
            cur.execute(f'SELECT love_bot FROM user WHERE uid = {self.user}')
            info = cur.fetchone()
            if info is None:
                return False
            return info[0]
        
        def infoMood(self):
            cur.execute(f'SELECT anger FROM bot')
            return cur.fetchone()[0]

        # Взаимодействие с эмоциями
        # Любовь
        def addLove(self, value=0):
            love_now = self.infoLove()
            if love_now + value <= 1000:
                cur.execute(f'UPDATE user SET love_bot = love_bot + {value} WHERE uid = {self.user}')
                con.commit()
                return True
            return False
        
        def subLove(self, value=0):
            love_now = self.infoLove()
            if love_now - value < 0:
                return False
            cur.execute(f'UPDATE user SET love_bot = love_bot - {value} WHERE uid = {self.user}')
            con.commit()
            return True

        def updateLove(self, value=0):
            cur.execute(f'UPDATE user SET love_bot = {value} WHERE uid = {self.user}')
            con.commit()
            return True

        # Настроение
        def addMood(self, value=0):
            mood_info = self.infoMood()
            if mood_info + value <= 1000:
                cur.execute(f'UPDATE bot SET anger = anger + {value}')
                con.commit()
                return True
            return False
        
        def subMood(self, value=0):
            mood_now = self.infoMood()
            if mood_now - value < 0:
                return False
            cur.execute(f'UPDATE bot SET anger = anger - {value}')
            con.commit()
            return True

        def updateMood(self, value=0):
            cur.execute(f'UPDATE bot SET anger = {value}')
            con.commit()
            return True
    class Fun:
        def __init__(self, user: int, strick=None):
            self.user = user
            self.strick = strick
        
        def add(self):
            if self.strick == 'coin':
                cur.execute(f'UPDATE user_wins SET coin_str = coin_str + 1 WHERE uid = {self.user}')
                con.commit()
                return True
            elif self.strick == 'casino':
                cur.execute(f'UPDATE user_wins SET casino_str = casino_str + 1 WHERE uid = {self.user}')
                con.commit()
                return True
            elif self.strick == 'rolete':
                cur.execute(f'UPDATE user_wins SET RusRolete = RusRolete + 1 WHERE uid = {self.user}')
                con.commit()
                return True
            return False
        
        def clear(self):
            if self.strick == 'coin':
                cur.execute(f'UPDATE user_wins SET coin_str = 0 WHERE uid = {self.user}')
                con.commit()
                return True
            elif self.strick == 'casino':
                cur.execute(f'UPDATE user_wins SET casino_str = 0 WHERE uid = {self.user}')
                con.commit()
                return True
            elif self.strick == 'rolete':
                cur.execute(f'UPDATE user_wins SET RusRolete = 0 WHERE uid = {self.user}')
                con.commit()
                return True
            return False
        
        def get(self):
            cur.execute(f'SELECT * FROM user_wins WHERE uid = {self.user}')
            return cur.fetchone()
        
        def maxis(self):
            ls = ('coin_str_max', 'casino_str_max', 'RusRolete_max')

            cur.execute(f'SELECT * FROM user_wins_max WHERE uid = {self.user}')
            max_str = list(cur.fetchone())
            max_str.pop(0)
            cur.execute(f'SELECT * FROM user_wins WHERE uid = {self.user}')
            user_str = list(cur.fetchone())
            user_str.pop(0)

            for i in range(len(max_str)):
                if max_str[i] < user_str[i]:
                    cur.execute(f'UPDATE user_wins_max SET {ls[i]} = {user_str[i]} WHERE uid = {self.user}')
    class Moderation:
        def __init__(self, id: int, value: int= None):
            self.id= id
            self.value= value
        
        def add(self):
            pass
        def sub(self):
            pass
        def set(self):
            pass
        def delete(self):
            pass
        def check(self):
            pass
