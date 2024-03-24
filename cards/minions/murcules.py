from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Murcules(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 44
        self.classes = [MinionClass.Murloc]
        self.level = 2
        self.base_attack_value = 5
        self.base_health_value = 2
        self.hooks["on_kill"].append(self.boost_hand_values)

    def boost_hand_values(self) -> None:
        available_targets = [t for t in self.army.player.hand.cards if isinstance(t, Minion)]
        if not available_targets:
            self.log.debug(f"{self} found no targets")
            return
        target = random.choice(available_targets)
        self.log.debug(f"{self} boosting {target}")
        target.attack_perm_boost += 2
        target.health_perm_boost += 2
        if self.triplet:
            target.attack_perm_boost += 2
            target.health_perm_boost += 2
