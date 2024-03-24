from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spells import *

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
        self.hooks["on_lose"].append(self.remove_hook)
        self.hooks["on_turn_start"].append(self.reset_avenge)
        self.hooks["on_play"].append(self.put_hook)

    def put_hook(self) -> None:
        self.log.debug(f"{self} put hook on_minion_death")
        self.army.hooks["on_minion_death"].append(self.on_another_death)

    def remove_hook(self) -> None:
        self.log.debug(f"{self} removed hook on_minion_death")
        self.army.hooks["on_minion_death"].remove(self.on_another_death)

    def on_another_death(self, died, position) -> None:
        if self.health_value > 0 and self in self.army.cards:
            if not died is self:
                self.avenge_cntr -= 1
            self.log.debug(f"{self} decreased avenge, new cntr {self.avenge_cntr}")
            if self.avenge_cntr == 0:
                self.give_spell()
                self.reset_avenge()

    def reset_avenge(self) -> None:
        self.avenge_cntr = 3

    def choose_and_give_spell(self) -> None:
        # TODO: add all spells
        spells = [
            AnglersLure(self.army.player),
            SickRiffs(self.army.player),
            SurfNSurf(self.army.player),
            DefendToTheDeath(self.army.player),
            JustKeepSwimming(self.army.player),
            DeepBlues(self.army.player),
            GlowingCrown(self.army.player)
        ]
        available = [s for s in spells if s.level <= self.army.player.level]
        if not available:
            self.log.debug(f"{self} no spells available")
            return
        spell = random.choice(available)
        self.log.debug(f"{self} gives {spell}")
        self.army.player.hand.add(spell, len(self.army.player.hand))

    def give_spell(self):
        if self.triplet:
            self.choose_and_give_spell()
        self.choose_and_give_spell()
