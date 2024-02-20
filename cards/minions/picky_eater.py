from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class PickyEater(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 10
        self.classes = [MinionClass.Demon]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 1
        self.hooks["battlecry"].append(self.eat_minion)

    def eat_minion(self) -> None:
        available_targets = self.army.player.view
        if len(available_targets) == 0:
            return
        target = random.choice(available_targets)
        card = self.army.player.tavern.buy(target)
        self.army.player.view.remove(card)
        self.attack_perm_boost += card.attack_value
        self.health_perm_boost += card.health_value
        if self.triplet:
            self.attack_perm_boost += card.attack_value
            self.health_perm_boost += card.health_value