from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class Tad(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 54
        self.classes = [MinionClass.Murloc]
        self.level = 2
        self.base_attack_value = 2
        self.base_health_value = 2
        self.hooks["on_sell"].append(self.give_murloc)

    def choose_and_give_murloc(self) -> None:
        cards = [c for c in self.army.player.tavern.available_cards() if c.level <= self.army.player.level and MinionClass.Murloc in c.classes and not c is self]
        if len(cards) == 0:
            return
        if len(self.army.player.hand) == 10:
            return
        card = random.choice(cards)
        self.army.player.tavern.buy(card)
        card.army = self.army
        for hook in card.hooks["on_get"]:
            hook()
        self.army.player.hand.add(card, len(self.army.player.hand))

    def give_murloc(self) -> None:
        self.choose_and_give_murloc()
        if self.triplet:
            self.choose_and_give_murloc()
