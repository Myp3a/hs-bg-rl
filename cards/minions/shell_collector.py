from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.gold_coin import GoldCoin

if TYPE_CHECKING:
    from models.army import Army


class ShellCollector(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.classes = [MinionClass.Naga]
        self.level = 1
        self.base_attack_value = 2
        self.base_health_value = 1
        self.attack_value = self.base_attack_value
        self.health_value = self.base_health_value
        self.hooks["battlecry"].append(self.give_gold_coin)

    def give_gold_coin(self) -> None:
        self.army.player.hand.add(GoldCoin(self.army.player), len(self.army.player.hand))
        if self.triplet:
            self.army.player.hand.add(GoldCoin(self.army.player), len(self.army.player.hand))
