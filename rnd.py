import os
import random
import logging
from models.game import Game
from models.player import Player
from models.field import Field
from models.tavern import Tavern

loglevel = logging.DEBUG
seed = random.randint(1,10000000)
os.system("cls")
print(seed)
random.seed(seed)
tav = Tavern(loglevel)
g = Game([Player(tav, loglevel) for _ in range(8)], loglevel)
g.run()