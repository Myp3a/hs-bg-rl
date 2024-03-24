from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class SlitherspearLordOfGains(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 204
        self.classes = [MinionClass.Naga]
        self.level = 6
        self.base_attack_value = 4
        self.base_health_value = 6
        self.hooks["on_turn_end"].append(self.boost_naga)
    
    def boost_naga(self):
        targets = [t for t in self.army.cards if not t is self]
        if not targets:
            self.log.debug(f"{self} found no targets")
            return
        self.log.debug(f"{self} boosting {len(targets)} nagas")
        for t in targets:
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            diff_spells = set([type(s) for s in self.army.player.casted_on_turn])
            atk_boost *= len(diff_spells)
            hlt_boost *= len(diff_spells)
            t.attack_perm_boost += atk_boost
            t.health_perm_boost += hlt_boost
            for hook in self.army.hooks["on_values_change_perm"]:
                hook(t, atk_boost, hlt_boost)
