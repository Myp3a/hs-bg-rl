from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class ToughTusk(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 56
        self.classes = [MinionClass.Quilboar]
        self.level = 2
        self.base_attack_value = 5
        self.base_health_value = 3
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.add_divine_shield)

    def remove_hook(self) -> None:
        self.army.hooks["on_spell_cast"].remove(self.add_divine_shield)

    def add_divine_shield(self, casted, target) -> None:
        if target is self:
            if isinstance(casted, BloodGem):
                self.feature_overrides["shield"].append({"state": True, "one_turn": not self.triplet})
