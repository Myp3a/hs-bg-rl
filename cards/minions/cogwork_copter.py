from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class CogworkCopter(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 30
        self.classes = [MinionClass.Mech]
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 1
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_divine_shield_lost"].append(self.boost_hand_values)

    def remove_hook(self) -> None:
        self.army.hooks["on_divine_shield_lost"].remove(self.boost_hand_values)

    def boost_hand_values(self, lost) -> None:
        hand_minions = [m for m in self.army.player.hand if isinstance(m, Minion)]
        if len(hand_minions) > 0:
            rnd = random.choice(hand_minions)
            rnd.attack_perm_boost += 1
            rnd.health_perm_boost += 1
            if self.triplet:
                rnd.attack_perm_boost += 1
                rnd.health_perm_boost += 1