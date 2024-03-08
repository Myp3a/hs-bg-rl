from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SindoreiStraightShot(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 128
        self.classes = [MinionClass.Naga]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 4
        self.base_windfury = True
        self.base_divine_shield = True
        self.hooks["on_attack_pre"].append(self.remove_features)

    def remove_features(self, target: Minion) -> None:
        target.feature_overrides["taunt"].append({"state": False, "one_turn": True})
        target.feature_overrides["rebirth"].append({"state": False, "one_turn": True})
