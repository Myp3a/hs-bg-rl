from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class TheGladIator(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 91
        self.classes = [MinionClass.Naga]
        self.level = 3
        self.base_attack_value = 1
        self.base_health_value = 1
        self.base_divine_shield = True
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_spell_cast")
        self.army.hooks["on_spell_cast"].append(self.boost_attack)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_spell_cast")
        self.army.hooks["on_spell_cast"].remove(self.boost_attack)

    def boost_attack(self, casted, target):
        self.log.debug(f"{self} found casted spell, boosting self")
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        self.attack_perm_boost += atk_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(self, atk_boost, 0)
