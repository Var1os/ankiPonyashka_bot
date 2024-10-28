from ..base import Base
import json

with open('../PonyashkaDiscord/content/fight/enemy_content/eventEnemy.json') as file:
    assets = json.load(file)