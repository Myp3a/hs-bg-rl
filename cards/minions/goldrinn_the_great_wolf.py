from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class GoldrinnTheGreatWolf(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 192
        self.classes = [MinionClass.Beast]
        self.level = 6
        self.base_attack_value = 3
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.boost_beasts_this_combat)

    def boost_beasts_this_combat(self, position):
        if self.triplet:
            atk_boost = 6
            hlt_boost = 4
        else:
            atk_boost = 3
            hlt_boost = 2
        curr_beasts = [b for b in self.army.cards if MinionClass.Beast in b.classes]
        for b in curr_beasts:
            b.attack_temp_boost += atk_boost
            b.health_temp_boost += hlt_boost
        self.army.player.beast_boost_atk += atk_boost
        self.army.player.beast_boost_hlt += hlt_boost
