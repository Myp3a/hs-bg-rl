from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class GeomagusRoogug(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 109
        self.classes = [MinionClass.Quilboar]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 6
        self.divine_shield = True
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_sell"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_spell_cast"].append(self.play_blood_gem)

    def remove_hook(self) -> None:
        self.army.hooks["on_spell_cast"].remove(self.play_blood_gem)

    def play_blood_gem(self, casted, target):
        if target is self:
            if isinstance(casted, BloodGem):
                targets = [t for t in self.army.cards if not t is self]
                if len(targets) == 0:
                    return
                target = random.choice(targets)
                if self.triplet:
                    bg = BloodGem(self.army.player)
                    self.army.player.play_spell_minion(bg, self.army.index(target))
                bg = BloodGem(self.army.player)
                self.army.player.play_spell_minion(bg, self.army.index(target))