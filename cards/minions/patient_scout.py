from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion

if TYPE_CHECKING:
    from models.army import Army


class PatientScout(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 47
        self.classes = []
        self.level = 2
        self.base_attack_value = 1
        self.base_health_value = 1
        self.tier = 1
        self.hooks["on_turn_start"].append(self.boost_tier)
        self.hooks["on_sell"].append(self.discover)

    def boost_tier(self) -> None:
        if self.tier < 6:
            self.tier += 1

    def discover(self) -> None:
        # TODO: make discover mechanic
        available_cards = [c for c in self.army.player.tavern.available_cards() if c.level <= self.tier]
        if len(available_cards) == 0:
            return
        if len(self.army.player.hand) == 10:
            return
        discovered = random.choice(available_cards)
        card = self.army.player.tavern.buy(discovered)
        card.army = self.army
        for hook in card.hooks["on_get"]:
            hook()
        self.army.player.hand.add(card, len(self.army.player.hand))
