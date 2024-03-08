from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class BongoBopper(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 143
        self.classes = [MinionClass.Quilboar]
        self.level = 5
        self.base_attack_value = 4
        self.base_health_value = 3
        self.hooks["on_turn_end"].append(self.give_blood_gems)

    def give_blood_gems(self) -> None:
        if self.triplet:
            count = 4
        else:
            count = 2
        for _ in range(count):
            bg = BloodGem(self.army.player)
            self.army.player.play_spell_minion(bg, self.army.index(self))
        for _ in range(count):
            bg = BloodGem(self.army.player)
            self.army.player.hand.add(bg, len(self.army.player.hand))
