from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BloodsailCannoneer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 62
        self.classes = [MinionClass.Pirate]
        self.level = 3
        self.base_attack_value = 4
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.boost_pirates)

    def boost_pirates(self) -> None:
        targets = [t for t in self.army.cards if MinionClass.Pirate in t.classes and not t is self]
        self.log.debug(f"{self} boosting {len(targets)} pirates")
        if len(targets) == 0:
            return
        if self.triplet:
            atk_boost = 6
        else:
            atk_boost = 3
        for t in targets:
            if self.in_fight:
                t.attack_temp_boost += atk_boost
            else:
                t.attack_perm_boost += atk_boost
                for hook in self.army.hooks["on_values_change_perm"]:
                    hook(t, atk_boost, 0)
