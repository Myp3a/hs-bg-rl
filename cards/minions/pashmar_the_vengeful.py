from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from spells import *

if TYPE_CHECKING:
    from models.army import Army


class PashmarTheVengeful(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 83
        self.classes = [MinionClass.Naga]
        self.level = 3
        self.base_attack_value = 4
        self.base_health_value = 5
        self.avenge_cntr = 3
        self.hooks["on_sell"].append(self.give_spell)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_turn_end"].append(self.put_hook)
        self.hooks["on_death"].append(self.remove_hook)

    def put_hook(self) -> None:
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if not died is self:
            self.avenge_cntr -= 1
        if self.avenge_cntr == 0:
            self.give_spell()
            self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 3
        self.hooks["on_death"] = [self.remove_hook]

    def choose_and_give_spell(self) -> None:
        # TODO: add all spells
        spells = [
            AnglersLure(self.army.player),
            SickRiffs(self.army.player),
            SurfNSurf(self.army.player),
            DefendToTheDeath(self.army.player)
        ]
        available = [s for s in spells if s.level <= self.army.player.level]
        if len(available) == 0:
            return
        spell = random.choice(available)
        self.army.player.hand.add(spell, len(self.army.player.hand))

    def give_spell(self):
        if self.triplet:
            self.choose_and_give_spell()
        self.choose_and_give_spell()
