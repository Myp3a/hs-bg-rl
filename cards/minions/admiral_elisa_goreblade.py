from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class AdmiralElisaGoreblade(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 178
        self.classes = [MinionClass.Pirate]
        self.level = 6
        self.base_attack_value = 6
        self.base_health_value = 7
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_attack"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.army.hooks["on_attack"].remove(self.boost_values)

    def boost_values(self, attacker, defender):
        if MinionClass.Pirate in attacker.classes:
            if self.triplet:
                atk_boost = 6
                hlt_boost = 2
            else:
                atk_boost = 3
                hlt_boost = 1
            targets = [m for m in self.army.cards]
            for t in targets:
                t.attack_temp_boost += atk_boost
                t.health_temp_boost += hlt_boost
