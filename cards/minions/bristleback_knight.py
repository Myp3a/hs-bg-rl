from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class BristlebackKnight(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 145
        self.classes = [MinionClass.Quilboar]
        self.level = 5
        self.base_attack_value = 6
        self.base_health_value = 9
        self.base_windfury = True
        self.base_divine_shield = True
        self.hits_left = 0
        self.hooks["on_take_hit_post"].append(self.get_shield)
        self.hooks["on_play"].append(self.reset_hits)
        self.hooks["on_turn_start"].append(self.reset_hits)

    def reset_hits(self):
        if self.triplet:
            self.hits_left = 2
        else:
            self.hits_left = 1

    def get_shield(self, attacker: Minion):
        if self.hits_left > 0:
            if self.health_value > 0:
                self.log.debug(f"{self} got not deadly hit, getting shield")
                self.feature_overrides["shield"].append({"state": True, "one_turn": True})
