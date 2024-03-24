from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class HungeringAbomination(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 154
        self.classes = [MinionClass.Undead]
        self.level = 5
        self.base_attack_value = 3
        self.base_health_value = 4
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_death")
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_death")
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if self.health_value > 0:
            if not died is self:
                self.log.debug(f"{self} getting boost")
                if self.triplet:
                    atk_boost = 2
                    hlt_boost = 2
                else:
                    atk_boost = 1
                    hlt_boost = 1
                self.attack_perm_boost += atk_boost
                self.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(self, atk_boost, hlt_boost)
