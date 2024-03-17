from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class FamishedFelbat(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 187
        self.classes = [MinionClass.Demon]
        self.level = 6
        self.base_attack_value = 8
        self.base_health_value = 5
        self.hooks["on_turn_end"].append(self.demons_eat)

    def demons_eat(self):
        demons = [d for d in self.army.cards if MinionClass.Demon in d.classes]
        random.shuffle(demons)
        for d in demons:
            self.eat_minion(d)

    def eat_minion(self, eater) -> None:
        if eater.in_fight:
            return
        available_targets = self.army.player.view
        if len(available_targets) == 0:
            return
        target = random.choice(available_targets)
        card = self.army.player.tavern.buy(target)
        self.army.player.view.remove(card)
        eater.contains.append(card)
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
