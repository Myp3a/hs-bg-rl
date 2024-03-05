from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class RendleTheMistermind(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 124
        self.classes = []
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 5
        self.hooks["on_turn_end"].append(self.steal_tavern)

    def choose_and_steal(self):
        targets = sorted(self.army.player.view, key=lambda m: m.level, reverse=True)
        if len(targets) == 0:
            return
        if len(self.army.player.hand) == 10:
            return
        self.army.player.tavern.buy(targets[0])
        self.army.player.view.remove(targets[0])
        self.army.player.hand.add(targets[0], len(self.army.player.hand.cards))

    def steal_tavern(self):
        if self.triplet:
            self.choose_and_steal()
        self.choose_and_steal()