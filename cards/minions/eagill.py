from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Eagill(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 67
        self.classes = [MinionClass.Murloc, MinionClass.Beast]
        self.level = 3
        self.base_attack_value = 7
        self.base_health_value = 1
        self.hooks["battlecry"].append(self.boost_hand_and_minion)

    def boost_hand_and_minion(self) -> None:
        if self.triplet:
            atk_boost = 4
            hlt_boost = 6
        else:
            atk_boost = 2
            hlt_boost = 3
        army_targets = [t for t in self.army.cards if not t is self]
        if len(army_targets) > 0:
            at = random.choice(army_targets)
            at.attack_perm_boost += atk_boost
            at.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(at, atk_boost, hlt_boost)
        hand_targets = [t for t in self.army.player.hand.cards if isinstance(t, Minion)]
        if len(hand_targets) > 0:
            ht = random.choice(hand_targets)
            ht.attack_perm_boost += atk_boost
            ht.health_perm_boost += hlt_boost
