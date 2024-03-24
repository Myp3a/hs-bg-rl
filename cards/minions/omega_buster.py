from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from .microbot import Microbot

if TYPE_CHECKING:
    from models.army import Army


class OmegaBuster(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 200
        self.classes = [MinionClass.Mech]
        self.level = 6
        self.base_attack_value = 6
        self.base_health_value = 6
        self.hooks["deathrattle"].append(self.try_summon_microbots)

    def try_summon_microbots(self, position):
        for _ in range(6):
            self.summon_microbot(position)

    def summon_microbot(self, position):
        if len(self.army) == 7:
            self.boost_mechs()
        else:
            mb = Microbot(self.army)
            mb.triplet = self.triplet
            self.log.debug(f"{self} summoning {mb}")
            self.army.add(mb, position)
            for hook in mb.hooks["on_get"]:
                hook()
            for hook in self.army.hooks["on_minion_summon"]:
                hook(mb)

    def boost_mechs(self):
        targets = [t for t in self.army.cards if MinionClass.Mech in t.classes]
        if not targets:
            self.log.debug(f"{self} found no targets")
            return
        self.log.debug(f"{self} boosting {len(targets)} mechs")
        for t in targets:
            if self.triplet:
                atk_boost = 2
                hlt_boost = 2
            else:
                atk_boost = 1
                hlt_boost = 1
            t.attack_temp_boost += atk_boost
            t.health_temp_boost += hlt_boost
