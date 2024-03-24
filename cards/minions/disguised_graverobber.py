from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class DisguisedGraverobber(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 105
        self.classes = []
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 3
        self.hooks["battlecry"].append(self.destroy_undead)

    def destroy_undead(self) -> None:
        targets = [t for t in self.army.cards if MinionClass.Undead in t.classes]
        if len(targets) == 0:
            self.log.debug(f"{self} found no undead to destroy")
            return
        target = random.choice(targets)
        self.log.debug(f"{self} destroying {target}")
        if target.rebirth:
            self.log.debug(f"{self} found rebirth at {target}, removing")
            target.death()
            target.feature_overrides["rebirth"].append({"state": False, "one_turn": self.in_fight})
        else:
            self.log.debug(f"{self} destroying {target}")
            target.death()
            for hook in target.hooks["on_lose"]:
                hook()
            if not self.in_fight:
                self.army.player.tavern.sell(target)
        self.army.player.gold += 3
        if self.triplet:
            self.army.player.gold += 3
