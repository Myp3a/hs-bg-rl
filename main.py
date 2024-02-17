from models.player import Player
from models.field import Field

import random
seed = random.randint(1,10000)
print(seed)
random.seed(seed)

p1 = Player()
p2 = Player()

p1.start_turn()
p2.start_turn()
p1.buy(0)
p2.buy(0)
p1.play_minion(0,0)
p2.play_minion(0,0)

p1.end_turn()
p2.end_turn()

print(p1.view)
print(p2.view)

f = Field(p1,p2)
print(f)
f.fight()
print(f)

p1.start_turn()
p2.start_turn()
f = Field(p1,p2)
print(f)
f.fight()
print(f)

print(p2)
print(p1)