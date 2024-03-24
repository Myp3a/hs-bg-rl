from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spell import Spell
from cards.spells.blood_gem import BloodGem

if TYPE_CHECKING:
    from models.army import Army


class MangledBandit(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 77
        self.classes = [MinionClass.Quilboar]
        self.level = 3
        self.base_attack_value = 3
        self.base_health_value = 3
        self.hooks["on_turn_start"].append(self.discard_spell)

    def discard_spell(self):
        if self.triplet:
            gem_count = 6
        else:
            gem_count = 3
        for card in self.army.player.hand.cards:
            if isinstance(card, Spell):
                self.log.debug(f"{self} discarding {card}, getting {gem_count} blood gems")
                self.army.player.hand.cards.remove(card)
                for _ in range(gem_count):
                    self.army.player.hand.add(BloodGem(self.army.player), len(self.army.player.hand))
                break
