from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MindMuck(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 42
        self.classes = [MinionClass.Demon]
        self.level = 2
        self.base_attack_value = 3
        self.base_health_value = 2
        self.hooks["battlecry"].append(self.other_eat_minion)

    def other_eat_minion(self) -> None:
        # TODO: choose minion who will be eating
        if self.in_fight:
            self.log.debug(f"{self} tried to eat mid-fight")
            return
        available_targets = self.army.player.view
        if not available_targets:
            self.log.debug(f"{self} found no targets to eat")
            return
        available_eaters = [e for e in self.army.cards if MinionClass.Demon in e.classes and not e is self]
        if not available_eaters:
            self.log.debug(f"{self} found no eaters")
            return
        target = random.choice(available_targets)
        eater = random.choice(available_eaters)
        self.log.debug(f"{eater} eating {target}")
        card = self.army.player.tavern.buy(target)
        eater.contains.append(card)
        self.army.player.view.remove(card)
        if self.triplet:
            atk_boost = card.attack_value * 2
            hlt_boost = card.health_value * 2
        else:
            atk_boost = card.attack_value
            hlt_boost = card.health_value
        eater.attack_perm_boost += atk_boost
        eater.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(eater, atk_boost, hlt_boost)
