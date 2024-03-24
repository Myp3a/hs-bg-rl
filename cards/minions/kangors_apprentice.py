from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class KangorsApprentice(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 157
        self.classes = [MinionClass.Demon]
        self.level = 5
        self.base_attack_value = 3
        self.base_health_value = 6
        self.hooks["deathrattle"].append(self.summon_two_mechs)

    def summon_two_mechs(self, position) -> None:
        summoned = 0
        for c in self.army.dead:
            if summoned < 2 and MinionClass.Mech in c.classes:
                mech = type(c)(self.army)
                self.log.debug(f"{self} found dead {mech}, summoning")
                mech.enemy_army = self.enemy_army
                for hook in mech.hooks["on_get"]:
                    hook()
                self.army.add(mech, position)
                summoned += 1
