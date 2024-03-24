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
        if not targets:
            self.log.debug(f"{self} found no targets to steal")
            return
        if len(self.army.player.hand) == 10:
            self.log.debug(f"{self} {self.army.player} hand is full")
            return
        self.log.debug(f"{self} stealing {targets[0]}")
        self.army.player.tavern.buy(targets[0])
        targets[0].army = self.army
        self.army.player.view.remove(targets[0])
        for hook in targets[0].hooks["on_get"]:
            hook()
        self.army.player.hand.add(targets[0], len(self.army.player.hand.cards))

    def steal_tavern(self):
        if self.triplet:
            self.choose_and_steal()
        self.choose_and_steal()
