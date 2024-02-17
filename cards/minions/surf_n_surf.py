from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.surf_n_surf import SurfNSurf as CrabSpell

if TYPE_CHECKING:
    from models.army import Army


class SurfNSurf(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Beast, MinionClass.Naga]
        self.level = 1
        self.base_attack_value = 1
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["on_turn_start"].append(self.give_crab)

    def give_crab(self) -> None:
        self.army.player.hand.add(CrabSpell(self.army.player))
        if self.triplet:
            self.army.player.hand.add(CrabSpell(self.army.player))