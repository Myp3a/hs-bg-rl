from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MalchezaarPrinceOfDance(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 114
        self.classes = [MinionClass.Demon]
        self.level = 4
        self.base_attack_value = 6
        self.base_health_value = 3
        self.rolls = 0
        self.hooks["on_roll"].append(self.damage_hero)
        self.hooks["on_turn_start"].append(self.reset_rolls)
        self.hooks["on_play"].append(self.reset_rolls)

    def reset_rolls(self):
        if self.triplet:
            self.rolls = 4
        self.rolls = 2

    def damage_hero(self):
        hero_damage = 1
        if not self.army.player.damaged_for_roll and self.rolls > 0:
            self.rolls -= 1
            self.army.player.damaged_for_roll = True
            self.army.player.health -= hero_damage
            for hook in self.army.hooks["on_hero_damage"]:
                hook(hero_damage)
