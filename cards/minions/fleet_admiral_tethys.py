from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class FleetAdmiralTethys(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 189
        self.classes = [MinionClass.Pirate]
        self.level = 3
        self.base_attack_value = 5
        self.base_health_value = 6
        self.gold_left = 9
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_gold_spent"].append(self.get_pirate)
        
    def remove_hook(self) -> None:
        self.gold_left = 9
        self.army.hooks["on_gold_spent"].remove(self.get_pirate)

    def get_pirate(self, spent_amount):
        self.gold_left -= spent_amount
        if self.gold_left <= 0:
            if self.triplet:
                self.select_and_get_pirate()
            self.select_and_get_pirate()
            self.gold_left += 9

    def select_and_get_pirate(self):
        avail = [p for p in self.army.player.tavern.available_cards() if p.level <= self.army.player.level]
        if not avail:
            return
        p = random.choice(avail)
        self.army.player.tavern.buy(p)
        p.army = self.army
        for hook in p.hooks["on_get"]:
            hook()
        self.army.player.hand.add(p, len(self.army.player.hand))
