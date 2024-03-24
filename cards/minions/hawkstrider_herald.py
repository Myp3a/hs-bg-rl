from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class HawkstriderHerald(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 193
        self.classes = [MinionClass.Beast]
        self.level = 6
        self.base_attack_value = 6
        self.base_health_value = 2
        self.hooks["on_fight_start"].append(self.trigger_deathrattles)

    def trigger_deathrattles(self):
        for m in self.army.cards:
            self.log.debug(f"{self} triggering deathrattles for {m}")
            for hook in m.hooks["deathrattle"]:
                hook(self.army.index(m))
