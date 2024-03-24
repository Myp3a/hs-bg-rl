from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ChoralMrrrglr(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 182
        self.classes = [MinionClass.Murloc]
        self.level = 6
        self.base_attack_value = 6
        self.base_health_value = 6
        self.hooks["on_fight_start"].append(self.get_hand_values)

    def get_hand_values(self):
        targets = [t for t in self.army.player.hand.cards if isinstance(t, Minion)]
        atk_boost = 0
        hlt_boost = 0
        for t in targets:
            atk_boost += t.attack_value
            hlt_boost += t.health_value
        self.log.debug(f"{self} found {len(targets)} minion in hand, getting {atk_boost}/{hlt_boost}")
        self.attack_temp_boost += atk_boost
        self.health_temp_boost += hlt_boost
