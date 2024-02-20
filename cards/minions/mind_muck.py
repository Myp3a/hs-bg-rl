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
        available_targets = self.army.player.view
        if len(available_targets) == 0:
            return
        available_eaters = [e for e in self.army.cards if MinionClass.Demon in e.classes and not e is self]
        if len(available_eaters) == 0:
            return
        target = random.choice(available_targets)
        eater = random.choice(available_eaters)
        card = self.army.player.tavern.buy(target)
        self.army.player.view.remove(card)
        eater.attack_perm_boost += card.attack_value
        eater.health_perm_boost += card.health_value
        if self.triplet:
            eater.attack_perm_boost += card.attack_value
            eater.health_perm_boost += card.health_value
