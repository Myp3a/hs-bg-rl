from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class Charlga(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 181
        self.classes = [MinionClass.Quilboar]
        self.level = 6
        self.base_attack_value = 4
        self.base_health_value = 4
        self.hooks["on_turn_end"].append(self.play_blood_gem)

    def play_blood_gem(self):
        targets = [t for t in self.army.cards if not t is self]
        for t in targets:
            bg = BloodGem(self.army.player)
            self.army.player.play_spell_minion(bg, self.army.index(t))
