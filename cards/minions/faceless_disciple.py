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
        if len(targets) == 0:
            return
        target = random.choice(targets)
        minion_level = min(target.level + 1, 3)
        new_minion = random.choice([m for m in self.army.player.tavern.available_cards() if m.level == minion_level])
        position = self.army.index(target)
        self.army.remove(target)
        self.army.player.tavern.sell(target)
        self.army.player.tavern.buy(new_minion)
        new_minion.army = self.army
        self.army.add(new_minion, position)
        for hook in self.army.hooks["on_minion_summon"]:
            hook(new_minion)
