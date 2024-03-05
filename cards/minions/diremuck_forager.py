from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class DiremuckForager(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 65
        self.classes = [MinionClass.Murloc]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 4
        self.divine_shield = True
        self.summon = None
        self.hooks["on_fight_start"].append(self.summon_from_hand)

    def summon_from_hand(self) -> None:
        if len(self.army) == 7:
            return
        to_summon = [t for t in self.army.player.hand if isinstance(t, Minion) and not t.summoned]
        if len(to_summon) == 0:
            return
        summon = random.choice(to_summon)
        if self.triplet:
            atk_boost = 4
            hlt_boost = 4
        else:
            atk_boost = 2
            hlt_boost = 2
        summon.attack_perm_boost += atk_boost
        summon.health_perm_boost += hlt_boost
        summon.summoned = True
        position = self.army.index(self) + 1
        self.army.add(summon, position)
        for hook in self.army.hooks["on_minion_summon"]:
            hook(summon)
