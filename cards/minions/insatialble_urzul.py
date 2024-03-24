from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class InsatiableUrzul(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 156
        self.classes = [MinionClass.Demon]
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 6
        self.base_taunt = True
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_play")
        self.army.hooks["on_minion_play"].append(self.eat)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_play")
        self.army.hooks["on_minion_play"].remove(self.eat)

    def eat(self, played) -> None:
        if MinionClass.Demon in played.classes:
            available_targets = self.army.player.view
            if not available_targets:
                self.log.debug(f"{self} found no target to eat")
                return
            target = random.choice(available_targets)
            self.log.debug(f"{self} eating {target}")
            card = self.army.player.tavern.buy(target)
            self.contains.append(card)
            self.army.player.view.remove(card)
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
