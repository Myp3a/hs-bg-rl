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
        self.base_divine_shield = True
        self.hooks["on_play"].append(self.put_hook)
        self.hooks["on_lose"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_spell_cast")
        self.army.hooks["on_spell_cast"].append(self.play_blood_gem)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_spell_cast")
        self.army.hooks["on_spell_cast"].remove(self.play_blood_gem)

    def play_blood_gem(self, casted, target):
        if target is self and isinstance(casted, BloodGem):
            targets = [t for t in self.army.cards if not t is self]
            if not targets:
                self.log.debug(f"{self} found no other minions to play blood gem")
                return
            target = random.choice(targets)
            self.log.debug(f"{self} playing blood gem on {target}")
            if self.triplet:
                bg = BloodGem(self.army.player)
                self.army.player.play_spell_minion(bg, self.army.index(target))
            bg = BloodGem(self.army.player)
            self.army.player.play_spell_minion(bg, self.army.index(target))