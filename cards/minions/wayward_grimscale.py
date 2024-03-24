from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class WaywardGrimscale(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 137
        self.classes = [MinionClass.Murloc]
        self.level = 4
        self.base_attack_value = 1
        self.base_health_value = 5
        self.hooks["on_defence_pre"].append(self.get_toxic)

    def get_toxic(self, attacker):
        self.log.debug(f"{self} being attacked, getting toxic")
        self.feature_overrides["toxic"].append({"state": True, "one_turn": True})
