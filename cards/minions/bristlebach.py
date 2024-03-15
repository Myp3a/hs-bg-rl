from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class Bristlebach(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 180
        self.classes = [MinionClass.Quilboar]
        self.level = 6
        self.base_attack_value = 3
        self.base_health_value = 10
        self.avenge_cntr = 2
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if self.health_value > 0:
            if not died is self:
                self.avenge_cntr -= 1
            if self.avenge_cntr == 0:
                if self.triplet:
                    count = 4
                else:
                    count = 2
                for _ in range(count):
                    self.play_blood_gem()
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 3

    def play_blood_gem(self):
        targets = [t for t in self.army.cards if MinionClass.Quilboar in t.classes]
        for t in targets:
            bg = BloodGem(self.army.player)
            self.army.player.play_spell_minion(bg, self.army.index(t))
