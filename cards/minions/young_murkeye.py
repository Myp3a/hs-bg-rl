from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class YoungMurkeye(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 208
        self.classes = [MinionClass.Murloc]
        self.level = 6
        self.base_attack_value = 8
        self.base_health_value = 5
        self.hooks["on_turn_end"].append(self.trigger_battlecries)

    def choose_and_trigger_battlecries(self, position):
        if position > 0:
            for hook in self.army.cards[position - 1].hooks["battlecry"]:
                for _ in range(self.army.player.count_brann_times()):
                    hook()
        if position < len(self.army.cards):
            for hook in self.army.cards[position].hooks["battlecry"]:
                for _ in range(self.army.player.count_brann_times()):
                    hook()

    def trigger_battlecries(self):
        position = self.army.index(self)
        if self.triplet:
            self.choose_and_trigger_battlecries(position)
        self.choose_and_trigger_battlecries(position)
