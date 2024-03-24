from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .scallywag import Scallywag

if TYPE_CHECKING:
    from models.army import Army


class RapscallionRecruiter(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 167
        self.classes = [MinionClass.Pirate]
        self.level = 5
        self.base_attack_value = 9
        self.base_health_value = 3
        self.hooks["deathrattle"].append(self.summon_scallywags)

    def summon_scallywags(self, position):
        for _ in range(3):
            sw = Scallywag(self.army)
            if self.triplet:
                sw.triplet = True
            self.log.debug(f"{self} summoning {sw}")
            for hook in sw.hooks["on_get"]:
                hook()
            self.army.add(sw, position)
