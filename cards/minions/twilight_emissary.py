from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TwilightEmissary(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 57
        self.classes = [MinionClass.Dragon]
        self.level = 2
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_dragon)

    def boost_dragon(self) -> None:
        targets = [c for c in self.army.cards if not c is self and MinionClass.Dragon in c.classes]
        if len(targets) == 0:
            return
        dragon = random.choice(targets)
        if self.triplet:
            atk_boost = 4
            hlt_boost = 4
        else:
            atk_boost = 2
            hlt_boost = 2
        if self.in_fight:
            dragon.attack_temp_boost += atk_boost
            dragon.health_temp_boost += hlt_boost
        else:
            dragon.attack_perm_boost += atk_boost
            dragon.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(dragon, atk_boost, hlt_boost)
