from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RylakMetalhead(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 125
        self.classes = [MinionClass.Beast]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 4
        self.base_taunt = True
        self.hooks["deathrattle"].append(self.trigger_battlecries)

    def choose_and_trigger_battlecries(self, position):
        if position > 0:
            self.log.debug(f"{self} triggering battlecries for {self.army.cards[position - 1]}")
            for hook in self.army.cards[position - 1].hooks["battlecry"]:
                for _ in range(self.army.player.count_brann_times()):
                    hook()
        if position < len(self.army.cards):
            self.log.debug(f"{self} triggering battlecries for {self.army.cards[position]}")
            for hook in self.army.cards[position].hooks["battlecry"]:
                for _ in range(self.army.player.count_brann_times()):
                    hook()

    def trigger_battlecries(self, position):
        if self.triplet:
            self.choose_and_trigger_battlecries(position)
        self.choose_and_trigger_battlecries(position)
