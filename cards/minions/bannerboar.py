from __future__ import annotations
from typing import TYPE_CHECKING
from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class Bannerboar(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 98
        self.classes = [MinionClass.Quilboar]
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 5
        self.hooks["on_turn_end"].append(self.play_blood_gem)

    def select_and_play_blood_gem(self):
        my_pos = self.army.index(self)
        if my_pos > 0:
            bg = BloodGem(self.army.player)
            self.log.debug(f"{self} playing blood gem on {self.army[my_pos - 1]}")
            self.army.player.play_spell_minion(bg, my_pos - 1)
        if my_pos < len(self.army.cards) - 1:
            bg = BloodGem(self.army.player)
            self.log.debug(f"{self} playing blood gem on {self.army[my_pos + 1]}")
            self.army.player.play_spell_minion(bg, my_pos + 1)
        
    def play_blood_gem(self):
        if self.triplet:
            self.select_and_play_blood_gem()
        self.select_and_play_blood_gem()
