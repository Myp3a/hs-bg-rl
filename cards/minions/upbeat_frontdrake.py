from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class UpbeatFrontdrake(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 25
        self.classes = [MinionClass.Dragon]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 1
        self.turns_left = 3
        self.hooks["on_turn_end"].append(self.give_dragon)

    def give_dragon(self) -> None:
        self.turns_left -= 1
        self.log.debug(f"{self} decreased end turn count, new cntr {self.turns_left}")
        if self.turns_left == 0:
            self.turns_left = 3
            dragons = [d for d in self.army.player.tavern.cards 
                       if MinionClass.Dragon in d.classes 
                       and d.level <= self.army.player.level]
            dragon = random.choice(dragons)
            self.log.debug(f"{self} giving {dragon}")
            dragon.army = self.army
            self.army.player.tavern.buy(dragon)
            for hook in dragon.hooks["on_get"]:
                hook()
            self.army.player.hand.add(dragon, len(self.army.player.hand))