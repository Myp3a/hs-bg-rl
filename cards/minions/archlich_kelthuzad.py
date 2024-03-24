from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ArchlichKelthuzad(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 179
        self.classes = [MinionClass.Undead]
        self.level = 6
        self.base_attack_value = 10
        self.base_health_value = 8
        self.hooks["on_turn_end"].append(self.destroy_sides)

    def destroy_sides(self):
        if (my_pos := self.army.index(self)) > 0:
            new_minion = self.destroy(my_pos - 1)
            if len(self.army) < 7:
                self.army.add(new_minion, self.army.index(self))
        if self.triplet and (my_pos := self.army.index(self)) < len(self.army) - 1:
            new_minion = self.destroy(my_pos + 1)
            if len(self.army) < 7:
                self.army.add(new_minion, self.army.index(self) + 1)

    def destroy(self, position: int) -> None:
        to_the_side: Minion = self.army[position]
        if MinionClass.Undead in to_the_side.classes:
            self.log.debug(f"{self} destroying {to_the_side} at position {position}")
            t_atk = to_the_side.attack_temp_boost
            t_hlt = to_the_side.health_temp_boost
            features = list(to_the_side.feature_overrides)
            if to_the_side.rebirth:
                self.log.debug(f"{self} found rebirth at {to_the_side}, removing")
                to_the_side.death()
                to_the_side.feature_overrides["rebirth"].append({"state": False, "one_turn": False})
            else:
                self.log.debug(f"{self} destroying {to_the_side}")
                to_the_side.death()
                for hook in to_the_side.hooks["on_lose"]:
                    hook()
                self.contains.append(to_the_side)
            if len(self.army) == 7:
                return
            new_minion = type(to_the_side)(self.army)
            new_minion.attack_perm_boost = to_the_side.attack_perm_boost
            new_minion.health_perm_boost = to_the_side.health_perm_boost
            new_minion.attack_temp_boost = t_atk
            new_minion.health_temp_boost = t_hlt
            new_minion.feature_overrides = features
            self.log.debug(f"{self} spawning {new_minion}")
            for hook in new_minion.hooks["on_get"]:
                hook()
            for hook in new_minion.hooks["on_play"]:
                hook()
            return new_minion