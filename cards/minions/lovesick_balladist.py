from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class LovesickBalladist(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 113
        self.classes = [MinionClass.Pirate]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.boost_pirate)

    def boost_pirate(self):
        targets = [t for t in self.army.cards if MinionClass.Pirate in t.classes and not t is self]
        if not targets:
            self.log.debug(f"{self} found no pirate to boost")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} boosting {target} by {self.army.player.gold_spent_on_turn} hlt")
        if self.in_fight:
            target.health_temp_boost += self.army.player.gold_spent_on_turn
        else:
            target.health_perm_boost += self.army.player.gold_spent_on_turn
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(target, 0, self.army.player.gold_spent_on_turn)
