from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ImpulsiveTrickster(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 39
        self.classes = [MinionClass.Demon]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 3
        self.max_health = self.health_value
        self.hooks["deathrattle"].append(self.boost_health)

    def choose_and_boost_health(self) -> None:
        hlt_boost = self.max_health
        other_minions = [m for m in self.army.cards if not m is self]
        if len(other_minions) > 0:
            chosen = random.choice(other_minions)
            chosen.health_temp_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(chosen, 0, hlt_boost)
        
    def boost_health(self) -> None:
        # TODO: check if boosted ingame health counts
        self.choose_and_boost_health()
        if self.triplet:
            self.choose_and_boost_health()
