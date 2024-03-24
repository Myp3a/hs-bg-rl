from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class FacelessDisciple(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 69
        self.classes = []
        self.level = 3
        self.base_attack_value = 6
        self.base_health_value = 4
        self.hooks["battlecry"].append(self.upgrade_minion)

    def upgrade_minion(self) -> None:
        targets = [t for t in self.army.cards if not t is self]
        if not targets:
            return
        target = random.choice(targets)
        if self.triplet:
            minion_level = min(target.level + 2, 6)
        else:
            minion_level = min(target.level + 1, 6)
        self.log.debug(f"{self} levelling up {target} to {minion_level}")
        new_minion = random.choice([m for m in self.army.player.tavern.available_cards() if m.level == minion_level])
        self.log.debug(f"{self} changed {target} to {new_minion}")
        position = self.army.index(target)
        self.army.remove(target)
        if not self.in_fight:
            self.log.debug(f"{self} applied tavern change")
            for hook in target.hooks["on_lose"]:
                hook()
            self.army.player.tavern.sell(target)
            self.army.player.tavern.buy(new_minion)
        new_minion.army = self.army
        for hook in new_minion.hooks["on_get"]:
            hook()
        self.army.add(new_minion, position)
        for hook in new_minion.hooks["on_play"]:
            hook()
        for hook in self.army.hooks["on_minion_summon"]:
            hook(new_minion)
