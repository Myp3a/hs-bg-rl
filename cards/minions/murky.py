from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Murky(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 198
        self.classes = [MinionClass.Murloc]
        self.level = 6
        self.base_attack_value = 6
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.boost_murloc)
        
    def boost_murloc(self):
        available_targets = [c for c in self.army.cards if not self and MinionClass.Murloc in c.classes]
        if not available_targets:
            self.log.debug(f"{self} found no targets")
            return
        target = random.choice(available_targets)
        self.log.debug(f"{self} boosting {target}")
        if self.triplet:
            atk_boost = 20
            hlt_boost = 20
        else:
            atk_boost = 10
            hlt_boost = 10
        if self.in_fight:
            target.attack_temp_boost += atk_boost
            target.health_temp_boost += hlt_boost
        else:
            target.attack_perm_boost += atk_boost
            target.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(target, atk_boost, hlt_boost)
