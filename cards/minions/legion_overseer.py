from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class LegionOverseer(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 75
        self.classes = [MinionClass.Demon]
        self.level = 3
        self.base_attack_value = 4
        self.base_health_value = 2
        self.hooks["on_play"].append(self.boost_tavern)
        self.hooks["on_lose"].append(self.hinder_tavern)

    def boost_tavern(self):
        if self.triplet:
            atk_boost = 4
            hlt_boost = 2
        else:
            atk_boost = 2
            hlt_boost = 1
        self.army.player.tavern_attack_boost += atk_boost
        self.army.player.tavern_health_boost += hlt_boost

    def hinder_tavern(self):
        if self.triplet:
            atk_boost = 4
            hlt_boost = 2
        else:
            atk_boost = 2
            hlt_boost = 1
        self.army.player.tavern_attack_boost -= atk_boost
        self.army.player.tavern_health_boost -= hlt_boost
