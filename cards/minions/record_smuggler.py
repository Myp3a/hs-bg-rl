from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RecordSmuggler(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 168
        self.classes = [MinionClass.Pirate]
        self.level = 5
        self.base_attack_value = 5
        self.base_health_value = 4
        self.hooks["on_turn_start"].append(self.give_gold)

    def give_gold(self):
        if self.triplet:
            gold = 2
        else:
            gold = 1
        for _ in range(len([t for t in self.army.cards if MinionClass.Pirate in t.classes])):
            self.army.player.gold += gold
            for hook in self.army.hooks["on_gold_get"]:
                hook(gold)
            