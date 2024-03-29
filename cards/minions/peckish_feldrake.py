from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class PeckishFeldrake(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 120
        self.classes = [MinionClass.Demon, MinionClass.Dragon]
        self.level = 4
        self.base_attack_value = 0
        self.base_health_value = 1
        self.hooks["battlecry"].append(self.eat)

    def eat(self):
        for _ in range(3):
            self.eat_minion()

    def eat_minion(self) -> None:
        if self.in_fight:
            self.log.debug(f"{self} tried to eat mid-fight")
            return
        available_targets = self.army.player.view
        if not available_targets:
            self.log.debug(f"{self} found no targets to eat")
            return
        target = random.choice(available_targets)
        self.log.debug(f"{self} eating {target}")
        card = self.army.player.tavern.buy(target)
        self.army.player.view.remove(card)
        self.contains.append(card)
        if self.triplet:
            atk_boost = card.attack_value * 2
            hlt_boost = card.health_value * 2
        else:
            atk_boost = card.attack_value
            hlt_boost = card.health_value
        self.attack_perm_boost += atk_boost
        self.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(self, atk_boost, hlt_boost)