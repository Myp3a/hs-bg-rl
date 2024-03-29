from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class GraveGobbler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 36
        self.classes = [MinionClass.Undead]
        self.level = 2
        self.base_attack_value = 4
        self.base_health_value = 3
        self.hooks["on_turn_start"].append(self.destroy_left)

    def destroy_left(self) -> None:
        pos = self.army.index(self)
        if pos > 0:
            to_the_left: Minion = self.army[pos-1]
            if MinionClass.Undead in to_the_left.classes:
                self.log.debug(f"{self} destroying {to_the_left} at position {pos-1}")
                if to_the_left.rebirth:
                    self.log.debug(f"{self} found rebirth at {to_the_left}, removing")
                    to_the_left.death()
                    to_the_left.feature_overrides["rebirth"].append({"state": False, "one_turn": False})
                else:
                    self.log.debug(f"{self} destroying {to_the_left}")
                    to_the_left.death()
                    for hook in to_the_left.hooks["on_lose"]:
                        hook()
                    self.contains.append(to_the_left)
                if self.triplet:
                    atk_boost = 10
                    hlt_boost = 10
                else:
                    atk_boost = 5
                    hlt_boost = 5
                self.attack_perm_boost += atk_boost
                self.health_perm_boost += hlt_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(self, atk_boost, hlt_boost)
