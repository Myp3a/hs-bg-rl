from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class PeggySturdybone(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 121
        self.classes = [MinionClass.Pirate]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 2
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_buy"].append(self.boost_attack)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_buy"].remove(self.boost_attack)

    def boost_attack(self, bought):
        # TODO: trigger on new spells and minion acquires
        if self.triplet:
            atk_boost = 2
            hlt_boost = 2
        else:
            atk_boost = 1
            hlt_boost = 1
        targets = [t for t in self.army.cards if MinionClass.Pirate in t.classes and not t is self]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        target.attack_perm_boost += atk_boost
        target.health_perm_boost += hlt_boost
        for hook in self.army.hooks["on_values_change_perm"]:
            hook(target, atk_boost, hlt_boost)
