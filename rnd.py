from models.game import Game
from models.player import Player
from models.field import Field

import random
seed = random.randint(1,10000)
print(seed)
random.seed(seed)

g = Game([Player() for _ in range(8)])
g.run()