from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from cards.minion import Minion

class GlowingCrown(TargetedSpell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player, triplet)
        self.target = None
        self.spell_id = 9
        self.level = 5
        self.spellcraft = True

    def play(self, target: Minion) -> None:
        self.target = target
        target.feature_overrides["shield"].append({"state": True, "one_turn": True})
    