from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .skeleton import Skeleton

if TYPE_CHECKING:
    from models.army import Army


class HarmlessBonehead(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 3
        self.classes = [MinionClass.Undead]
        self.level = 1
        self.base_attack_value = 0
        self.base_health_value = 2
        self.hooks["deathrattle"].append(self.summon_skeletons)

    def summon_skeletons(self, position) -> None:
        for _ in range(2):
            skel = Skeleton(self.army)
            if self.triplet:
                skel.triplet = True
            self.log.debug(f"{self} summoning {skel}")
            for hook in skel.hooks["on_get"]:
                hook()
            self.army.add(skel, position)
            for hook in self.army.hooks["on_minion_summon"]:
                hook(skel)