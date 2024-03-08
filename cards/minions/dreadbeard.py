from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.gold_coin import GoldCoin

if TYPE_CHECKING:
    from models.army import Army


class Dreadbeard(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 66
        self.classes = [MinionClass.Demon, MinionClass.Pirate]
        self.level = 3
        self.base_attack_value = 4
        self.base_health_value = 4
        self.hooks["on_turn_end"].append(self.damage_hero)

    def damage_hero(self) -> None:
        hero_damage = 1
        self.army.player.health -= hero_damage
        for hook in self.army.hooks["on_hero_damage"]:
            hook(hero_damage)
        if self.triplet:
            self.army.player.hand.add(GoldCoin(self.army.player), len(self.army.player.hand))
        self.army.player.hand.add(GoldCoin(self.army.player), len(self.army.player.hand))