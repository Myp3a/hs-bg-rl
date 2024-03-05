from __future__ import annotations
from typing import TYPE_CHECKING
import random

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SlyRaptor(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 129
        self.classes = [MinionClass.Naga]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 4
        self.windfury = True
        self.divine_shield = True
        self.hooks["deathrattle"].append(self.summon_beast)

    def summon_beast(self, position) -> None:
        beasts = [b for b in self.army.player.tavern.cards if MinionClass.Beast in b.classes]
        if len(beasts) == 0:
            return
        beast = random.choice(beasts)
        new_beast = type(beast)(self.army)
        new_beast.base_attack_value = 7
        new_beast.base_health_value = 7
        self.army.add(new_beast, position)
        for hook in self.army.hooks["on_minion_summon"]:
            hook(new_beast)
