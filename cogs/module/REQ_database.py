import disnake
from disnake.ext import commands

import sqlite3
import time

con = sqlite3.connect('../bots/_system.db')
conRPG = sqlite3.connect('../bots/_rpg.db')
cur = con.cursor()
curRPG = conRPG.cursor()

class Db(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
# DataBase.Check(user_id=9000).user()

class DataBase:
    class Check:
        # Передать id пользователя
        def __init__(self, user_id = None, user_name:str = None):
            self.user_id= user_id
        def user(self):
            num= 0
            #! Основная таблица юзера в таблицах системы и не РПГ модуле
            cur.execute(f'SELECT * FROM user_ment WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO user_ment VALUES (?, ?, ?)", (self.user_id, 0, 0))
            cur.execute(f'SELECT uid FROM user_wins WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO user_wins VALUES (?, ?, ?, ?)", (self.user_id, 0, 0, 0))
            cur.execute(f'SELECT uid FROM user_wins_max WHERE uid = {self.user_id}')
            if cur.fetchone() is None:
                num+= 1
                cur.execute("INSERT INTO user_wins_max VALUES (?, ?, ?, ?)", (self.user_id, 0, 0, 0))


            #? RPG module
            curRPG.execute(f'SELECT * FROM user_active_inventory WHERE UID = {self.user_id}')
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute("INSERT INTO user_active_inventory VALUES (?, ?, ?, ?, ?, ?)", (self.user_id, 0, 0, 0, 0, 0))
            curRPG.execute(f'SELECT * FROM user_diplomaty WHERE UID = {self.user_id}')
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute("INSERT INTO user_diplomaty VALUES (?,?,?,?,?,?,?,?,?)", (self.user_id,0,0,0,0,0,0,0,0))
            curRPG.execute(f'SELECT * FROM user_equipment WHERE UID = {self.user_id}')
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute("INSERT INTO user_equipment VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (self.user_id,0,0,0,0,0,0,0,0,0,0,0,0,0))
            curRPG.execute(f"SELECT * FROM user_main_info WHERE UID = {self.user_id}")
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute("INSERT INTO user_main_info VALUES (?,?,?,?)", (self.user_id,0,0,0))
            curRPG.execute(f"SELECT * FROM user_money WHERE UID = {self.user_id}")
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute('INSERT INTO user_money VALUES (?,?,?,?,?,?,?,?,?)', (self.user_id,0,0,0,0,0,0,0,0))
            curRPG.execute(f"SELECT * FROM user_parametr WHERE UID = {self.user_id}")
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute('INSERT INTO user_parametr VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (self.user_id,10,5,1,1,1,25,10,0,10,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0))
            curRPG.execute(f'SELECT * FROM user_blocktime WHERE UID = {self.user_id}')
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute('INSERT INTO user_blocktime VALUES (?,?,?,?,?,?)', (self.user_id,0,0,0,0,0))
            curRPG.execute(f'SELECT * FROM user_terms WHERE UID = {self.user_id}')
            if curRPG.fetchone() is None:
                num+=1
                curRPG.execute('INSERT INTO user_terms VALUES (?,?,?,?)', (self.user_id,False,0,True))

            conRPG.commit()
            con.commit()
            if num!= 0:
                print(f'Create new record {self.user_id} / None poss: {num}')
                return False
            return True
        
        def bot(self):
            cur.execute('SELECT * FROM bot')
            if cur.fetchone() is None:
                cur.execute("INSERT INTO bot VALUES (?, ?, ?, ?)", (0, 0, 0, 0))
                con.commit()
                return True
            else:
                return False
            
    class Money:
        # Передать id пользователя по которому и будут совершаться дальнейшие операции
        def __init__(self, *, user: int, currency= 'ESSENCE', value= 0):
            self.user= user
            self.currency= currency
            self.value= value

        # essence, shard, soul, cristall
        def add(self) -> bool:
            if self.currency in ["ESSENCE", "SHARD", "SOUL", "CRISTAL_SOUL", "COU", "VCOIN", "ACOIN", "TCOIN"]:
                curRPG.execute(f'UPDATE user_money SET {self.currency} = {self.currency} + {self.value} WHERE UID = {self.user}')
            else: return False
            
            conRPG.commit()
            return True
        def sub(self) -> bool:
            if self.currency in ["ESSENCE", "SHARD", "SOUL", "CRISTAL_SOUL", "COU", "VCOIN", "ACOIN", "TCOIN"]:
                cur.execute(f'SELECT {self.currency} FROM user_money WHERE UID = {self.user}')
                if curRPG.fetchone()[0] - self.value < 0: 
                    cur.execute(f'UPDATE user_money SET {self.currency} = {self.currency} - {self.value} WHERE UID = {self.user}')
                else: return False
            else: return False

            con.commit()
            return True
        def update(self) -> bool:
            if self.currency in ["ESSENCE", "SHARD", "SOUL", "CRISTAL_SOUL", "COU", "VCOIN", "ACOIN", "TCOIN"]:
                cur.execute(f'UPDATE user_money SET {self.currency} = {self.value} WHERE UID = {self.user_id}')
            else: return False
            con.commit()
            return True
        
        def have(self) -> tuple:
            cur.execute(f'SELECT {self.currency} FROM user_money WHERE UID = {self.user}')
            return cur.fetchone()[0]
        
    class Info:
        def __init__(self, user_id= None):
            self.user_id= user_id
        def takeFromRPG(self, table:str) -> tuple:
            if self.user_id is None:
                curRPG.execute(f'SELECT * FROM {table}')
                return curRPG.fetchall()
            curRPG.execute(f'SELECT * FROM {table} WHERE UID = {self.user_id}')
            return curRPG.fetchone()    
        
        def takeFromSystem(self, table:str) -> tuple:
            if self.user_id is None:
                cur.execute(f'SELECT * FROM {table}')
                return cur.fetchall()
            cur.execute(f'SELECT * FROM {table} WHERE UID = {self.user_id}')
            return cur.fetchone()

        def positionLVL(self, exp:int):
            curRPG.execute(f'SELECT lvl FROM levels WHERE expTotal - {exp} <= 0')
            lvl = curRPG.fetchone()
            if lvl is None:
                return 0
            return lvl[0]
        def user(self):
            cur.execute(f'SELECT * FROM user_ment WHERE uid = {self.user_id}')
            return cur.fetchone()

    class Bot:
        def __init__(self, value=0):
            self.value = value
        
        def lock(self) -> bool:
            cur.execute(f'UPDATE bot SET lock_tmreact = {round(time.time() + self.value)}')
            con.commit()
            return True

        def checkLock(self) -> bool:
            cur.execute(f'SELECT lock_tmreact FROM bot')
            if round(time.time()) > cur.fetchone()[0]: return False
            else: return True
        
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
            def update(self):
                cur.execute(f'UPDATE bot SET {self.column} = {self.value}')
                con.commit()
                return True
            
    class User:
        def __init__(self, column=None, user_id=None, value=0):
            self.user_id = user_id
            self.value = value
            self.column = column

        def setParam(self):
            curRPG.execute(f'UPDATE user_main_info SET {self.column} = {self.value} WHERE UID = {self.user_id}')
            con.commit()
            return True
        
        def upParam(self):
            curRPG.execute(f'UPDATE user_main_info SET {self.column} = {self.column} + {self.value} WHERE UID = {self.user_id}')
            con.commit()
            return True
        
        def downParam(self):
            curRPG.execute(f'UPDATE user_main_info SET {self.column} = {self.column} - {self.value} WHERE UID = {self.user_id}')
            con.commit()
            return True
        
        def lockMent(self):
            times = round(time.time()) + self.value
            cur.execute(f'UPDATE user_ment SET MentTimer = {times} WHERE uid = {self.user_id}')
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
    
    class Exp:
        def __init__(self, user_id:int, value:int) -> None:
            self.user_id = user_id
            self.value = value
        
        def add(self) -> bool:
            curRPG.execute(f'UPDATE user_main_info SET EXP = EXP + {self.value} WHERE UID = {self.user_id}')
            conRPG.commit()
            return True
        def sub(self) -> bool:
            curRPG.execute(f'SELECT EXP FROM user_main_info WHERE UID = {self.user_id}')
            if curRPG.fetchone() - self.value < 0:
                return False
            curRPG.execute(f'UPDATE user_main_info SET EXP = EXP - {self.value} WHERE UID = {self.user_id}')
            conRPG.commit()
            return True
        def update(self) -> bool:
            if self.value < 0:
                return False
            curRPG.execute(f'UPDATE user_main_info SET EXP = {self.value} WHERE UID = {self.user_id}')
            conRPG.commit()
            return True

    class RPG:
        def __init__(self) -> None:
            pass
        def info(self, user_id:int, table:str):
            curRPG.execute(f'SELECT * FROM {table} WHERE UID = {user_id}')
            return curRPG.fetchone()
        
        def changeUser(self, user_id:int, table:str, column:str, value):
            try:
                curRPG.execute(f'UPDATE {table} SET {column} WHERE UID = {user_id}')
                curRPG.commit()
                return True
            except:
                return False

        def addRecord(self, table:str, dict:dict):
            pass
            

    # TODO: Releaze function what can delet record from db. this need for delete data leave user.
    class DeleteData:
        def __init__(self, id:int):
            self.id = id
        
        def delete(self):
            pass

def setup(bot:commands.Bot):
    bot.add_cog(Db(bot))