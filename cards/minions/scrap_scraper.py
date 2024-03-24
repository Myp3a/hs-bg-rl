from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class ScrapScraper(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 171
        self.classes = [MinionClass.Mech]
        self.level = 5
        self.base_attack_value = 6
        self.base_health_value = 5
        self.hooks["deathrattle"].append(self.get_magnetic_mech)

    def choose_and_get_magnetic_mech(self):
        mechs = [c for c in self.army.player.tavern.available_cards() if MinionClass.Mech in c.classes and c.magnetic]
        if not mechs:
            self.log.debug(f"{self} found no magnetic mechs")
            return
        mech = random.choice(mechs)
        self.log.debug(f"{self} getting magnetic {mech}")
        self.army.player.tavern.buy(mech)
        mech.army = self.army
        for hook in mech.hooks["on_get"]:
            hook()
        self.army.player.hand.add(mech, len(self.army.player.hand))

    def get_magnetic_mech(self, position):
        if self.triplet:
            self.choose_and_get_magnetic_mech()
        self.choose_and_get_magnetic_mech()
