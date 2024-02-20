from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.surf_n_surf import SurfNSurf as CrabSpell

if TYPE_CHECKING:
    from models.army import Army


class SurfNSurf(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 22
        self.classes = [MinionClass.Beast, MinionClass.Naga]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 1
        self.hooks["on_turn_start"].append(self.give_crab)

    def give_crab(self) -> None:
        if self.triplet:
            self.army.player.hand.add(CrabSpell(self.army.player, triplet=True), len(self.army.player.hand))
        else:
            self.army.player.hand.add(CrabSpell(self.army.player), len(self.army.player.hand))
