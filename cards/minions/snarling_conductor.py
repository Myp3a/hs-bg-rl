from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.spell import Spell

if TYPE_CHECKING:
    from models.army import Army


class SnarlingConductor(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 130
        self.classes = [MinionClass.Quilboar]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 5
        self.hooks["on_turn_start"].append(self.discard_spell)

    def discard_spell(self):
        if self.triplet:
            gold_count = 8
        else:
            gold_count = 4
        for card in self.army.player.hand.cards:
            if isinstance(card, Spell):
                self.log.debug(f"{self} discarding {card}, getting {gold_count} gold")
                self.army.player.hand.cards.remove(card)
                self.army.player.gold += gold_count
                break
