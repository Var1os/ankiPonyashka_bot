import time
import asyncio
import disnake
from cogs import Economy, Events, EmotionalPony

# Это независимый таймер, по аналогии Update() из unity
# Создать интерфейс, что реализует данную возможность
# Использовать низкоуровневую структуру, для быстродействия

class BaseTimer:
    def __init__(self):
        self.active = False

    async def Start(self):
        self.active = True
        loop = asyncio.create_task(self._Loop())
        await loop

    async def Stop(self):
        self.active = False

    async def _Loop(self):
        while self.active:
            pass
    