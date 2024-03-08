from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class AmberGuardian(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 61
        self.classes = [MinionClass.Dragon]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 2
        self.hooks["on_fight_start"].append(self.boost_dragon)

    def select_and_boost(self) -> None:
        targets = [t for t in self.army.cards if MinionClass.Dragon in t.classes and not t is self]
        if len(targets) == 0:
            return
        target = random.choice(targets)
        atk_boost = 2
        hlt_boost = 2
        if not target.divine_shield:
            target.feature_overrides["shield"].append({"state": True, "one_turn": True})
        target.attack_temp_boost += atk_boost
        target.health_temp_boost += hlt_boost

    def boost_dragon(self) -> None:
        self.select_and_boost()
        if self.triplet:
            self.select_and_boost()
        