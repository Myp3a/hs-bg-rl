from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class WrathWeaver(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 26
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 4
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_play"].append(self.boost_values)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_play"].remove(self.boost_values)

    def boost_values(self, played: Minion) -> None:
        if MinionClass.Demon in played.classes:
            self.army.player.health -= 1
            self.attack_value += 2
            self.health_value += 1
            if self.triplet:
                self.attack_value += 2
                self.health_value += 1
