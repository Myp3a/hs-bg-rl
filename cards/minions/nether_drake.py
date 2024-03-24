from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class NetherDrake(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 80
        self.classes = [MinionClass.Dragon]
        self.level = 3
        self.base_attack_value = 2
        self.base_health_value = 4
        self.hooks["on_turn_end"].append(self.boost_dragons)

    def boost_dragons(self):
        targets = [t for t in self.army.cards if MinionClass.Dragon in t.classes and not t is self]
        if self.triplet:
            atk_boost = 2
        else:
            atk_boost = 1
        self.log.debug(f"{self} boosting {len(targets)} dragons")
        for t in targets:
            t.attack_perm_boost += atk_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(t, atk_boost, 0)
