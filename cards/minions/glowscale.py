from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.glowing_crown import GlowingCrown

if TYPE_CHECKING:
    from models.army import Army


class Glowscale(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 153
        self.classes = [MinionClass.Naga]
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 6
        self.base_taunt = True
        self.hooks["on_turn_start"].append(self.give_crown)

    def give_crown(self) -> None:
        if self.triplet:
            self.army.player.hand.add(GlowingCrown(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(GlowingCrown(self.army.player), len(self.army.player.hand))
