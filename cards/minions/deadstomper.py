from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Deadstomper(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 184
        self.classes = [MinionClass.Beast, MinionClass.Undead]
        self.level = 6
        self.base_attack_value = 2
        self.base_health_value = 6
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_summon")
        self.army.hooks["on_minion_summon"].append(self.on_summon)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_summon")
        self.army.hooks["on_minion_summon"].remove(self.on_summon)

    def on_summon(self, summoned: Minion):
        if self.in_fight:
            self.log.debug(f"{self} found summoned minion, boosting army atk")
            for t in self.army.cards:
                if self.triplet:
                    atk_boost = 6
                else:
                    atk_boost = 3
                t.attack_temp_boost += atk_boost
